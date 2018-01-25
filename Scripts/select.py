#!/usr/bin/python
# coding: utf-8
from insertSQL import *

### Esse script realiza uma série de SELECTs no banco de dados 
### e imprime os resultados. 
###
### Os SELECTs foram feitos com base nas perguntas presentes no
### arquivo 'Projeto.pdf' do Tidia

query = "SELECT gene_symbol FROM genes"
genes = execute_query(query, 1)
for gene in genes:
	gene_symbol = gene[0]
	print "Gene Symbol: " + gene_symbol
	
	print ""

	query = "SELECT accession_mrna FROM transcripts_proteins WHERE gene_symbol = '" +gene_symbol + "'"
	transcripts = execute_query(query, 1)
	print "Transcritos:"
	for transcript in transcripts:
		print transcript[0]
	
	print ""

	query = "SELECT accession_protein, size_protein FROM transcripts_proteins WHERE gene_symbol = '" +gene_symbol+ "'"
	proteins = execute_query(query, 1)
	print "Proteínas \t Tamanhos"
	for protein in proteins:
		print protein[0] + " \t " + str(protein[1])

	print""

	query = "SELECT A.clinvar_id, B.variant_type FROM gene_clinvar A, clinvar B WHERE A.clinvar_id = B.id AND A.gene_symbol = '" +gene_symbol+ "'"
	variants = execute_query(query, 1)
	print "Variantes \t Tipo"
	for variant in variants:
		print str(variant[0]) + " \t " + variant[1]
	
	print "\n\n"
	
	
