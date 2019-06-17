import sys
import pandas as pd
from py2neo import Graph

### Set default paramters
limit = 5
user = 1

### Set script parameters
if len(sys.argv) > 1 and int(sys.argv[1]) > 0:
    user = int(sys.argv[1])
if len(sys.argv) > 2 and int(sys.argv[2]) > 0:
    limit = int(sys.argv[2])
header="""
Open Data - Final Project - Recommender 
----------------------------------------
Generating recommendations for User {user} with limit {limit}:

"""
print(header.format(user=user, limit=limit))

similarities="""
Table with {type} user similarities for given user:

{content}

---------------

"""

recommendations="""
Table with Film/Book recommendations for given user:

{content}

---------------

"""

### Connection to graph.
neo4jUrl = "bolt://localhost:7687"
graph = Graph(neo4jUrl, bolt=True, password='odproject')


### Cypher queries.
querieEucSimilarity="""
MATCH (:User {uId: {user}})-[e1]-(w),
    (u:User)-[e2]-(w)
WHERE w:Film OR w:Book
RETURN u.uId as user,
    algo.similarity.euclideanDistance(collect(e1.rating), collect(e2.rating)) AS EucSim
ORDER BY EucSim ASC
LIMIT {limit}
"""

querieCosSimilarity="""
MATCH (:User {uId: {user}})-[e1]-(w),
    (u:User)-[e2]-(w)
WHERE w:Film OR w:Book
RETURN u.uId as user,
    algo.similarity.cosine(collect(e1.rating), collect(e2.rating)) AS CosSim
ORDER BY CosSim DESC
LIMIT {limit}
"""

queryRecommendFilm="""
UNWIND {simUsers} AS uid
MATCH (:User {uId: uid})-[]-(w:Film)
WHERE NOT (:User {uId: {user}})-[]-(w)
WITH w, rand() AS r
ORDER BY r
RETURN DISTINCT SUBSTRING(w.title,0,{strLimit}) AS title, labels(w) AS Type
LIMIT {limit}
"""

queryRecommendBook="""
UNWIND {simUsers} AS uid
MATCH (:User {uId: uid})-[]-(w:Book)
WHERE NOT (:User {uId: {user}})-[]-(w)
WITH w, rand() AS r
ORDER BY r
RETURN DISTINCT SUBSTRING(w.title,0,{strLimit}) AS title, labels(w) AS Type
LIMIT {limit}
"""

### Execution of Cypher queries.
eucSim = graph.run(querieEucSimilarity, user=user, limit=limit).to_data_frame()
cosSim = graph.run(querieCosSimilarity, user=user, limit=limit).to_data_frame()
simUsers = cosSim["user"].tolist() + eucSim["user"].tolist()
recom1 = graph.run(queryRecommendFilm, simUsers=simUsers, user=user, limit=limit, strLimit=30).to_data_frame()
recom2 = graph.run(queryRecommendBook, simUsers=simUsers, user=user, limit=limit, strLimit=30).to_data_frame()
recom = pd.concat([recom1, recom2])


### Result presentation
#print(similarities.format(type="Eculidean", content=eucSim.to_string(index=False)))
#print(similarities.format(type="Cosine", content=cosSim.to_string(index=False)))
print(recommendations.format(content=recom.to_string(index=False)))

