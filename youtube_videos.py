import pandas as pd
import json

import matplotlib
import matplotlib.pyplot as plt


matplotlib.rcParams['figure.figsize'] = (10, 10)

file_name = 'USvideos.csv'
my_df = pd.read_csv(file_name, index_col='video_id')
my_df.head()

my_df['trending_date'] = pd.to_datetime(my_df['trending_date'], format='%y.%d.%m')
my_df['trending_date'].head()

my_df['publish_time'] = pd.to_datetime(my_df['publish_time'], format='%Y-%m-%dT%H:%M:%S.%fZ')
my_df['publish_time'].head()

# separates date and time into two columns from 'publish_time' column
my_df.insert(4, 'publish_date', my_df['publish_time'].dt.date)
my_df['publish_time'] = my_df['publish_time'].dt.time
my_df[['publish_date', 'publish_time']].head()

type_int_list = ['views', 'likes', 'dislikes', 'comment_count']
for column in type_int_list:
    my_df[column] = my_df[column].astype(int)

type_str_list = ['category_id']
for column in type_str_list:
    my_df[column] = my_df[column].astype(str)

# creates a dictionary that maps `category_id` to `category`
id_to_category = {}

with open('US_category_id.json', 'r') as f:
    data = json.load(f)
    for category in data['items']:
        id_to_category[category['id']] = category['snippet']['title']

my_df.insert(4, 'category', my_df['category_id'].map(id_to_category))
my_df[['category_id', 'category']].head()


def visualize_most(my_df, column, num=10):  # getting the top 10 videos by default
    sorted_df = my_df.sort_values(column, ascending=False).iloc[:num]

    ax = sorted_df[column].plot.bar()

    # customizes the video titles, for asthetic purposes for the bar chart
    labels = []
    for item in sorted_df['title']:
        labels.append(item[:10] + '...')
    ax.set_xticklabels(labels, rotation=45, fontsize=10)

    plt.show()

visualize_most(my_df, 'views')

category_count = my_df['category'].value_counts() # frequency for each category
category_count

ax = category_count.plot.bar()
ax.set_xticklabels(labels=category_count.index, rotation=45, fontsize=10)

plt.show()
