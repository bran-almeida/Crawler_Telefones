import requests, re
from bs4 import BeautifulSoup as bs4

DOMINIO = "https://django-anuncios.solyd.com.br"


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


def find_links(soup):
    """Busca links dentro do site alvo"""
    try:
        site_links = []
        card_root = soup.find('div', class_="ui three doubling link cards")
        card_child = card_root.find_all('a', class_="card")
        for card in card_child: 
            site_links.append(DOMINIO+card["href"])
        return site_links
    except Exception as error: 
        print("Erro durante busca de links.")
        print(error)


def find_phones(soup):
    try:
        announcement = soup.find_all("div", class_="sixteen wide column")[2].p.get_text().strip()
    except:
        print("Erro na requisição.")
        return None
    
    phones = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", announcement)
    if phones:
        return phones

if __name__ == "__main__":
    html = site_request(DOMINIO)
    if html:
        soup = parsing_html(html)
        if soup:
            links = find_links(soup)
            for link in links:
                announcement = site_request(link)
                if announcement:
                    soup_announcement = parsing_html(announcement)
                    if soup_announcement: 
                        phones = find_phones(soup_announcement)
                        if phones:
                            print(phones)