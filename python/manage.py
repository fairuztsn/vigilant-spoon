import pandas as pd
import json
import os

file_path = os.path.join("data", "recently_played_data.json")

with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Convert JSON to DataFrame
df = pd.DataFrame(json_data)

# Group by Artist and count the number of tracks
artist_counts = df.groupby('Artist').size().reset_index(name='Listen Count')

# Save the result to a CSV file
artist_counts.to_csv(os.path.join("data", 'artist_listen_counts.csv'), index=False)

artist_counts.head()

print("CSV file created successfully.")
