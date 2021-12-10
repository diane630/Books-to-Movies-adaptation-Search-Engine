from flask import Flask
from elasticsearch import Elasticsearch
from flask import render_template, request, jsonify, redirect, url_for

app = Flask(__name__) 

es_client = Elasticsearch()
alert = 0
default_size = 10

@app.route('/')
def home():
    return render_template("index.html", alert = alert, size = default_size)

@app.route('/search/<catagory>/<querytext>/<quantity>')
def searchResults(querytext, quantity, catagory):
    query_body = {
        "bool": {
            "must": [
                {
                    "term": 
                        {"catagory": catagory}
                }
            ],
            "should": [
                {"query_string": 
                    {
                    "query": querytext,
                    "fuzziness" : "auto:0,10"
                    }
                }
            ]
        }
    }
    result = es_client.search(index="db-demo", query=query_body, size=quantity)
    all_hits = result['hits']['hits']

    writers = []
    titles = []
    texts = []
    urls = []
    id = []
    catagory = []
    for doc in all_hits:
      writers.append(doc["_source"]["writer"])
      titles.append(doc["_source"]["title"])
      urls.append(doc["_source"]["url"])
      texts.append(doc["_source"]["story"])
      catagory.append(doc["_source"]["catagory"])   
      id.append(doc["_id"])
    docs = list(zip(writers, titles, urls,texts, id, catagory))
    return render_template("display.html", doc = docs, querybody = querytext, catagory = catagory[0], type="Search", quantity = quantity)

@app.route('/recommend/<catagory>/<querytext>/<id>/<quantity>')
def recommendResults(querytext, id, quantity, catagory):
    # always recommend a differnet catagory
    catagory = "book" if catagory == "movie" else "movie"
    query_body = {
        "bool": {
        "must": [
            {"term": 
                {"catagory": catagory}
            },
            {"query_string": {
            "query": querytext,
            "fuzziness" : "auto:0,10"
            }
            }
        ],
        "should": [
            {"more_like_this": {
            "fields": [
                "title","writer","character","story"
            ],
            "like": [
                {
                "_index": "db-demo",
                "_id": id
                }
            ],
            "min_term_freq": 1,
            "max_query_terms": 12
            }
            }
        ]
        }
    }
    result = es_client.search(index="db-demo", query=query_body, size=quantity)
    all_hits = result['hits']['hits']

    writers = []
    titles = []
    texts = []
    urls = []
    id = []
    catagory = []
    for doc in all_hits:
      writers.append(doc["_source"]["writer"])
      titles.append(doc["_source"]["title"])
      urls.append(doc["_source"]["url"])
      texts.append(doc["_source"]["story"])
      catagory.append(doc["_source"]["catagory"])   
      id.append(doc["_id"])
    docs = list(zip(writers, titles, urls,texts, id, catagory))
    return render_template("display.html", doc = docs, querybody = querytext, catagory = catagory[0], type="Recommend", quantity = quantity)

@app.route('/search', methods=['POST'])
def search():
    querytext = request.form['querytext']
    quantity = request.form['quantity']
    catagory = request.form['catagory']

    # input checking
    if(querytext.strip()):
      alert = 0
    else:
      alert = 1
      return redirect(url_for('home', alert = alert))
    
    return redirect(url_for('searchResults', querytext = querytext, quantity = quantity, catagory = catagory))

@app.route('/recommend', methods=['POST'])
def recommend():
    querytext = request.form['querytext']
    db_id = request.form['db_id']
    quantity = request.form['quantity']
    catagory = request.form['catagory']
    return redirect(url_for('recommendResults', querytext = querytext, id = db_id, quantity = quantity, catagory = catagory))

if __name__ == '__main__':
   app.run(debug = True)