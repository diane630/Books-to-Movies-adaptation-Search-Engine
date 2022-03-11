# Setup
1. Install python3 (3.6+) and Docker(https://docs.docker.com/engine/install/) 
2. Create a virtural environment with venv, and activate it
```bash
$ python3 -m venv ./venv
$ source ./venv/bin/activate
```
3. In project folder, install required dependencies into the activated virtual environment
```bash
(venv) $ pip3 install -r requirements.txt
```
4. Setup docker containers, setup Elastic Search database and wait for all index to be created (this may take 1~2 hours)
```bash
(venv) $ docker-compose up -d
(venv) $ python3 setup_database.py
```    
5. Run Flask app, navigate to http://127.0.0.1:5000/
```bash
(venv) $ python3 main.py
```  

# Overview & Main Results
The project is based on elastic search, a document-orientated database that provides unstructured search functionality. The underlying book and movie data is crawled from IMDB and Goodreads. It is meant to develop a search engine for book-to-movie or movie-to-book adaptations.  It includes two parts: first, build a basic search engine to source a specific document of one catagory (a book or a movie); second, given a known document, recommend similar documents from the other catagory (movies or books).    

For example, an user can enter a phrase (e.g. Harry Potter and the Sorcerer's Stone) and select a catagory (movie), and the application will retrieve search result for all relevant movies. The user can then select any of them, click the recommend button, and book recommendations for this movie  will be returned(e.g. Harry Potter and the Sorcerer's Stone (Harry Potter, #1) along with other Harry Potter series book). Users can also adjust the number of results for both search and recommendation.

The code base can be divided to 3 steps.   

### Crawl raw data:
Individual scraper files are in "scraper_code folder". Cleaned data (url, title, writer, story, character) is stored in "IMDB_goodreads_data folder".
> [movies data from IMDB](https://www.imdb.com/search/keyword/?mode=detail&page=1&title_type=movie): crawled first 200 pages, 50 movies per page in popularity descending order, 9999 entries in total.  

> [books data from goodreads](https://www.goodreads.com/book/popular_by_date/2021): crawled between 1921 and 2021, average 200 books per year in popularity descending order, 20199 entries in total.
### Setup Elastic Search database:
"setup_database.py" reads processed txt files from above step, assign either book or movie catagory to each entry, and then store into the Elastic Search database. 
### Build a search engine with Flask:
In "main.py", a basic Flask application communicates with Elastic Search database using ["query string"](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html) queries for retrieving search results and ["more like this"](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-mlt-query.html) queries for retrieving similar documents.


# Demo video
https://drive.google.com/file/d/1c4ozvpe91szWteBz-6wVFwOUonVyYUdF/view
