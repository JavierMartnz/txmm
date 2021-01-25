# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 18:48:47 2020

@author: Javier Martínez
"""

import pandas as pd
from ast import literal_eval
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import matplotlib.pyplot as plt
# from wordcloud import WordCloud

def get_keywords_from_csv(filename, attraction, positive):
  
  review_df = pd.read_csv(filename)
  
  all_pos_keywords = []
  all_neg_keywords = []
  
  attraction_specific_df = review_df[review_df.attraction == attraction]
  attraction_specific_df = attraction_specific_df[attraction_specific_df.positive_sentiment == positive]
  
  for _, row in tqdm(attraction_specific_df.iterrows()):
  
    pos_row_array = literal_eval(row.positive_keywords) 
    neg_row_array = literal_eval(row.negative_keywords) 
  
    for score_tuple in pos_row_array:
      
      for i in range(0, int(score_tuple[0])):
        all_pos_keywords.append(score_tuple[1])
        
    for score_tuple in neg_row_array:
      
      for i in range(0, int(score_tuple[0])):
        all_neg_keywords.append(score_tuple[1])

  return all_pos_keywords, all_neg_keywords

def plot_top_words(model, feature_names, n_top_words, n_topics, title=None):
  
  fig, axes = plt.subplots(1, n_topics, figsize=(30, 15), sharex=True)
  axes = axes.flatten()
  
  for topic_idx, topic in enumerate(model.components_):
    top_features_ind = topic.argsort()[:-n_top_words - 1:-1]
    top_features = [feature_names[i] for i in top_features_ind]
    weights = topic[top_features_ind]
  
    ax = axes[topic_idx]
    ax.barh(top_features, weights, height=0.4)
    ax.set_title(f'Topic {topic_idx +1}',
                  fontdict={'fontsize': 30})
    ax.invert_yaxis()
    ax.tick_params(axis='both', which='major', labelsize=20)
    for i in 'top right left'.split():
        ax.spines[i].set_visible(False)
    fig.suptitle(title, fontsize=40) if title else None
    
  plt.subplots_adjust(top=0.85, bottom=0.4, wspace=0.3, hspace=0.5)
  plt.show()
  
  for topic_idx, topic in enumerate(model.components_):
    top_features_ind = topic.argsort()[:-n_top_words*2 - 1:-1]
    top_features = [feature_names[i] for i in top_features_ind]
    weights = topic[top_features_ind]
    
    # plt.figure()
    # plt.imshow(WordCloud(background_color='white').fit_words({top_features[i]: weights[i] for i in range(len(top_features))}))
    # plt.axis("off")
    # # plt.title("Topic #" + str(topic_idx))
    # plt.show()
  

def get_topic_attraction(filename, attraction, use_only_keywords=True):
    
  if use_only_keywords:
    
    pos_keywords, neg_keywords = get_keywords_from_csv(filename, attraction, True)

    count_vect_pos = CountVectorizer(max_df=1.0, min_df=2)
    doc_term_matrix_pos = count_vect_pos.fit_transform(pos_keywords)
    
    count_vect_neg = CountVectorizer(max_df=1.0, min_df=2)
    doc_term_matrix_neg = count_vect_neg.fit_transform(neg_keywords)
    
    n_topics = 2
    
    lda_model_pos = LDA(n_components=n_topics, random_state=42)
    lda_model_pos.fit(doc_term_matrix_pos)
    
    lda_model_neg = LDA(n_components=n_topics, random_state=42)
    lda_model_neg.fit(doc_term_matrix_neg)
        
    n_top_words = 5
    
    tf_feature_names_pos = count_vect_pos.get_feature_names()
    tf_feature_names_neg = count_vect_neg.get_feature_names()
    
    plot_top_words(lda_model_pos, tf_feature_names_pos, n_top_words, n_topics)
    plot_top_words(lda_model_neg, tf_feature_names_neg, n_top_words, n_topics)
    

  else:
    
    reviews = get_reviews_from_csv(filename, attraction, True)
    
    count_vect = CountVectorizer(max_df=1.0, min_df=2, stop_words='english')
    doc_term_matrix = count_vect.fit_transform(reviews)

    n_topics = 2
    
    lda_model = LDA(n_components=n_topics, random_state=42)
    lda_model.fit(doc_term_matrix)

    n_top_words = 5    
    tf_feature_names = count_vect.get_feature_names()
    
    plot_top_words(lda_model, tf_feature_names, n_top_words, n_topics)

def get_most_reviewed_attractions(filename, number):
  review_df = pd.read_csv(filename)
  return review_df.groupby('attraction').count().sort_values(by=['title'], ascending=False).index.values[0:number]

filename = 'processed_reviews.csv'

most_reviewed_10 = get_most_reviewed_attractions(filename, 10)

for attraction in most_reviewed_10:
  get_topic_attraction(filename, attraction)