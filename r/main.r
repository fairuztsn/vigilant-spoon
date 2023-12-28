file_path <- file.path("data", "top_artists_and_time_4_weeks.csv")
data <- read.csv(file_path)

# Check if 'wordcloud' is installed
if (!require(wordcloud, quietly = TRUE)) {
    install.packages("wordcloud")
    library(wordcloud)
}

wordcloud(words = data$artist, freq = data$listening_time_minutes, scale = c(3, 0.5), min.freq = 1, colors = brewer.pal(8, "Dark2")) # nolint: line_length_linter.