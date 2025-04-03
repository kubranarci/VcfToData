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
vcf-to-data --vcf <vcf_file> --out <output> --gene-list <gene_list> --gnomad-af <gnomad_af> --info-fields RankScore --format-fields GT DB


## Options

--vcf: The input VCF file.

--out: Output prefix.

--output-format: The format of the output file - csv, tab or json

--gene-list: Optional file with a list of genes to annotate.

--gnomad-af: Optional GNOMAD_AF file for allele frequency data.

--info-fields: Space-separated list of INFO fields to extract (e.g., RankScore, Annotation).

--format-fields: Space-separated list of FORMAT fields to extract (e.g., GT, DB).