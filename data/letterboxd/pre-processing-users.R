library(dplyr)
library(stringdist)
library(tidyverse)
library(rjson)
rm(list = ls())

movies <- read.csv("movies.csv", header = TRUE, dec=".", encoding = "UTF-8")
size <- 500
ratings <- data.frame(user_id=sample(1:20, size, replace = T), movie_id=sample(nrow(movies), size, replace = T), user_score=round(runif(size, min=0.01, max=5), digits=2))
