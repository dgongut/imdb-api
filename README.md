# imdb-api
API REST no oficial de IMDb en castellano. Desarrollada desde cero en python.

Puedes encontrar el codigo dockerizado en [DockerHub](https://hub.docker.com/r/dgongut/imdb-api)

## Introducción

Esta es una API REST que utiliza WEB SCRAPING tanto para hacer búsquedas como para extraer información de películas y
series de [IMDb](https://www.imdb.com/).

Aún no se encuentra en una versión estable por lo que pueden ocurrir errores.

Está preparada tanto para la ejecución en local, como para crear una imagen en docker.

## API-REST

| Método | API         | Parámetros                                                                   | Descripción                                               |
| ------ | ----------- | ---------------------------------------------------------------------------- | --------------------------------------------------------- |
| GET    | /api/search | `query=${patrón a buscar}` | Busca películas y series por título |
| GET    | /api/film   | `id=${id}`                                             | Obtiene datos de una película o serie mediante un ID      |
| GET   | /api/film   | `url="https://www.filmaffinity.com/es/film819745.html"` | Obtiene datos de una película o serie mediante una URL    |

## Ejemplos de uso

### Búsqueda de películas cuyo título coincida con el string de búsqueda introducido

#### Ejemplo 1

GET
[http://localhost:22048/api/search?query=lo%20que%20el%20viento%20se%20llevo](http://localhost:22048/api/search?query=lo%20que%20el%20viento%20se%20llevo)

(Ejemplo recortado con fines demostrativos)

```json
[
   {
      "api": "/api/film?id=0169364",
      "id": "0169364",
      "image": "https://m.media-amazon.com/images/M/MV5BMmI3NjNhZTctMmY0Yy00OGI3LTk4MjQtYjRjMTRjZGRkMTMxXkEyXkFqcGdeQXVyNjgxMTU1ODU@._V1_QL75_UY74_CR2,0,50,74_.jpg",
      "title": "El viento se llevó lo que",
      "url": "https://www.imdb.com/title/tt0169364/",
      "year": "1998"
   },
   {
      "api": "/api/film?id=0151373",
      "id": "0151373",
      "image": "https://m.media-amazon.com/images/M/MV5BZTY4YTFiNzEtMmMyMy00MWFlLWE3YjEtZDUyODMzMTM3YzFmXkEyXkFqcGdeQXVyMjU1NjY2Mw@@._V1_QL75_UY74_CR1,0,50,74_.jpg",
      "title": "Lo que el viento se llevó",
      "url": "https://www.imdb.com/title/tt0151373/",
      "year": "1980"
   },
   {
      "api": "/api/film?id=0082808",
      "id": "0082808",
      "image": "https://m.media-amazon.com/images/M/MV5BZTY4YTFiNzEtMmMyMy00MWFlLWE3YjEtZDUyODMzMTM3YzFmXkEyXkFqcGdeQXVyMjU1NjY2Mw@@._V1_QL75_UY74_CR1,0,50,74_.jpg",
      "title": "Ni se lo llevó el viento, ni puñetera falta que hacía",
      "url": "https://www.imdb.com/title/tt0082808/",
      "year": "1982"
   }
]
```

### Búsqueda de una película a través de su ID

GET [http://localhost:22048/api/film?id=0169364](http://localhost:22049/api/film?id=0169364)

```json
{
   "duration": "1h 30m",
   "genre": "Comedy, Drama",
   "id": "0169364",
   "image": "https://m.media-amazon.com/images/M/MV5BMmI3NjNhZTctMmY0Yy00OGI3LTk4MjQtYjRjMTRjZGRkMTMxXkEyXkFqcGdeQXVyNjgxMTU1ODU@._V1_FMjpg_UX1000_.jpg",
   "rating": "6.4",
   "ratingCount": "615",
   "summary": "Soledad, a girl tired of being a taxi driver in Buenos Aires, travels with her car to Patagonia. She stops in a village whose inhabitants live in isolation and their only contact with the outside world is a cinema where old films are projected.",
   "title": "El viento se llevó lo que",
   "url": "https://www.imdb.com/title/tt0169364/",
   "year": "1998"
}
```

### Búsqueda de una película a través de su URL

GET [http://localhost:22049/api/film?url=%22https://www.imdb.com/title/tt0169364/%22](http://localhost:22049/api/film?url=%22https://www.imdb.com/title/tt0169364/%22)

```json
{
   "duration": "1h 30m",
   "genre": "Comedy, Drama",
   "id": "0169364",
   "image": "https://m.media-amazon.com/images/M/MV5BMmI3NjNhZTctMmY0Yy00OGI3LTk4MjQtYjRjMTRjZGRkMTMxXkEyXkFqcGdeQXVyNjgxMTU1ODU@._V1_FMjpg_UX1000_.jpg",
   "rating": "6.4",
   "ratingCount": "615",
   "summary": "Soledad, a girl tired of being a taxi driver in Buenos Aires, travels with her car to Patagonia. She stops in a village whose inhabitants live in isolation and their only contact with the outside world is a cinema where old films are projected.",
   "title": "El viento se llevó lo que",
   "url": "https://www.imdb.com/title/tt0169364/",
   "year": "1998"
}
```
