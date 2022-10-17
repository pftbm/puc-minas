import urllib.request
import time
import random
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import csv
import datetime
import os.path as path
import unicodedata
import html as html_us
from os import rename, listdir




def salvar_dado(file_name, file_name_creation, url_existent_list, data_base):

	if len(url_existent_list) > 0:
		with open(file_name, 'a') as f:
			writer = csv.writer(f, dialect = 'excel', quoting=csv.QUOTE_ALL, delimiter = ';', lineterminator = '\n')
			for data in data_base:
				try:
					writer.writerow(data)
					print("ok - new data")
				except Exception as e:
					print("zebra!!!")
					print(data)
					print(e)
		f.close()

	else:
		with open(file_name_creation, 'wt') as csv_file:
			writer = csv.writer(csv_file, dialect = 'excel', quoting=csv.QUOTE_ALL, delimiter = ';', lineterminator = '\n')
			writer.writerow(["data", "publicado_ha", "cidade", "endereco", "bairro", "titulo_resumo", "titulo", "sala_comercial", "descricao", "área total", "área útil", "quartos", "banheiros", "vagas", "suítes", "idade do imóvel", "condominio", "brinquedoteca", "campo", "churrasqueira", "espaço gourmet", "sala de ginástica", "frente mar", "central de gás", "gás encanado", "mobiliado", "nascente", "piscina", "playground", "salão de festas", "salão de jogos", 
				"sauna", "varanda gourmet", "andares", "anunciante", "cod_imovel_anunciante", "fone_anunciante", "email_anunciante", "preco", "url"])

			for data in data_base:
				try:
					writer.writerow(data)
					print("ok")

				except Exception as e:
					print("zebra!!!")
					print(data)
					print(e)

		csv_file.close()

	



def get_andares(descricao):

	descricao = descricao.lower()

	index = descricao.find("andares")

	if index == -1:		
		andares = "NA"

	else:
		sub = descricao[index-5:index]
		andares = ""

		for i in sub:
			if i.isdigit():
				andares = andares + i

		if andares == "":
			andares = "NA"


	return andares



def get_header():
	header = {'user-agent': 'Mozilla/5.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
        'Host': 'www.imovelweb.com.br',
        'Sec-Fetch-Dest': 'document',
        'Upgrade-Insecure-Requests':'1',
        'Sec-Fetch-Mode': 'navigate'}

	header2 = {'user-agent': 'Mozilla/5.0'}

	return header2



def only_digits(text):
	return(re.sub("[^0-9]", "", text))


def is_sala_comercial(text):
	text = text.upper()
	sala = "não"
	if text.find("SALA") != -1:
		sala = "sim"

	return(sala)



def remove_control_characters(s):
	s = s.replace('\n', " ")
	return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")


def get_file_name(file_name_start):
    file_list = listdir('.')
    file_name_ok = ""
    for file_name in file_list:
        if file_name.startswith(file_name_start):
            file_name_ok = file_name

    return file_name_ok


def rename_file(file_name_start):

	file_name_ok = get_file_name(file_name_start)
	slice_position = file_name_ok.find("-atualizacao-")

	if slice_position != -1:
		file_base_name = file_name_ok[:slice_position]
	else:
		file_base_name = file_name_ok[:file_name_ok.find(".csv")]

	today = datetime.date.today().strftime("%d-%m-%Y")
	rename(file_name_ok, file_base_name+"-atualizacao-"+today+".csv")




def get_links(url_inicial, quant):

	pages = quant / 20
	if(pages - int(pages)) > 0:
		pages = int(pages) + 1

	pages = int(pages)

	print("pages: "+str(pages))

	req = Request(url_inicial, headers= get_header())#{'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req)
		

	soup = BeautifulSoup(html.read(), "html.parser")

	index = url_inicial.find(".html")
	links = list()
	print("pages: ", pages)
	cont_novo = 1
	aux = 1
	repetidos = 0

	pages_lim = 1

	if(pages > 2):
		pages_lim = 2
#		pages = 1
		
	

	#for i in range(pages):
	pages_list = random.sample(range(1, pages+1), pages)
	#pages_list = random.sample(range(1, 5), 4)

	for i in range(pages_lim):

		page = pages_list.pop()
		#page = i + 1	
		if(page == 1):
			url_page = url_inicial
		else:
			url_page = url_inicial[:index]+"-pagina-"+str(page)+url_inicial[index:]	

		print(url_page)					

		req = Request(url_page, headers= get_header())#{'User-Agent': 'Mozilla/5.0'})
		html = urlopen(req)

		print(html)

		soup = BeautifulSoup(html.read(), "html.parser")
		#all_links = soup.findAll("h2", {"class":"postingCardTitle"})
		all_links = soup.findAll("h2")

		print("all_links len: ", len(all_links))

		time.sleep(random.randint(1, 3))
		
		for item in all_links:			
			new_link = "https://www.imovelweb.com.br"+item.find("a").attrs['href']
			if new_link not in links:
				links.append(new_link)		
				#print("novo!", end = '')
				print("novo!")
			else:
				print("repetido!")
				
	

	return links



def publicado(soup):

	try:

#		dias = soup.find("h5",{"class":"section-date"}).get_text().strip()

		dias = soup.findAll("script", attrs={'type': None, 'src': None})[0].get_text().strip()
		inicio = dias.find("Publicado")
		fim = dias[inicio:].find("const")
		dias = dias[inicio: inicio+fim].strip()


		if(dias.find("Publicado hoje") != -1):
			dias = "0"		
		elif(dias.find("Publicado há mais de 1 ano") != -1):
			dias = "MAIS DE UM ANO"
		else:
			dias = only_digits(dias)

	except Exception as e:
		print("EXCEÇÃO EM DIAS")
		print(e)
		dias = "DADO COM ERRO - VERIFICAR"
	
	
	return dias


def get_icon_features(soup):

	list_soup = soup.findAll("li", {"class":"icon-feature"})
	#d = {"Total":"NA","Útil":"NA", "Quarto":"NA", "Quartos":"NA", "Banheiro":"NA", "Banheiros":"NA", "Vaga":"NA", "Vagas":"NA", "Suíte":"NA", "Suítes":"NA", "Idade do imóvel":"NA"}
	d = {"Total":"NA","Útil":"NA", "Quarto":"NA", "Banheiro":"NA", "Vaga":"NA", "Suíte":"NA", "Idade":"NA"}

	for item in list_soup:
		i = item.get_text().strip().upper()
		for key in d.keys():
			if key.upper() in i:
				d[key] = re.sub("[^0-9]", "", i) #filter(str.isdigit, i)
				break

	l = list(d.values())
	return(l)
		

#quebrado - outras informações
def get_fone_email(url):
	
	url = "https://www.imovelweb.com.br/propriedades/imprimir/"+url[42:]
	req = Request(url, headers= get_header())#{'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req)
	soup = BeautifulSoup(html.read(), "html.parser")

	list_aux = soup.find("div", {"class":"ficha-print-box"}).findAll("strong")
	anunciante = list_aux[0].get_text().strip()
#	fone_anunciante = list_aux[1].get_text().strip()
#	email_anunciante = list_aux[2].get_text().strip()

	#return([fone_anunciante, email_anunciante])
	return(anunciante)


def get_dicotomicas_in_descricao(descricao, brinquedoteca, campo, churrasqueira, espaco_gourmet, sala_ginastica, frente_mar, central_gas, gas_encanado, mobiliado, 
	nascente, piscina, playground, salao_festa, salao_jogos, sauna, varanda_gourmet, andares):

	if(brinquedoteca == 0):
		if("brinquedoteca" in descricao):
			brinquedoteca = 1

	if(campo == 0):
		if("campo" or "campinho") in descricao:
			campo = 1

	if(churrasqueira == 0):
		if("churrasqueira" in descricao):
			churrasqueira = 1

	if(espaco_gourmet == 0):
		if("espaço gourmet" or "espaco gourmet") in descricao:
			espaco_gourmet = 1

	if(sala_ginastica == 0):
		if("sala de ginástica" or "sala ginástica" or "salão de ginástica" or "academia") in descricao:
			sala_ginastica = 1

	if(frente_mar == 0):
		if("frente para o mar" in descricao):
			frente_mar = 1

	if central_gas == 0:
		if "central de gás" in descricao:
			central_gas = 1

	if gas_encanado == 0:
		if("gás encanado" in descricao):
			gas_encanado = 1

	if mobiliado == 0:
		if "mobiliado" in descricao:
			mobiliado = 1

	if nascente == 0:
		if "nascente" in descricao:
			nascente = 1

	if piscina == 0:
		if "piscina" in descricao:
			piscina = 1

	if playground == 0:
		if "playground" in descricao:
			playground = 1

	if salao_festa == 0:
		if "salão de festa" in descricao:
			salao_festa = 1

	if salao_jogos == 0:
		if ("salão de jogos" or "sala de jogos") in descricao:
			salao_jogos = 1

	if sauna == 0:
		if "sauna" in descricao:
			sauna = 1

	if varanda_gourmet == 0:
		if "varanda gourmet" in descricao:
			varanda_gourmet = 1


	return [brinquedoteca, campo, churrasqueira, espaco_gourmet, sala_ginastica, frente_mar, central_gas, gas_encanado, mobiliado, nascente, piscina, playground, salao_festa, salao_jogos, sauna, varanda_gourmet, andares]
	



def get_dicotomicas(dic_list, descricao):

	descricao = descricao.lower()

	brinquedoteca = campo = churrasqueira = espaco_gourmet = sala_ginastica = frente_mar = central_gas = gas_encanado = 0
	mobiliado = nascente = piscina = playground = salao_festa = salao_jogos = sauna = varanda_gourmet = 0
	andares = "NA"

	for item in dic_list:
		if(item == "Brinquedoteca"):
			brinquedoteca = 1

		elif(item == "Campo de futebol"):
			campo = 1

		elif(item == "Churrasqueira"):
			churrasqueira = 1

		elif(item == "Espaço Gourmet"):
			espaco_gourmet = 1

		elif(item == "Fitness/Sala de Ginástica"):
			sala_ginastica = 1

		elif(item == "Frente para o mar"):
			frente_mar = 1

		elif(item == "Central de gás"):
			central_gas = 1

		elif(item == "Gás encanado"):
			gas_encanado = 1

		elif(item == "Mobiliado"):
			mobiliado = 1

		elif(item == "Posição do Sol: Nascente"):
			nascente = 1

		elif(item == "Piscina"):
			piscina = 1

		elif(item == "Playground"):
			playground = 1

		elif(item == "Salão de festas"):
			salao_festa = 1

		elif(item == "Salão de Jogos"):
			salao_jogos = 1

		elif(item == "Sauna"):
			sauna = 1

		elif(item == "Varanda Gourmet"):
			varanda_gourmet = 1

		elif("Andares:" in item):
			andares = item.replace("Andares: ", "")


	list_result = get_dicotomicas_in_descricao(descricao, brinquedoteca, campo, churrasqueira, espaco_gourmet, sala_ginastica, frente_mar, central_gas, gas_encanado, mobiliado, nascente, piscina, playground, salao_festa, salao_jogos, sauna, varanda_gourmet, andares)


	return(list_result)





def get_data_from_link(url, cidade):

	req = Request(url, headers=get_header())#{'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req)
	

	#soup = BeautifulSoup(html.read(), "html.parser")
	soup = BeautifulSoup(html.read().decode('utf-8', 'ignore'), "html.parser")

#	data_attr = soup.findAll("ul", {"class":"section-bullets"})

	
	time.sleep(random.randint(2, 4))

	new = ""
	new_list = list()
#	for data in data_attr:		
#		new = data.li.get_text().strip()
#		new_list.append(new)
#		print("item prédio: ", new)
	

	#print(new_list)
	publicado_ha = publicado(soup)	
	cidade = cidade
	try:
		#endereco - OK
		endereco = soup.find("h2",{"class":"title-location"}).get_text().strip()
		endereco = endereco[:endereco.find("Ver no mapa")]
	except Exception as e:
		print(e)
		endereco = "NA"
	#bairro - ok
	bairro = soup.findAll("span", {"property":"name"})[5].get_text().strip()

	try:
		#titulo resumo - ok
		titulo_resumo = soup.find("h2",{"class":"title-type-sup"}).get_text().strip()	
	except Exception as e:
		titulo_resumo = "NA"
	

	#titulo = soup.find("h1").get_text().strip()
	#titulo - OK
	titulo = soup.find("div",{"class":"section-title"}).get_text().strip()

	sala_comercial = is_sala_comercial(titulo)
	#descricao - OK
	descricao = soup.find("div",{"id":"reactDescription"}).get_text().strip()

	#list_icon_features - ok
	list_icon_features = get_icon_features(soup)

	endereco = remove_control_characters(endereco)
	endereco = endereco.replace("\u2013", "-")
	endereco = endereco.replace("\u0155", "r")
	titulo_resumo = remove_control_characters(titulo_resumo)
	titulo = remove_control_characters(titulo)
	titulo = titulo.replace("\u2013", "-")
	titulo = titulo.replace("\u201d", "'")
	descricao = remove_control_characters(descricao)
	descricao = descricao.replace("\u2013", "-")
	descricao = descricao.replace("\u2019", "'")
	descricao = descricao.replace("\u2022", "*")
	descricao = descricao.replace("\u201c", "*")
	descricao = descricao.replace("\u201d", "*")
	descricao = descricao.replace("\u0155", "r")


	try:
		#pode haver IPTU também - verificar novo atributo
		condominio = soup.find("div", {"class":"block-expensas block-row"}).find("span").get_text().strip()
		condominio = condominio.replace("R$ ", "")
	except Exception as e:
		condominio = "NA"
	

	dicotomicas = get_dicotomicas(new_list, descricao)
	andares = dicotomicas.pop()
	
	if andares == "NA":
		andares = get_andares(descricao)


	#anunciante = soup.find("div", {"class":"column-left"}).find("a").attrs['title']
	anunciante = get_fone_email(url)
		
	cod_imovel_anunciante = "quebrado - script" #soup.find("span", {"class":"publisher-code"}).get_text().strip()
#	cod_imovel_anunciante = cod_imovel_anunciante.replace("Código do anunciante: ", "")
#	cod_imovel_anunciante = cod_imovel_anunciante.replace("\u2013", "-")

#	fone_email = get_fone_email(url)
	fone_anunciante = "quebrado" #fone_email[0]
	email_anunciante = "quebrado" #fone_email[1] #protected
	try:
		preco = soup.find("div", {"class":"price-items"}).get_text().strip()
		preco = preco.replace("R$ ", "")
	except Exception as e:
		preco = "NA"
	
	print("\n")
	print("######### PRÓXIMO ######################################################")
	print("publicado há (dias):", publicado_ha)
	print("cidade: ", cidade)
	print("endereço: ", endereco)
	print("bairro: ", bairro)
	print("título resumo: ", titulo_resumo)
	print("título: ", titulo)
	#print("descrição: ", descricao)
	print("list icon features: ", list_icon_features)
	print("condomínio: ", condominio)
	print("Andares: ", andares)
	print("lista dicot.: ", new_list)
	print("dicotômicas: ", dicotomicas)
	print("anunciante: ", anunciante)
	print("cód. imóvel anunciante: ", cod_imovel_anunciante)
	print("telefone: ", fone_anunciante)	
	print("preço: ", preco)

	time.sleep(1)
	
#	return new_list

#	usar essa estrutura para montar o lista abaixo: [1,2,3]+[99,88,77]+[0,-1,-2] 

	list_result = [publicado_ha, cidade, endereco, bairro, titulo_resumo, titulo, sala_comercial, descricao] + list_icon_features + [condominio]+ dicotomicas +[andares] + [anunciante, cod_imovel_anunciante, fone_anunciante, email_anunciante, preco, url]	

	return list_result





def run(tipo_imovel, tipo_negocio, cidade, estado):	

	order = "-ordem-publicado-maior"
	by_order = False
	
	if by_order:
		url_inicial = "https://www.imovelweb.com.br/"+tipo_imovel+"-"+tipo_negocio+"-"+cidade+"-"+estado+order+".html"
	else:
		#url_inicial = "https://www.imovelweb.com.br/"+tipo_imovel+"-"+tipo_negocio+"-"+cidade+"-"+estado+".html"
		url_inicial = "https://www.imovelweb.com.br/"+tipo_imovel+"-"+tipo_negocio+"-"+cidade+".html"



	req = Request(url_inicial, headers=get_header())#{'User-Agent': 'Mozilla/5.0'})
	html = urlopen(req)

	print(html)
	print("PASSOU ATÉ AQUI.")
	
	soup = BeautifulSoup(html.read(), "html.parser")
	
	#quant = soup.find("h1", {"class":"list-result-title"}).get_text().strip()
	#quant = quant.split(" ")[0]
	#quant = int(quant.replace(".", ""))
	quant = 3772
	print("quantidade de dados: ", quant)
	links = get_links(url_inicial, quant)

	print("comprimento links: ", len(links))

	
	
	file_name_creation = tipo_imovel+"-"+"imovelweb-"+cidade+"-PE"+".csv"
	file_name_start = tipo_imovel+"-"+"imovelweb-"+cidade+"-PE"
	file_name = get_file_name(file_name_start)
	

	url_existent_list = list()

	if path.isfile(file_name):
		with open(file_name) as f:
			reader = csv.reader(f, delimiter = ';')
			for row in reader:
				url_existent_list.append(row[-1])

		f.close()

	data_base = []
	cont = 0
	today = datetime.date.today().strftime("%d/%m/%y")
	
	for link in links:
		
		if link not in url_existent_list:

			data = get_data_from_link(link, cidade)
			data.insert(0, today)                        

			if(data[-1] != None):
				data_base.append(data)
				print("novo dado obtido!")
			#	salvar_dado(file_name, file_name_creation, url_existent_list, data)
				print(cont)
				cont = cont + 1
				if cont == 10:
					break

    

	if len(data_base) == 0:
	#if cont == 0:
		print("Nenhum novo dado encontrado.")


	
	if len(url_existent_list) > 0:
		with open(file_name, 'a') as f:
			writer = csv.writer(f, dialect = 'excel', quoting=csv.QUOTE_ALL, delimiter = ';', lineterminator = '\n')
			for data in data_base:
				try:
					writer.writerow(data)
					print("ok - new data")
				except Exception as e:
					print("zebra!!!")
					print(data)
					print(e)
		f.close()

	else:
		with open(file_name_creation, 'wt') as csv_file:
			writer = csv.writer(csv_file, dialect = 'excel', quoting=csv.QUOTE_ALL, delimiter = ';', lineterminator = '\n')
			writer.writerow(["data", "publicado_ha", "cidade", "endereco", "bairro", "titulo_resumo", "titulo", "sala_comercial", "descricao", "área total", "área útil", "quartos", "banheiros", "vagas", "suítes", "idade do imóvel", "condominio", "brinquedoteca", "campo", "churrasqueira", "espaço gourmet", "sala de ginástica", "frente mar", "central de gás", "gás encanado", "mobiliado", "nascente", "piscina", "playground", "salão de festas", "salão de jogos", 
				"sauna", "varanda gourmet", "andares", "anunciante", "cod_imovel_anunciante", "fone_anunciante", "email_anunciante", "preco", "url"])

			for data in data_base:
				try:
					writer.writerow(data)
					print("ok")

				except Exception as e:
					print("zebra!!!")
					print(data)
					print(e)

		csv_file.close()

	rename_file(file_name_start)









#tipos_imovel = {'apartamentos':1}
tipos_imovel = {'comerciais':1}

tipos_negocio = {'venda': 1}

#bairros = {'gruta-de-lourdes', 'barro-duro-maceio', 'pitanguinha', 'feitosa-maceio', 'santo-amaro-maceio', 'canaa-maceio', 'farol-maceio', 'bom-parto',
#'levada', 'ponta-grossa-maceio', 'vergel-do-lago', 'cha-de-bebedouro', 'cha-da-jaqueira', 'petropolis-maceio', 'santa-amelia-maceio',
#'fernao-velho', 'jacintinho', 'tabuleiro-do-martins', 'santa-lucia-maceio'}

#bairros = {"pitanguinha"}

#for tipo_imovel in tipos_imovel:
#    for tipo_negocio in tipos_negocio:
#    	run(tipo_imovel, tipo_negocio, "recife", "pe")

            
runs = 40
for i in range(runs):
	print("\n")
	print("############----------- EXECUÇÃO: "+str(i)+" --------------############################")
	#run('comerciais', 'venda', "recife", "pe")
	run('apartamentos', 'venda', "boa-viagem-recife", "pe")


