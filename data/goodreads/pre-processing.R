library(dplyr)
library(stringdist)
rm(list = ls())
ClosestMatch = function(string, stringVector, n = 4){
  flag <- amatch(string, stringVector, maxDist = n)
  if ( !is.na(flag)){
    flag
  }
  else
    -1
}

books <- read.csv("books.csv", header = TRUE, dec=".")
book_tags <- read.csv("book_tags.csv", header = TRUE, dec=".")
tags <- read.csv("tags.csv", header = TRUE, dec=".")
ratings <- read.csv("ratings.csv", header = T, dec=".")

colnames(books)
books <- books[,c(1:2,8,11,13)]

book_tags <- book_tags[which(book_tags$goodreads_book_id %in% books$goodreads_book_id),]
book_tags <- book_tags[order(book_tags$goodreads_book_id, -book_tags$count),]
book_tags <- book_tags[-which(book_tags$tag_id %in% c(1642, 1416, 3389, 9221, 8865, 5051, 2104, 11557, 11590, 22743, 8717, 5207, 4949, 30574, 32989)),]
book_tags <- book_tags %>%
  group_by(goodreads_book_id) %>%
  top_n(n=5, wt=count) %>%
  ungroup %>%
  as.data.frame()

tags <- tags[which(tags$tag_id %in% book_tags$tag_id),]

ratings <- ratings[which(ratings$book_id %in% books$book_id),]
ratings <- ratings %>%
  filter(user_id <= 20) %>%
  as.data.frame()
ratings <- ratings[order(ratings$user_id, ratings$book_id),]
rownames(ratings) <- NULL

#dive into the whole book tags and apply the function to every row
names <- tags$tag_name
for ( i in 1:length(names)){
  flag <- ClosestMatch(names[i], names[-i])
  if ( flag > 0){
    if ( i <= flag ) #if the found index is bigger than current row's index, increase the found(we discard the current row, so it decreases the no of rows by 1; we need to increase it again)
      names[i] = names[flag+1]
    else
      names[i] = names[flag]
  }
}
tags$tag_name <- names

write.csv(books, file = "books.csv", row.names = F)
write.csv(book_tags, file = "book_tags.csv", row.names = F)
write.csv(tags, file = "tags.csv", row.names = F)
write.csv(ratings, file = "ratings.csv", row.names = F)
