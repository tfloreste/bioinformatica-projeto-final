CREATE SCHEMA schizophrenia;

CREATE TABLE schizophrenia.clinvar ( 
	id                   int UNSIGNED NOT NULL  ,
	clinical_significance varchar(100)    ,
	variant_type         varchar(100)    ,
	CONSTRAINT pk_clinvar PRIMARY KEY ( id )
 ) engine=InnoDB;

CREATE TABLE schizophrenia.genes ( 
	gene_symbol          varchar(10)  NOT NULL  ,
	location             varchar(50)    ,
	CONSTRAINT pk_gene PRIMARY KEY ( gene_symbol )
 ) engine=InnoDB;

CREATE TABLE schizophrenia.go ( 
	go_id                int UNSIGNED NOT NULL  ,
	category             varchar(50)    ,
	CONSTRAINT pk_go PRIMARY KEY ( go_id )
 ) engine=InnoDB;

CREATE TABLE schizophrenia.transcripts_proteins ( 
	accession_mrna       varchar(25)  NOT NULL  ,
	accession_protein    varchar(25)    ,
	size_mrna            int UNSIGNED   ,
	size_protein         int UNSIGNED   ,
	gene_symbol          varchar(10)    ,
	CONSTRAINT pk_transcript_protein PRIMARY KEY ( accession_mrna )
 ) engine=InnoDB;

CREATE INDEX idx_transcripts_proteins ON schizophrenia.transcripts_proteins ( gene_symbol );

CREATE TABLE schizophrenia.gene_clinvar ( 
	gene_symbol          varchar(10)  NOT NULL  ,
	clinvar_id           int UNSIGNED NOT NULL  ,
	CONSTRAINT idx_gene_clinvar PRIMARY KEY ( gene_symbol, clinvar_id )
 ) engine=InnoDB;

CREATE INDEX idx_gene_clinvar_gene ON schizophrenia.gene_clinvar ( gene_symbol );

CREATE INDEX idx_gene_clinvar_clinvar ON schizophrenia.gene_clinvar ( clinvar_id );

CREATE TABLE schizophrenia.gene_go ( 
	gene_symbol          varchar(10)  NOT NULL  ,
	go_id                int UNSIGNED NOT NULL  ,
	evidence_code        varchar(3)  NOT NULL  ,
	CONSTRAINT idx_gene_go PRIMARY KEY ( gene_symbol, go_id, evidence_code )
 ) engine=InnoDB;

CREATE INDEX idx_gene_go_gene ON schizophrenia.gene_go ( gene_symbol );

CREATE INDEX idx_gene_go_go ON schizophrenia.gene_go ( go_id );

ALTER TABLE schizophrenia.gene_clinvar ADD CONSTRAINT fk_gene_clinvar_gene FOREIGN KEY ( gene_symbol ) REFERENCES schizophrenia.genes( gene_symbol ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE schizophrenia.gene_clinvar ADD CONSTRAINT fk_gene_clinvar_clinvar FOREIGN KEY ( clinvar_id ) REFERENCES schizophrenia.clinvar( id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE schizophrenia.gene_go ADD CONSTRAINT fk_genes_go_genes FOREIGN KEY ( gene_symbol ) REFERENCES schizophrenia.genes( gene_symbol ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE schizophrenia.gene_go ADD CONSTRAINT fk_gene_go_go FOREIGN KEY ( go_id ) REFERENCES schizophrenia.go( go_id ) ON DELETE NO ACTION ON UPDATE NO ACTION;

ALTER TABLE schizophrenia.transcripts_proteins ADD CONSTRAINT fk_transcripts_proteins_genes FOREIGN KEY ( gene_symbol ) REFERENCES schizophrenia.genes( gene_symbol ) ON DELETE NO ACTION ON UPDATE NO ACTION;

