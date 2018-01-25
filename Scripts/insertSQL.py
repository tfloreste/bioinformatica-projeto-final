#!/usr/bin/python
# coding: utf-8
import mysql.connector

db='schizophrenia'
usr='root'
passwd ='bioinfo'


### Esse script contem funções para execução de querys no
### banco de dados do projeto.
###
### Ele serve de auxiliar para os scripts main.py e
### select.py

def execute_query(query, operation = 0):
	cnx = mysql.connector.connect(database = db, user = usr, password = passwd)
	cur = cnx.cursor()
	result = 0
	try:
		cur.execute(query)
		if (operation == 1):
			result = cur.fetchall()
	except mysql.connector.Error as err:
		print "Error {}".format(err)
	cnx.commit()
	cur.close()
	return result	

def insert_gene(gene_symbol, location):	
	query = "INSERT INTO genes (gene_symbol, location) values ('"+gene_symbol+"','"+location+"');"
	execute_query(query)	

def insert_transcript_protein(mrna, prot, size_mrna, size_prot, gene):
	query = "INSERT INTO transcripts_proteins (accession_mrna, accession_protein, size_mrna, size_protein, gene_symbol) values ('" +mrna+ "','" +prot+ "'," +size_mrna+ "," +size_prot+ ",'" +gene+ "');"
	execute_query(query)

def insert_go(go_id, category):
	query = "INSERT INTO go (go_id, category) values (" +go_id+ ",'" +category+ "');"
	execute_query(query)

def insert_clinvar(c_id, significance, v_type):
	query = "INSERT INTO clinvar (id, clinical_significance, variant_type) values (" +c_id+ ",'" +significance+ "' , '" +v_type+ "');"
	execute_query(query)

def insert_gene_go(gene_symbol, go_id, evidence):
	query = "INSERT INTO gene_go (gene_symbol, go_id, evidence_code) values ('" +gene_symbol+ "'," +go_id+ ",'" +evidence+ "');"
	execute_query(query)	

def insert_gene_clinvar(gene_symbol, clinvar_id):
	query = "INSERT INTO gene_clinvar (gene_symbol, clinvar_id) values ('" +gene_symbol+ "'," +clinvar_id+ ");"
	execute_query(query)

