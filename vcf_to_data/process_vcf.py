import pysam
import csv
import json
import gzip

def process_vcf(vcf_file, gene_list_file, gnomad_af_file, output_file, info_fields, format_fields, output_format):
    # Load GNOMAD_AF data into a dictionary (if provided)
    gnomad_af_data = {}
    if gnomad_af_file:
        open_func = gzip.open if gnomad_af_file.endswith(".gz") else open
        with open_func(gnomad_af_file, 'rt') as f:
            for line in f:
                parts = line.strip().split("\t")
                if len(parts) < 4:
                    continue
                chrom, pos, alt, gnomad_af = parts
                pos = str(pos)  # Ensure consistency with VCF positions
                alt_alleles = alt.split(",")  # Handle multiple ALT alleles
                for a in alt_alleles:
                    gnomad_af_data[(chrom, pos, a)] = gnomad_af

    # Open the VCF file
    vcf = pysam.VariantFile(vcf_file)

    # Extract sample names
    samples = list(vcf.header.samples)

    # Load gene list from file (if provided)
    gene_list = set()
    if gene_list_file:
        with open(gene_list_file) as f:
            gene_list = {line.strip() for line in f}

    # Prepare to write the output in the desired format
    if output_format == "csv":
        open_func = open
        writer_func = csv.writer
        delimiter = ","
    elif output_format == "json":
        open_func = open
        writer_func = None  # JSON has a different format
    else:  # Default to TSV format
        open_func = open
        writer_func = csv.writer
        delimiter = "\t"

    with open(output_file, "w", newline="") as tsv_out:
        if output_format != "json":
            writer = writer_func(tsv_out, delimiter=delimiter)
            # Write header
            header = [
                "CHROM", "POS", "ID", "REF", "ALT"
            ]
            if gnomad_af_file:  # Only add GNOMAD_AF if the file is provided
                header.append("GNOMAD_AF")

            header += info_fields + [f"{s}_{field}" for s in samples for field in format_fields]
            writer.writerow(header)

        # Process each variant in the VCF
        data_rows = []  # For JSON output
        for record in vcf:
            chrom = record.chrom
            pos = str(record.pos)  # Ensure consistency with GNOMAD_AF file
            vid = record.id if record.id else "."
            ref = record.ref
            alts = record.alts if record.alts else ["."]

            # Extract GNOMAD_AF value (handling multiple ALT alleles)
            gnomad_af_values = [gnomad_af_data.get((chrom, pos, alt), "NA") for alt in alts]
            gnomad_af_value = ",".join(gnomad_af_values) if gnomad_af_file else "NA"  # Only set if GNOMAD_AF file is provided

            # Extract INFO fields
            info_values = [str(record.info.get(field, "NA")) for field in info_fields]

            # Extract FORMAT fields for each sample
            format_values = []
            for sample in samples:
                for field in format_fields:
                    format_value = record.samples[sample].get(field, "NA")
                    if isinstance(format_value, (tuple, list)):
                        format_value = "/".join(map(str, format_value))
                    format_values.append(format_value)

            # Prepare the row
            row = [
                chrom, pos, vid, ref, ",".join(alts),
                gnomad_af_value
            ] + info_values + format_values

            # For JSON output
            if output_format == "json":
                row_data = {
                    "CHROM": chrom,
                    "POS": pos,
                    "ID": vid,
                    "REF": ref,
                    "ALT": ",".join(alts),
                }
                if gnomad_af_file:
                    row_data["GNOMAD_AF"] = gnomad_af_value

                # Add INFO fields
                for field, value in zip(info_fields, info_values):
                    row_data[field] = value

                # Add FORMAT fields
                for sample, format_field, value in zip(samples, format_fields, format_values):
                    row_data[f"{sample}_{format_field}"] = value

                data_rows.append(row_data)
            else:
                # Write row to CSV/TSV
                writer.writerow(row)

        # Write JSON output if requested
        if output_format == "json":
            json.dump(data_rows, tsv_out, indent=4)

    print(f"{output_format.upper()} file saved: {output_file}")
