"""Transforms user input to GeneSignature instance.
"""

from .soft_file_factory.file_manager import get_example_file

from .signature_factory import \
    from_geo,\
    from_file,\
    from_gene_list
