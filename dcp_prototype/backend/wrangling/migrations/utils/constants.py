from dcp_prototype.backend.ledger.code.common.ledger_orm import (
    AlignmentProtocol,
    QuantificationProtocol,
)

# Prefix that will be used for every single ID that is generated for every single entity
# in the DCP.
ID_GENERATOR_PREFIX = "HCA"

# Alignment protocol for SmartSeq2 data used to migration DCP 1.0 data to DCP 2.0.
SS2_ALIGNMENT_PROTOCOL = AlignmentProtocol(
    software="HCA Smart-Seq2 Workflow",
    algorithm="HISAT2",
    genome_reference="GRCh38 primary assembly",
    genomic_annotation="GENCODE v27",
    genomic_annotation_biotypes=[
        "3prime_overlapping_ncRNA",
        "antisense_RNA",
        "bidirectional_promoter_lncRNA",
        "IG_C_gene",
        "IG_C_pseudogene",
        "IG_D_gene",
        "IG_J_gene",
        "IG_J_pseudogene",
        "IG_pseudogene",
        "IG_V_gene",
        "IG_V_pseudogene",
        "lincRNA",
        "macro_lncRNA",
        "miRNA",
        "misc_RNA",
        "Mt_rRNA",
        "Mt_tRNA",
        "non_coding",
        "polymorphic_pseudogene",
        "processed_pseudogene",
        "processed_transcript",
        "protein_coding",
        "pseudogene",
        "ribozyme",
        "rRNA",
        "scaRNA",
        "scRNA",
        "sense_intronic",
        "sense_overlapping",
        "snoRNA",
        "snRNA",
        "sRNA",
        "TEC",
        "transcribed_processed_pseudogene",
        "transcribed_unitary_pseudogene",
        "transcribed_unprocessed_pseudogene",
        "translated_processed_pseudogene",
        "TR_C_gene",
        "TR_D_gene",
        "TR_J_gene",
        "TR_J_pseudogene",
        "TR_V_gene",
        "TR_V_pseudogene",
        "unitary_pseudogene",
        "unprocessed_pseudogene",
        "vaultRNA",
    ],
)

# Alignment protocol for 10x data used to migration DCP 1.0 data to DCP 2.0.
X10_ALIGNMENT_PROTOCOL = AlignmentProtocol(
    software="HCA Optimus Workflow",
    algorithm="STAR",
    genome_reference="GRCh38 primary assembly",
    genomic_annotation="GENCODE v27",
    genomic_annotation_biotypes=[
        "3prime_overlapping_ncRNA",
        "antisense_RNA",
        "bidirectional_promoter_lncRNA",
        "IG_C_gene",
        "IG_C_pseudogene",
        "IG_D_gene",
        "IG_J_gene",
        "IG_J_pseudogene",
        "IG_pseudogene",
        "IG_V_gene",
        "IG_V_pseudogene",
        "lincRNA",
        "macro_lncRNA",
        "miRNA",
        "misc_RNA",
        "Mt_rRNA",
        "Mt_tRNA",
        "non_coding",
        "polymorphic_pseudogene",
        "processed_pseudogene",
        "processed_transcript",
        "protein_coding",
        "pseudogene",
        "ribozyme",
        "rRNA",
        "scaRNA",
        "scRNA",
        "sense_intronic",
        "sense_overlapping",
        "snoRNA",
        "snRNA",
        "sRNA",
        "TEC",
        "transcribed_processed_pseudogene",
        "transcribed_unitary_pseudogene",
        "transcribed_unprocessed_pseudogene",
        "translated_processed_pseudogene",
        "TR_C_gene",
        "TR_D_gene",
        "TR_J_gene",
        "TR_J_pseudogene",
        "TR_V_gene",
        "TR_V_pseudogene",
        "unitary_pseudogene",
        "unprocessed_pseudogene",
        "vaultRNA",
    ],
)

SS2_QUANTIFICATION_PROTOCOL = QuantificationProtocol(quantification_software="RSEM")

X10_QUANTIFICATION_PROTOCOL = QuantificationProtocol(
    quantification_software="HCA Single Cell Tools"
)

ENTITY_TYPES = [
    "donor_organism",
    "specimen_from_organism",
    "cell_suspension",
    "library_preparation_protocol",
    "project",
    "sequence_file",
    "links",
    "sequencing_protocol",
    "analysis_file",
]
