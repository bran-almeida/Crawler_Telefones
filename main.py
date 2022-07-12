import requests, re, threading
from bs4 import BeautifulSoup as bs4


DOMINIO = "https://django-anuncios.solyd.com.br"
LINKS = []
PHONE_NUMBER = []


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


def get_phones():
    while True:
        try:
            announcement_link = LINKS.pop(0)
        except:
            return None


        response_announcement = site_request(announcement_link)

        if response_announcement:
            soup_announcement = parsing_html(response_announcement)
            if soup_announcement:
                phones = find_phones(soup_announcement)
                if phones:
                    for p in phones:
                        PHONE_NUMBER.append(p)
                        print(f"Telefone encontrado: ({p[0]}){p[1]}-{p[2]}")


def export_phones(phone):
    formated_phone = f"({phone[0]}) {phone[1]}-{phone[2]}\n"
    try:
        with open("Telefones.csv", "a") as file:
            file.write(formated_phone)

    except Exception as error:
        print("Erro ao salvar arquivo.")
        print(error)


if __name__ == "__main__":
    html = site_request(DOMINIO)
    if html:
        soup = parsing_html(html)
        if soup:
            LINKS = find_links(soup)


            THREADS = []
            for i in range(5):    
                t = threading.Thread(target=get_phones)
                THREADS.append(t)

            for t in THREADS:
                t.start()
            
            for t in THREADS:
                t.join()

            for p in PHONE_NUMBER:
                export_phones(p)
            