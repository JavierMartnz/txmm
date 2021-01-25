# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:37:37 2020

@author: Javi
"""
import pandas as pd

def take_second(elem):
  return elem[1]

def check_incomplete_reviews(attraction_filename, review_filename):

  attraction_df = pd.read_csv(attraction_filename)
  review_df = pd.read_csv(review_filename) 
  
  incomplete_attractions = []
  
  for idx, row in attraction_df.iterrows():
    
    attraction = row.attraction_name
    n_reviews = row.attraction_n_reviews
    
    actual_n_reviews = len(review_df[review_df.attraction == attraction])
    
    if n_reviews != actual_n_reviews:
      incomplete_attractions.append((attraction, n_reviews-actual_n_reviews))

  incomplete_attractions.sort(reverse=True, key=take_second)

  return incomplete_attractions

# pd.set_option('display.expand_frame_repr', False)

incomplete = check_incomplete_reviews('tripadvisorattraction_old.csv', 'tripadvisorreview_old.csv')

