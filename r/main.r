install.packages("wordcloud", repos = "https://cran.r-project.org")
library(wordcloud)

directory <- "C:/Users/tsfai/Projects/word-clouds/data"
filename <- "genres_30_days_assumption.txt"
full_path <- file.path(directory, filename)

text <- tolower(readLines(full_path, warn = FALSE))
text <- paste(text, collapse = " ")

word_freq <- table(strsplit(text, "\\s"))

print(head(word_freq))


wordcloud(words = names(word_freq), freq = word_freq, scale = c(3, 0.5), min.freq = 2, colors = brewer.pal(8, "Dark2"))

filename <- "artists.txt"
full_path <- file.path(directory, filename)

text <- tolower(readLines(full_path, warn = FALSE))
text <- paste(text, collapse = " ")

word_freq <- table(strsplit(text, "\\s"))

print(head(word_freq))

wordcloud(
    words = names(word_freq),
    freq = word_freq,
    scale = c(3, 0.5),
    min.freq = 2,
    colors = brewer.pal(8, "Dark2"),
    rot.per = 0
)