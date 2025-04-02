import os
import sys
from argparse import ArgumentParser
from vcf_to_data.process_vcf import process_vcf

def main():
    parser = ArgumentParser(description='VCF to Table converter')
    
    # Required arguments
    parser.add_argument('--vcf-file', required=True, help='VCF file path')
    parser.add_argument('--output', required=True, help='Output file path')
    
    # Optional arguments
    parser.add_argument('--gene-list-file', help='Gene list file path (optional)')
    parser.add_argument('--gnomad-af', help='GNOMAD_AF file path (optional, tab or tab.gz)')
    
    # Output format
    parser.add_argument('--output-format', choices=['csv', 'tsv', 'json'], default='tsv', help='Output format (csv, tsv, json)')
    
    # INFO and FORMAT fields to extract
    parser.add_argument('--info-fields', nargs='+', default=['RankScore', 'most_severe_consequence', 'most_severe_pli', 'Annotation', 'RankResult', 'GeneticModels', 'GNOMADAF_popmax'], help='INFO fields to extract')
    parser.add_argument('--format-fields', nargs='+', default=['GT'], help='FORMAT fields to extract (e.g., GT, DB)')
    
    args = parser.parse_args()

    # Call process_vcf function to process the VCF and generate output
    process_vcf(
        vcf_file=args.vcf_file,
        gene_list_file=args.gene_list_file,
        gnomad_af_file=args.gnomad_af,
        output_file=args.output,
        info_fields=args.info_fields,
        format_fields=args.format_fields,
        output_format=args.output_format
    )

if __name__ == "__main__":
    main()
