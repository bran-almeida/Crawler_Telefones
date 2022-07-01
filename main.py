import requests
from bs4 import BeautifulSoup as bs4
URL = "https://django-anuncios.solyd.com.br"


def site_request(url):
    """Faz uma requisição a URL especificada e retorna seu HTML em formato de texto."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            site_html = response.text
            return site_html
        else: 
            print(f"Erro {response.status_code} na requisição")
    except Exception as error:
        print("Erro na requisição")
        print(error)


def parsing_html(html):
    """Realiza o pasing de um HTML"""
    try:
        soup = bs4(html, 'html.parser')
        return soup
    except Exception as error: 
        print("Erro ao fazer o parsing.")
        print(error)


def search_links(soup): 
    """Busca links dentro do site alvo"""
    try:
        site_links = []
        card_root = soup.find('div', class_="ui three doubling link cards")
        card_child = card_root.find_all('a', class_="card")
        for card in card_child: 
            site_links.append(URL+card["href"])
        return site_links
    except Exception as error: 
        print("Erro durante busca de links.")
        print(error)

        
if  __name__ == "__main__":
    html = site_request(URL)
    soup = parsing_html(html)
    links = search_links(soup)
    for link in links: 
        print(link)
    



