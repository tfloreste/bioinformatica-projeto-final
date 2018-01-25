# DESCRIÇÃO DAS PASTAS E ARQUIVOS

### PASTA "Scripts"
***
**Arquivo**: insertSQL.py
Script python contendo funções para execução de querys no banco de dados Schizophrenia, em especial algumas funções para inserir os dados no banco de dados.
**IMPORTANTE**: Pode ser necessário mudar os valores das variáveis "usr" e "passwd" presentes neste arquivo dependendo do usuário e senha configurados no MySQL.

**Arquivo**: main.py
Script python para coletar as informações dos genes e salvar essas informações no banco de dados Schizophrenia. Esse script usa as funções presentes no arquivo insertSQL.py.

**Arquivo**: select.py
Realiza os "SELECTs" no banco de dados Schizophrenia e imprime os resultados. O objetivo desse script é responder as questões presentes no arquivo "Projeto.pdf" presente no Tidia.
***  
&nbsp;

### PASTA "Scripts/data"
***
**Arquivo**: schizophrenia_genes
Contém os geneSymbols dos 10 genes relacionados à esquizofrênia selecionados para o trabalho. As informações desses genes serão coletadas e inseridas no banco de dados pelo script "main.py".
	
**Arquivo**: gene2go
Arquivo com informações de Gene Ontology obtido a partir [deste link](https://ftp.ncbi.nlm.nih.gov/gene/DATA/gene2go.gz). Este arquivo foi atualizado pela última vez em 04/05/2017.
***
&nbsp;

### PASTA "Scripts/sql"
***
**Arquivo**: db_schizophrenia.sql
Código SQL para criação do banco de dados Schizophrenia, onde as informações coletadas dos genes serão armazenadas.
***
&nbsp;

### PASTA "Modelo-DbSchema"
***
**Arquivo**: db_projeto_final.dbs
Arquivo do DBSchema com a modelo do banco de dados.

**Arquivo**: db_projeto_final.png
Imagem representando o Modelo Entidade Relacionamento do Banco de Dados desenvolvido para o projeto.
***
