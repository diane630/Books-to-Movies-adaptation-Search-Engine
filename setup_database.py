from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

es_client = Elasticsearch()
es_index_client = IndicesClient(es_client)

try:
    es_index_client.create(index="db-demo")
except Exception as e: 
    print(e)

print("Start seeding database. This may take a few hours... Thanks for your patience.")
# seed goodreads data
book_urls = []
book_titles = []
book_stories = []
book_writers = []
book_characters = []

with open("../CourseProject/IMDB_goodreads_data/book_urls.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        book_urls.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/book_titles.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        book_titles.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/book_stories.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        book_stories.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/book_writers.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        book_writers.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/book_characters.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        book_characters.append(line)
        
i = 0
book_idx = 0
while book_idx < len(book_urls):
    url = book_urls[book_idx]
    title = book_titles[book_idx]
    story = book_stories[book_idx]
    writer = book_writers[book_idx]
    character = book_characters[book_idx]    

    doc = {
        'url': url,
        'title': title,
        'story': story,
        'writer': writer,
        'character': character,
        'catagory':'book'
    }

    res = es_client.index(index="db-demo", id=i, document=doc)
    if i % 100 == 0:
        print(".", end="")
    if i % 1000 == 0:
        print(res['result'] + " " + str(i))     
    i += 1
    book_idx += 1
print(f"Seeded {book_idx} books from goodreads")

# seed imdb data
movie_urls = []
movie_titles = []
movie_stories = []
movie_writers = []
movie_characters = []

with open("../CourseProject/IMDB_goodreads_data/movie_urls.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        movie_urls.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/movie_titles.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        movie_titles.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/movie_stories.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        movie_stories.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/movie_writers.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        movie_writers.append(line)
        
with open("../CourseProject/IMDB_goodreads_data/movie_characters.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = line.rstrip()
        movie_characters.append(line)
        
# i = 20199
movie_idx = 0
while movie_idx < len(movie_urls):
    url = movie_urls[movie_idx]
    title = movie_titles[movie_idx]
    story = movie_stories[movie_idx]
    writer = movie_writers[movie_idx]
    character = movie_characters[movie_idx]    

    doc = {
        'url': url,
        'title': title,
        'story': story,
        'writer': writer,
        'character': character,
        'catagory':'movie'
    }

    res = es_client.index(index="db-demo", id=i, document=doc)
    if i % 100 == 0:
        print(".", end="")
    if i % 1000 == 0:
        print(res['result'] + " " + str(i))     
    i += 1
    movie_idx += 1
print(f"Seeded {movie_idx} movies from IMDB")
