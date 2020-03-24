import requests
import re
from googlesearch import search
from bs4 import BeautifulSoup
import resume

'''
phrase = texto para buscar noticias
link = link da noticia do portal G1
q = % do texto que será feita o resumo
A função retorna sempre uma lista, onde o primeiro termo indica qual o tipo de retorno gerado
Tipo 0 = sem retorno da busca
Tipo 1 = página com a noticia
Tipo 2 = páginas de noticias
'''

#teste news(link='https://g1.globo.com/bemestar/coronavirus/noticia/2020/03/23/casos-de-coronavirus-no-brasil-em-23-de-marco.ghtml')
#função para buscar a materia no site
def news(phrase='',link='',q=0.3):
    #verifica se foi passado algum parametro
    if phrase == '' and link == '':
        return [0]

    #verifica se foi passado um link direto
    if link != '':
        news_link = link
    elif phrase != '':
        #faz a busca da frase no google e retorna o primeiro link
        for url in search('{} g1'.format(phrase),stop=1):
            news_link = url
            
            
    #verifica se é a pagina de uma noticia   
    if "/noticia/" in news_link and "globo" in news_link:
        #coleta url
        page = requests.get(news_link)
        #cria objeto bs4
        soup = BeautifulSoup(page.text, "html.parser")
        #retorna o titulo da materia
        title = soup.find(class_='content-head__title')
        #retorna o subtitulo da materia
        subtitle = soup.find(class_='content-head__subtitle')
        #retorna o texto da materia
        news_body = soup.find_all(class_='content-text__container')

        #cria um texto com toda máteria
        news_text = ''
        for p in news_body:
            news_text = news_text + '. ' + p.text
            
        #cria o resumo da materia
        news_resume = resume.short(news_text,q)

        #cria lista de retorno com o tipo 1: máteria
        return [1,title.text,subtitle.text,news_text,news_resume]
        
    #verifica se é uma pagia apenas visual
    elif "globo" in news_link and ("playlist" in news_link or "videos" in news_link):
        return [0]
    #verifica se é a pagina contendo as noticias  
    elif "globo" in news_link:
        #coleta url
        page = requests.get(news_link)
        #cria objeto bs4
        soup = BeautifulSoup(page.text, "html.parser")
        #retorna todas máterias da pagina
        body = soup.find(class_='bastian-page')
        body = body.find_all(class_='bastian-feed-item')
        news_title = []
        news_links = []
        news_resume = []
        for new in body:
            news_title.append(new.find(class_='feed-post-body-title gui-color-primary gui-color-hover').text)
            news_resume.append(new.find(class_='feed-post-body-resumo').text)
            news_links.append((new.find(class_='feed-post-link gui-color-primary gui-color-hover').get('href')))
        #cria lista de retorno com o tipo 2: pagina de noticia
        return  [2,news_title, news_resume, news_links]

        
        
        
        
    
    
