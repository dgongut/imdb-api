from flask import Flask, request, jsonify
from config import *
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)

@app.route('/api/search', methods=['GET'])
def search():
    headers = {"user-agent": USER_AGENT}
    query = request.args.get('query')
    if not query:
        msg = {"error": "The query parameter must contain the information to be searched for."}
        return jsonify(msg), STATUS_CODE_ERROR

    query = f'{query.replace("%20", " ")}'
    url = f'{URL_SEARCH_IMDB}{query}'
    print(f"URL: {url}")
    res = requests.get(url, headers=headers, timeout=10)

    elements = []
    response = []

    if res.status_code != 200:
        msg = {"error": f"imdb error: {res.status_code}"}
        return jsonify(msg), STATUS_CODE_ERROR
    else:
        # Búsqueda correcta, analizamos los resultados
        elements = web_scrapping_imdb_search_page(res.text)

    if not elements:
        msg = {"error": "Sin resultados"}
        return jsonify(msg), STATUS_CODE_NOT_FOUND

    for element in elements:
        try:
            filmCode = url_to_film_code(element[1])
        except:
            continue

        responseItem = {
            "id": filmCode,
            "api": f'/api/film?id={filmCode}',
            "title": element[0],
            "url": element[1],
            "year": element[2],
            "image": element[3]
        }
        response.append(responseItem)

    return jsonify(response), STATUS_CODE_OK

@app.route('/api/film', methods=['GET'])
def filmById():
    headers = {"user-agent": USER_AGENT}
    urlParameter = request.args.get('url')
    id = request.args.get('id')
    if urlParameter:
        id = url_to_film_code(urlParameter)

    if not id:
        msg = {"error": "The id or url parameter is required. Try /api/search endpoint to obtain the id."}
        return jsonify(msg), STATUS_CODE_ERROR

    url = f'{URL_FILM_PAGE_IMDB}{id}'
    res = requests.get(url, headers=headers, timeout=10)

    element = []
    response = []

    if res.status_code != 200:
        msg = {"error": f"imdb error: {res.status_code}"}
        return jsonify(msg), STATUS_CODE_ERROR
    else:
        # Búsqueda correcta, analizamos el resultado
        element = web_scrapping_imdb_main_page(res.text)

    response = {
        "id": id,
        "title": element[0],
        "url": element[1],
        "rating": element[2],
        "year": element[3],
        "image": element[4],
        "genre": element[5],
        "summary": element[6],
        "ratingCount": element[7],
        "duration": element[8]
    }

    return jsonify(response), STATUS_CODE_OK

def web_scrapping_imdb_search_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")
    imdbRawElements = soup.select("li.find-result-item")

    imdbElements = []

    noResults = soup.find('div', string=re.compile(r"No se han encontrado resultados para?"))
    if noResults:
        return imdbElements

    for filmElement in imdbRawElements:
        try:
            # Image
            img = filmElement.find("img")
            image = img["src"] if img else ""

            # URL y título
            a_tag = filmElement.find("a", href=True)
            title = a_tag.get_text(strip=True)
            url = re.sub(r"/\?ref_[^/]+", "", URL_IMDB_BASE.replace("/es-es", "") + a_tag["href"]) + "/"

            # Año
            year_span = filmElement.select_one("span.ipc-metadata-list-summary-item__li")
            year = year_span.get_text(strip=True)[:4] if year_span else ""

            imdbElements.append([title, url, year, image])
        except Exception as e:
            print("Error procesando un elemento:", e)

    return imdbElements

def web_scrapping_imdb_main_page(htmlText):
    soup = BeautifulSoup(htmlText, "html.parser")

    resumeSplit = None
    titleAndYearRating = None
    yearAndRating = None
    try:
        resume = soup.find("meta", property="og:title")["content"].strip()
        resumeSplit = resume.split(" | ")
        titleAndYearRating = resumeSplit[0].split(" (")
        yearAndRating = titleAndYearRating[1].split(" ⭐ ")
    except Exception as error:
        print("An error occurred:", error)
        print(resume)


    # Title
    title = None
    try:
        title = titleAndYearRating[0].strip()
    except:
        title = ""
    
    # URL
    allLinks = soup.find_all('a')
    url = None
    for link in allLinks:
        try:
            if '/title/tt' in link['href']:
                url = f"{URL_FILM_PAGE_IMDB}{url_to_film_code(link['href'])}/"
                break
        except:
            continue
    
    # Rating
    rating = None
    try:
        rating = yearAndRating[1].strip()
    except:
        rating = "--"

    # Image
    image = None
    try:
        image = soup.find("meta", property="og:image")["content"]
    except:
        image = ""

    # Original Title
    originalTitle = None
    try:
        originalTitle = soup.find('div', class_="sc-afe43def-3 EpHJp").get_text().strip().replace("Título original: ", "")
    except:
        originalTitle = ""
    
    # Year
    year = None
    try:
        year = yearAndRating[0].replace(")", "").strip()
    except:
        year = ""

    # Genre
    genre = None
    try:
        genre = resumeSplit[1].strip()
    except:
        genre = ""

    # Summary
    summary = None
    try:
        summary = soup.find("span", class_="sc-466bb6c-1 dRrIo").get_text()
    except:
        summary = ""

    # Rating count
    ratingCount = None
    try:
        ratingCount = soup.find(class_="sc-bde20123-3 bjjENQ").get_text()
    except:
        ratingCount = "0"

    # Duration
    duration = None
    try:
        duration = soup.find("meta", property="og:description")["content"].split(" | ")[0]
    except:
        duration = ""

    return [title, url, rating, year, image, genre, summary, ratingCount, duration]

def url_to_film_code(url):
    numeroPelicula = None
    url = url.replace("\"", "").replace("\n", "")
    if not url.endswith('/'):
        url = f'{url}/'
    numeroPelicula = re.search(r'/tt(\d+)/', url)
    if numeroPelicula:
        numeroPelicula = numeroPelicula.group(1)
        return numeroPelicula
    else:
        raise ValueError(f'No se encontró un número de película en el enlace: {url}')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22048)
