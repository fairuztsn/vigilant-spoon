import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Read the CSV file into a DataFrame
data = pd.read_csv(os.path.join("data", "top_artists_and_time_4_weeks.csv"))  # Replace 'your_file.csv' with the actual file name

# Combine all genres into a single string
all_genres = ','.join(data['genres'].dropna())

# Create a WordCloud object
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_genres)

# Plot the WordCloud image
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Turn off the axis labels
plt.show()
