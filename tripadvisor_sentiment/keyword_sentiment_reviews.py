import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from rake_nltk import Rake
from tqdm import tqdm
    
def get_score_phrases(title, content, helpful_votes):
  
  rake = Rake()
  analyzer = SentimentIntensityAnalyzer()
  
  rake.extract_keywords_from_text(title+" "+content)
  rake.get_ranked_phrases_with_scores()
  
  pos_score_list = []
  neg_score_list = []
    
  for phrase_tuple in rake.rank_list:
    
    sentiment_score = analyzer.polarity_scores(phrase_tuple[1])['compound']
    
    if sentiment_score > 0.3:
      
      score = phrase_tuple[0]/len(phrase_tuple[1].split(' '))*(helpful_votes + 1)
      
      if phrase_tuple[1] in title.lower():
        score *= 2
      
      pos_score_list.append((score, phrase_tuple[1]))
      
    elif sentiment_score < 0:
      
      score = phrase_tuple[0]/len(phrase_tuple[1].split(' '))*(helpful_votes + 1)
      
      if phrase_tuple[1] in title.lower():
        score *= 2
      
      neg_score_list.append((score, phrase_tuple[1]))

  return pos_score_list, neg_score_list


def add_scores_to_df(df):
  
  pos_list = []
  neg_list = []
  
  for _, row in tqdm(df.iterrows()):
    
    pos, neg = get_score_phrases(str(row.title), row.content, row.helpful_votes)
    pos_list.append(pos)
    neg_list.append(neg)
    
  df['positive_keywords'] = pos_list
  df['negative_keywords'] = neg_list
  
  return df

pd.set_option('display.expand_frame_repr', False)

filename = 'tripadvisorreview.csv'

review_df = pd.read_csv(filename) 

review_df['helpful_votes'] = review_df['helpful_votes'].replace(np.nan, 0)

# create new column based on the rating of the review
review_df['positive_sentiment'] = np.where(review_df['rating'] >= 4, True, False)

review_df = add_scores_to_df(review_df)

review_df.to_csv('processed_reviews.csv')
