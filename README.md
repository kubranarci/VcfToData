# VcfToData

VcfToData is a Python tool for converting VCF files into table format (TSV or CSV) with additional annotations such as GNOMAD allele frequency and customizable INFO/FORMAT fields.

## Installation

To install VcfToData, clone the repository and install the required dependencies:




```bash
git clone https://github.com/kubranarci/VcfToData.git 
cd VcfToData 
pip install -e .

```

## Usage
VcfToData <vcf_file> <gene_list> <gnomad_af> <output> --info-fields RankScore --format-fields GT DB


## Options

vcf_file: The input VCF file.

output_file: The output CSV file.

--gene-list: Optional file with a list of genes to annotate.

--gnomad-af: Optional GNOMAD_AF file for allele frequency data.

--info-fields: Space-separated list of INFO fields to extract (e.g., RankScore, Annotation).

--format-fields: Space-separated list of FORMAT fields to extract (e.g., GT, DB).