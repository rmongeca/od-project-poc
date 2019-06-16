library(dplyr)
library(stringdist)
library(tidyverse)
library(rjson)
rm(list = ls())

movies <- read.csv("movies.csv", header = TRUE, dec=".", encoding = "UTF-8")
movies.redu <- read.csv("movies_reduced.csv", header = TRUE, dec=".", encoding = "UTF-8")

colnames(movies)
movies <- movies[,c(2,10,12,17,26)]
movies$avg_score <- movies$imdb_score/2
movies <- movies[,-5]


filtered.movies <- movies %>% 
  select(director_name, genres, movie_title, plot_keywords, avg_score) %>% 
  filter(   str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "biography") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "family") |
              str_detect(tolower(genres), pattern = "family") |
              str_detect(tolower(genres), pattern = "family") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "fantasy") |
              str_detect(tolower(genres), pattern = "fantasy") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "horror") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "fantasy") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "thriller") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "action") |
              str_detect(tolower(genres), pattern = "history") |
              str_detect(tolower(genres), pattern = "drama") |
              str_detect(tolower(genres), pattern = "romance") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "family") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "thriller") |
              str_detect(tolower(genres), pattern = "family") |
              str_detect(tolower(genres), pattern = "mystery") |
              str_detect(tolower(genres), pattern = "sci") |
              str_detect(tolower(genres), pattern = "adventure") |
              str_detect(tolower(genres), pattern = "fantasy") |
              str_detect(tolower(genres), pattern = "action") |
              str_detect(tolower(genres), pattern = "action")
              
  ) %>%
  as.data.frame()

filtered.movies <- filtered.movies[-which(filtered.movies$movie_title %in% movies.redu$movie_title),]
filtered.movies <- filtered.movies[sample(nrow(filtered.movies), 51),]

final.movies <- rbind(movies.redu, filtered.movies)
final.movies <- final.movies[order(final.movies$movie_title),]
rownames(final.movies) <- NULL
final.movies$movie_id <- rownames(final.movies)
final.movies <- final.movies[,c(6, 1, 2, 3, 5)]



write.csv(final.movies, file = "movies_final.csv", row.names = F)
json <- toJSON(unname(split(final.movies, 1:nrow(final.movies))))
write(json, file="movies.json")
