import os
import pytest
import json
from vcf_to_data.process_vcf import process_vcf

# Fixture to return the path to the test VCF file
@pytest.fixture
def small_vcf():
    """Fixture to point to the VCF file located under 'tests/data/test.vcf'."""
    return os.path.join(os.path.dirname(__file__), 'data', 'test.vcf')

@pytest.fixture
def gene_list_file():
    """Fixture to create a simple gene list file."""
    gene_list = '''GENE1
GENE2
'''
    gene_list_path = os.path.join(os.path.dirname(__file__), 'test_gene_list.txt')
    with open(gene_list_path, 'w') as f:
        f.write(gene_list)
    return gene_list_path

@pytest.fixture
def gnomad_af_file():
    """Fixture to create a simple GNOMAD AF file."""
    gnomad_af_content = '''1   12198   G,C   0.005
1   12237   G,A   0.01
'''
    gnomad_af_path = os.path.join(os.path.dirname(__file__), 'test_gnomad_af.txt')
    with open(gnomad_af_path, 'w') as f:
        f.write(gnomad_af_content)
    return gnomad_af_path

def test_vcf_to_tsv(small_vcf, gene_list_file, gnomad_af_file):
    """Test the conversion of VCF to TSV format."""
    output_file = "test_output.tsv"
    process_vcf(
        vcf_file=small_vcf,
        gene_list_file=gene_list_file,
        gnomad_af_file=gnomad_af_file,
        output_file=output_file,
        info_fields=["RankScore", "Annotation", "GNOMADAF_popmax"],
        format_fields=["GT"],
        output_format="tsv"
    )
    
    # Check the TSV file contents
    with open(output_file, 'r') as f:
        lines = f.readlines()
        
        # Ensure header contains correct fields
        header = lines[0].strip().split('\t')
        assert "CHROM" in header
        assert "POS" in header
        assert "RankScore" in header
        assert "Annotation" in header
        assert "GNOMADAF_popmax" in header
        assert "Sample1_GT" in header
        
        # Check that the second line contains expected values (for example, for the first variant)
        second_line = lines[1].strip().split('\t')
        assert second_line[0] == "1"
        assert second_line[1] == "12198"
        assert second_line[8] == "GENE1"
        assert second_line[9] == "0.005"  # GNOMAD_AF for this position

def test_vcf_to_json(small_vcf, gene_list_file, gnomad_af_file):
    """Test the conversion of VCF to JSON format."""
    output_file = "test_output.json"
    process_vcf(
        vcf_file=small_vcf,
        gene_list_file=gene_list_file,
        gnomad_af_file=gnomad_af_file,
        output_file=output_file,
        info_fields=["RankScore", "Annotation", "GNOMADAF_popmax"],
        format_fields=["GT"],
        output_format="json"
    )
    
    # Check if the JSON file was created correctly
    with open(output_file, 'r') as f:
        data = json.load(f)
        
        # Ensure the JSON contains the expected fields
        assert "CHROM" in data[0]
        assert "POS" in data[0]
        assert "RankScore" in data[0]
        assert "Annotation" in data[0]
        assert "GNOMADAF_popmax" in data[0]
        
        # Check the values for the first record
        assert data[0]["CHROM"] == "1"
        assert data[0]["POS"] == 12198
        assert data[0]["Annotation"] == "GENE1"
        assert data[0]["GNOMADAF_popmax"] == "0.005"

def test_vcf_to_csv(small_vcf, gene_list_file, gnomad_af_file):
    """Test the conversion of VCF to CSV format."""
    output_file = "test_output.csv"
    process_vcf(
        vcf_file=small_vcf,
        gene_list_file=gene_list_file,
        gnomad_af_file=gnomad_af_file,
        output_file=output_file,
        info_fields=["RankScore", "Annotation", "GNOMADAF_popmax"],
        format_fields=["GT"],
        output_format="csv"
    )
    
    # Check the CSV file contents
    with open(output_file, 'r') as f:
        lines = f.readlines()
        
        # Ensure header contains correct fields
        header = lines[0].strip().split(',')
        assert "CHROM" in header
        assert "POS" in header
        assert "RankScore" in header
        assert "Annotation" in header
        assert "GNOMADAF_popmax" in header
        assert "Sample1_GT" in header
        
        # Check that the second line contains expected values (for example, for the first variant)
        second_line = lines[1].strip().split(',')
        assert second_line[0] == "1"
        assert second_line[1] == "12198"
        assert second_line[8] == "GENE1"
        assert second_line[9] == "0.005"  # GNOMAD_AF for this position
