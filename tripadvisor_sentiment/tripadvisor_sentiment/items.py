# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorAttractionItem(scrapy.Item):
  
  attraction_name = scrapy.Field()
  attraction_rating = scrapy.Field()
  attraction_n_reviews = scrapy.Field()
  attraction_n_reviews_eng = scrapy.Field()
  distance_to_center = scrapy.Field()
  # duration = scrapy.Field()
  attraction_rank = scrapy.Field()
  categories = scrapy.Field()
  attractions_nearby = scrapy.Field()
  restaurants_nearby = scrapy.Field()

class TripadvisorReviewItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  
  attraction = scrapy.Field()
  title = scrapy.Field()
  content = scrapy.Field()
  rating = scrapy.Field()
  date = scrapy.Field()
  helpful_votes = scrapy.Field()
  # traveler_type = scrapy.Field()



