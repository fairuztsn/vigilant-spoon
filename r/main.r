install.packages("wordcloud", repos = "https://cran.r-project.org")
install.packages("extrafont", repos = "https://cran.r-project.org")
library(extrafont)
library(wordcloud)
library(stringr)

directory <- "C:/Users/tsfai/Projects/word-clouds/data"
filename <- "genres_30_days_assumption.txt"
full_path <- file.path(directory, filename)

text <- readLines(full_path, warn = FALSE)
text <- paste(text, collapse = " ")

word_freq <- table(strsplit(text, "\\s"))

print(head(word_freq))

wordcloud(words = names(word_freq), freq = word_freq, scale = c(3, 0.5), min.freq = 2, colors = brewer.pal(8, "Dark2"))

filename <- "artists.txt"
full_path <- file.path(directory, filename)

text <- readLines(full_path, warn = FALSE)
text <- paste(text, collapse = "\n")

words <- unlist(strsplit(text, "\n"))
words <- str_trim(words)

word_freq <- table(words)

# Not working
font_import(pattern = "NotoSansJP")
loadfonts()

wordcloud(
    words = names(word_freq),
    freq = word_freq,
    scale = c(3, 0.5),
    min.freq = 1,
    colors = brewer.pal(8, "Dark2"),
    rot.per = 0,
    font_path = "./fonts/noto-sans-jp/NotoSansJP-VariableFont_wght.ttf"
)