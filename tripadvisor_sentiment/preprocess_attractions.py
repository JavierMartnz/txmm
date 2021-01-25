import pandas as pd
import numpy as np

pd.set_option('display.expand_frame_repr', False)

filename = 'tripadvisorattraction.csv'
review_file = 'tripadvisorreview.csv'

attraction_df = pd.read_csv(filename) 
review_df = pd.read_csv(review_file)

attraction_df['attraction_n_reviews'] = attraction_df['attraction_n_reviews'].str.replace(',', '').astype(int)
attraction_df['attraction_rank'] = attraction_df['attraction_rank'].str.replace(',', '').astype(int)
attraction_df = attraction_df[attraction_df['attraction_rank'] <= 1000]
attraction_df['categories'] = attraction_df['categories'].str.replace(';', ', ').str[:-2]

review_df['positive_sentiment'] = np.where(review_df['rating'] >= 4, True, False)

n_pos_list = []
n_neg_list = []

for index, row in attraction_df.iterrows():
  
  aux_df = review_df.loc[review_df['attraction'] == row.attraction_name].positive_sentiment.value_counts()
  
  n_pos_list.append(aux_df.loc[True])
  n_neg_list.append(aux_df.loc[False]) if False in aux_df else n_neg_list.append(0)

attraction_df['n_positive_reviews'] = n_pos_list
attraction_df['n_negative_reviews'] = n_neg_list

attraction_df['pos_review_ratio'] = attraction_df['n_positive_reviews']/attraction_df['attraction_n_reviews']
attraction_df['neg_review_ratio'] = attraction_df['n_negative_reviews']/attraction_df['attraction_n_reviews']


attraction_df.to_csv(filename)