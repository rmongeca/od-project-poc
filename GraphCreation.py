import os
import json
import csv
import random
from py2neo import Graph

### Connection to graph.
neo4jUrl = "bolt://localhost:7687"
graph = Graph(neo4jUrl, bolt=True, password='odproject')


### Cypher queries.
# Movie queries
queryMovies="""
WITH {json} AS json
UNWIND json AS p
MERGE (:Film {title: p.movie_title, avg_rate: p.avg_score, id: toInt(p.movie_id)})
"""

queryDirector="""
WITH {json} AS json
UNWIND json AS p
MERGE (d:Director {name:p.director_name})
WITH d, p
MATCH (f:Film {title: p.movie_title})
MERGE (f)-[:DIRECTED_BY]->(d)
"""

queryGenresMovie="""
MERGE (g:Genre {tag: {genre}})
WITH g, {movie} AS movie
MATCH (f:Film {title: movie})
MERGE (f)-[:OF_GENRE]->(g)
"""

queryMovieRatings="""
WITH {json} AS json
UNWIND json AS p
MERGE (u:User {id: p.user_id})
WITH u, p
MATCH (f:Film {id: p.movie_id})
MERGE (u)-[:WATCHED {rating: p.Mean}]->(f)
"""

# Book queries
queryBooks="""
LOAD CSV WITH HEADERS from 'file:///books.csv' AS book
MERGE (:Book {title: book.title, avg_rate: book.average_rating, id: book.book_id, grId: book.goodreads_book_id})
"""

queryWriters="""
LOAD CSV WITH HEADERS from 'file:///books.csv' AS book
MERGE (a:Author {name: book.authors})
WITH a, book
MATCH (b:Book {title: book.title})
MERGE (b)-[:WRITTEN_BY]->(a)
"""

queryTags="""
LOAD CSV WITH HEADERS from 'file:///tags.csv' AS tags
MERGE (g:Genre {tag: tags.tag_name, id: tags.tag_id})
"""

queryBookTags="""
LOAD CSV WITH HEADERS from 'file:///book_tags.csv' AS bt
MATCH (t:Genre {id: bt.tag_id}), (b:Book {grId: bt.goodreads_book_id})
MERGE (b)-[:OF_GENRE]->(t)
"""

queryBookRatings="""
LOAD CSV WITH HEADERS from 'file:///ratings.csv' AS rat
MERGE (u:User {id: rat.user_id})
WITH u, rat
MATCH (b:Book {id: rat.book_id})
MERGE (u)-[:READ {rating: rat.rating}]->(b)
"""

### Reading of external files
# Read JSON files
with open('data/letterboxd/movies.json', encoding='utf-8') as json_file:
    movies = json.load(json_file)
with open('data/letterboxd/ratings.json', encoding='utf-8') as json_file:
    users = json.load(json_file)

### Execution of Cypher queries.
# Move queries
graph.run(queryMovies, json=movies)
for movie in movies:
    genres = movie['genres'].lower().split('|')
    for genre in genres:
        graph.run(queryGenresMovie, movie=movie['movie_title'], genre=genre)
graph.run(queryMovieRatings, json=users)

# Book queries
graph.run(queryBooks)
graph.run(queryWriters)
graph.run(queryTags)
graph.run(queryBookTags)
graph.run(queryBookRatings)

