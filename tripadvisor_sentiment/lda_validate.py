# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 12:00:23 2021

@author: Javi
"""
import pandas as pd
from tqdm import tqdm
from ast import literal_eval
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from topic_extraction import get_keywords_from_csv, plot_top_words, get_topic_attraction
    
  if use_only_keywords:
    
    pos_keywords, neg_keywords = get_keywords_from_csv(filename, attraction, True)

    count_vect_pos = CountVectorizer(max_df=1.0, min_df=2)
    doc_term_matrix_pos = count_vect_pos.fit_transform(pos_keywords)
    
    count_vect_neg = CountVectorizer(max_df=1.0, min_df=2)
    doc_term_matrix_neg = count_vect_neg.fit_transform(neg_keywords)
    
    n_topics = 3
    
    lda_model_pos = LDA(n_components=n_topics, random_state=42)
    lda_model_pos.fit(doc_term_matrix_pos)
    
    lda_model_neg = LDA(n_components=n_topics, random_state=42)
    lda_model_neg.fit(doc_term_matrix_neg)
        
    n_top_words = 5
    
    tf_feature_names_pos = count_vect_pos.get_feature_names()
    tf_feature_names_neg = count_vect_neg.get_feature_names()
    
    plot_top_words(lda_model_pos, tf_feature_names_pos, n_top_words, n_topics, f'Positive topics in LDA model - {attraction}')
    plot_top_words(lda_model_neg, tf_feature_names_neg, n_top_words, n_topics, f'Negative topics in LDA model - {attraction}')

  else:
    
    reviews = get_reviews_from_csv(filename, attraction, True)
    
    count_vect = CountVectorizer(max_df=1.0, min_df=2, stop_words='english')
    doc_term_matrix = count_vect.fit_transform(reviews)

    n_topics = 3
    
    lda_model = LDA(n_components=n_topics, random_state=42)
    lda_model.fit(doc_term_matrix)

    n_top_words = 5    
    tf_feature_names = count_vect.get_feature_names()
    
    plot_top_words(lda_model, tf_feature_names, n_top_words, n_topics, f'Topics in LDA model - {attraction}')


filename = 'processed_reviews.csv'
attraction = "Buckingham Palace"

pos_keywords, neg_keywords = get_keywords_from_csv(filename, attraction, True)

count_vect = CountVectorizer(max_df=1.0, min_df=2)
doc_term_matrix = count_vect.fit_transform(pos_keywords)

n_topics = [2, 3, 4, 5, 6]
n_top_words = 5

for num in tqdm(n_topics):
  lda_model = LDA(n_components=num, random_state=42)
  lda_model.fit(doc_term_matrix)
  tf_feature_names = count_vect.get_feature_names()      
  plot_top_words(lda_model, tf_feature_names, n_top_words, num, f'Topics in LDA model - {attraction}')

  print(f"Model with {num} topics")
  # print("Best log likelihood score: ", lda_model.score(doc_term_matrix))
  print("Model perplexity: ", lda_model.perplexity(doc_term_matrix))