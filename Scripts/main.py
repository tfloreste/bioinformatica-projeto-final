#!/usr/bin/python
# coding: utf-8
import re
from Bio import Entrez
from insertSQL import *

### Esse script coleta as informações associadas a cada gene presente 
### no arquivo /data/schizophrenia_genes e as salva no banco de dados
###
### As funções que fazem a inserção e execução de querys no banco de dados
### estão presentes no arquivo insertSQL.py


# Recebe o geneSymbol de um gene e retorna o ID do gene
def getGeneID(gene_symbol):
	term = "Human[Orgn] AND " + gene_symbol + "[Gene Name]"
	handle = Entrez.esearch(db = "gene", term = term)
	return Entrez.read(handle)["IdList"][0]

# Recebe o ID do gene e retorna a localização dele
def getGeneLocation(gene_id):
	handle = Entrez.efetch(db = "gene", id = gi, rettype = "gb", retmode = "txt")
	location = re.search("Location:\s*(.+)", handle.read(), re.I)
	return location.group(1)


# Recebe um gene ID como parâmetro e retorna os Accessions e tamanhos dos mRNAs e proteínas codificados pelo gene
def getMrnaAndProteinInfo(gene_id):
	handle = Entrez.efetch(db='gene', id= gene_id, rettype='gene_table', retmode='txt')
	mrna_infos = list()
	protein_infos = list()
	for line in handle:
		mrna = re.search('((?:NM|XM)_\d+(?:.\d+)).*?length:\s*(\d+)', line, re.I)
		protein = re.search('((?:NP|XP)_\d+(?:.\d+)).*?length:\s*(\d+)', line, re.I)
		if mrna:
			mrna_infos.append(mrna)
		if protein:
			protein_infos.append(protein)
	return (mrna_infos, protein_infos)

# Retorna uma lista com informações de Gene Ontology de um gene usando o arquivo gene2go
# Cada item da lista é uma instância de um MatchObject que contem os seguintes grupos:
# .group(1) corresponde ao GO ID
# .group(2) corresponde ao GO Evidence Code
# .group(3) corresponde à categoria
def getGOInfo(gene_id, gene2go):
	gene2go.seek(0)
	go_infos = list()
	for line in gene2go:
		go_regex = "\d+\t" + gene_id + "\tGO:(\d+)\t(\w+)(?:\t.*\t)(\w+)"
		go_info = re.search(go_regex, line)
		if go_info:
			go_infos.append(go_info)
	return go_infos

# Retorna até 20 Variation IDs relacionados com o geneSymbol recebido como parâmetro
def getClinvarIds(gene_symbol):
	term = gene_symbol + "[Gene Name]"
	handle = Entrez.esearch(db = "clinvar", term = term)
	record = Entrez.read(handle)
	return record['IdList']	

# Recebe uma lista com Variation IDs e retorna duas listas contendo informacoes 
#associadas a cada ID
# A primeira lista contem informações das significâncias clínicas 
# A segunda lista contem inforções do tipo de variante
def getClinvarInfo(clinvar_ids):
	significances = list()
	variant_types = list()
	for clinvar_id in clinvar_ids:
		handle = Entrez.esummary(db = 'clinvar', id = clinvar_id)
		record = Entrez.read(handle)
		significance = record['DocumentSummarySet']['DocumentSummary'][0]['clinical_significance']['description']
		variant_type = record['DocumentSummarySet']['DocumentSummary'][0]['variation_set'][0]['variant_type']
		significances.append(significance)
		variant_types.append(variant_type)
	return (significances, variant_types)		


Entrez.email = 'thiago.floreste@aluno.ufabc.edu.br' 
genes = open('data/schizophrenia_genes', 'r') 	
gene2go = open('data/gene2go', 'r')		

for gene_symbol in genes:
	gene_symbol = re.sub('[\s\n]', '', gene_symbol) 

	print "Coletando informações do gene " + gene_symbol
	gi = getGeneID(gene_symbol)		
	location = getGeneLocation(gi)		
	(mrnas, proteins) = getMrnaAndProteinInfo(gi)	
	gos = getGOInfo(gi, gene2go)			
	clinvar_ids = getClinvarIds(gene_symbol)	
	(clinical_significances, variant_types) = getClinvarInfo(clinvar_ids)	

	print "Salvando informações no banco de dados\n"
	insert_gene(gene_symbol, location)
	for (transcript, protein) in zip(mrnas, proteins):
		mrna_accession = transcript.group(1)
		mrna_size = transcript.group(2)
		protein_accession = protein.group(1)
		protein_size = protein.group(2)
		insert_transcript_protein(mrna_accession, protein_accession, mrna_size, protein_size, gene_symbol)
	
	for go in gos:
		go_id = go.group(1)
		evidence = go.group(2)
		category = go.group(3)	
		query = "SELECT COUNT(go_id) FROM go WHERE go_id = " + go_id 
		count = execute_query(query, 1)
		if(count[0][0] == 0):
			insert_go(go_id, category)
		insert_gene_go(gene_symbol, go_id, evidence)
			
	
	for (clinvar_id, significance, variant_type) in zip(clinvar_ids, clinical_significances, variant_types):
		query = "SELECT COUNT(id) FROM clinvar WHERE id = " + clinvar_id
		count = execute_query(query, 1)
		if(count[0][0] == 0):
			insert_clinvar(clinvar_id, significance, variant_type)
		insert_gene_clinvar(gene_symbol, clinvar_id)	

genes.close()
gene2go.close()
