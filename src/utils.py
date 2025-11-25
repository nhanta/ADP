import gzip
import pandas as pd

def read_vcf(vcf_path):
    # open file .vcf.gz
    opener = gzip.open if vcf_path.endswith(".gz") else open

    with opener(vcf_path, "rt") as ifile:
        for line in ifile:
            if line.startswith("#CHROM"):
                vcf_names = line.strip().split('\t')
                break

    # Read data
    data = pd.read_csv(
        vcf_path,
        compression="gzip",
        comment="#",
        sep="\s+",
        header=None,
        names=vcf_names
    )
    return data

def save_vcf(data, output_VCF, header):
    """Save a DataFrame as a VCF file using an existing header."""

    # Ensure header ends with newline
    if not header.endswith("\n"):
        header += "\n"

    # Write header
    with open(output_VCF, 'w') as vcf:
        vcf.write(header)

    # Append body without adding column names again
    data.to_csv(output_VCF, sep="\t", mode='a', index=False, header=False)
