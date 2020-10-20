import dataset
import schedule

from requests_html import HTMLSession
from telegram import send_noticia
from time import sleep


db = dataset.connect("sqlite:///mydatabase.db")
table = db["noticias"]


session = HTMLSession()


main_url = "https://nei.ufrn.br"
noticias_path = "/acontecenei/noticias"
search_url = f"{main_url}{noticias_path}"
search_path = ".noticia-xxs-link"


def format_title(title):
    title_split = title.split("-")
    new_title = ""
    for text in title_split:
        print(text)
        new_title += text.capitalize() + " "
    return new_title


def find_noticias():
    r = session.get(search_url)
    noticias = r.html.find(search_path)
    for noticia in noticias:
        noticia_href = noticia.attrs["href"]
        noticia_id = int(noticia_href.split("/")[-1])
        noticia_url = f"{main_url}{noticia_href}"
        p = noticia.find("p")
        noticia_title = p[0].text
        if table.find_one(id=[noticia_id]) == None:
            print(noticia_url)
            table.insert(dict(id=noticia_id, url=noticia_url, title=noticia_title))
            send_noticia(noticia_title, noticia_url)


if __name__ == "__main__":
    schedule.every().minute().do(find_noticias)
    while True:
        schedule.run_peding()
        sleep(1)
