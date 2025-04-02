from setuptools import setup, find_packages

setup(
    name="VcfToData",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pysam",
    ],
    entry_points={
        "console_scripts": [
            "vcf-to-data=vcf_to_data.main:main",
        ],
    },
    author="Kuebra Narci",
    author_email="kuebra.narci@dkfz-heidelberg.de",
    description="A tool to convert VCF files into structured data formats.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
