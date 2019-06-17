# Open Data - Final Project
## Proof of Concept

**Proof of concept** for the **Open Data final project**. This project contains the necessary scripts and data files to populate an initialized Neo4j graph. Then use this graph to generate recommendations

The repository contains:

* Data folder with the provided data files, already preprocessed. These include:
  - *GoodReads* data in CSV format, with books, tags and user rating information.
  - *Letterboxd* data in JSON format with movie and ratings information.
  - Pre-processing R scripts that were used to preprocess mock data for the proof of concept.
* Graph creation Python script that populates an initialized Neo4j graph
* Recommender Python script that runs the recommender queries.

### Requisites

In order to get the recommender started, make sure there is an initialized and started Neo4j empty graph. The graph needs to be accessible through **Bolt** protocol at **[bolt://localhost:7687](bolt://localhost:7687)** with password **odproject**

In addition, the **data/goodreads/*.csv** files must be copied to the correct Neo4j import folder for the graph.

Python module **py2neo** needs to be installed in the system, as the Neo4j wrapper.

### Use instructions

Once the empty graph database is started, run the *GraphCreation.py* script in order to populate it.

When the script is finished, you can run the *Recommender.py* script to start the recommender queries.

When running the script, one can enter two optional integers as command arguments that will be passed to the script as **User_id**, the user who will recieve the recommendations, and **Limit** the number of Movies/Books (limit items of each) that the system will recommend. By the default these are *User_id=1* and *Limit=5*.