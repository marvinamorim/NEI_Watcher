from time import sleep

import dataset
import schedule
from requests_html import HTMLSession

from config import settings
from telegram import send_noticia

db = dataset.connect(settings.DATABASE_URL)
table = db[settings.NEWS]


def format_title(title):
    title_split = title.split("-")
    new_title = ""
    for text in title_split:
        new_title += text.capitalize() + " "
    return new_title


def find_noticias():
    session = HTMLSession()
    r = session.get(f'{settings.URL_MAIN}{settings.URL_PATH}')
    search_path = ".noticia-xxs-link"
    noticias = r.html.find(search_path)
    for noticia in noticias:
        noticia_href = noticia.attrs["href"]
        noticia_id = int(noticia_href.split("/")[-1])
        noticia_url = f"{settings.URL_MAIN}{noticia_href}"
        p = noticia.find("p")
        noticia_title = p[0].text
        if table.find_one(id=[noticia_id]) == None:
            print("Nova Noticia", noticia_url)
            table.insert(dict(id=noticia_id, url=noticia_url, title=noticia_title))
            send_noticia(noticia_title, noticia_url)


if __name__ == "__main__":
    print("Started main")
    find_noticias()
    schedule.every(5).minutes.do(find_noticias)
    while True:
        schedule.run_pending()
        sleep(1)
