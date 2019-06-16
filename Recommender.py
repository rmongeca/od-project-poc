import os
import sys
import random
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

### Connection to graph.
neo4jUrl = "bolt://localhost:7687"
graph = Graph(neo4jUrl, bolt=True, password='odproject')


### Cypher queries.
querieEucSimilarity="""
MATCH (:User {id: {user}})-[e1]-(w),
    (u:User)-[e2]-(w)
WHERE w:Film OR w:Book
RETURN u.id as user, sqrt(sum((e1.rating - e2.rating)^2)) AS EucSim
ORDER BY EucSim ASC
LIMIT {limit}
"""

### Execution of Cypher queries.
eucSim = graph.run(querieEucSimilarity, user=user, limit=limit)
print(eucSim.to_data_frame())

