# imdb-web-scraping
IMDB web scraping done utilizing Scrapy
## Autores
- César Fernández García
- Oscar Tienda Beteta
## Descripción del repositorio
**/source**: Proyecto scrapy generano con comando ***scrapy startproject IMDB***.

La estructura del proyecto generado es la siguiente:

    source/
        scrapy.cfg              # deploy configuration file
        IMDB/                   # project's Python module, you'll import your code from here
            __init__.py
            items.py            # project items definition file
            middlewares.py      # project middlewares file
            pipelines.py        # project pipelines file
            settings.py         # project settings file
            spiders/            # a directory where you'll later put your spiders
                __init__.py

Generamos el spider ejecutando el comando ***scrapy genspider IMDBspider***

            spiders/            # a directory where you'll later put your spiders
                __init__.py
                IMDBspider.py   # spider IMDB

DOI de Zenodo: https://zenodo.org/
 
