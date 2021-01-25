import scrapy
from tripadvisor_sentiment.items import TripadvisorReviewItem, TripadvisorAttractionItem
import re
from geopy import Nominatim, distance
import logging


logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("geopy").setLevel(logging.WARNING)

def get_distance_to_center(address):
  
  # addresses in tripadvisor come as "Nº StreetName, City POSTCODE Country"
  # where the postcode can come before or after the city name

  city = address.split(',')[-1]
  clean_city = re.sub(r'\w*\d\w*', '', city).strip()
  
  locator = Nominatim(user_agent="myGeocoder")
  
  _, center_loc = locator.geocode(clean_city)
  _, loc = locator.geocode(address)
  
  return round(distance.distance(center_loc, loc).km, 4)

class TripadvisorAttractionsSpider(scrapy.Spider):
    name = 'tripattraction'
    allowed_domains = ['www.tripadvisor.com']
    start_urls = ['https://www.tripadvisor.com/Attractions-g186338-Activities-a_allAttractions.true-London_England.html']
    # start_urls = ['https://www.tripadvisor.com/Attraction_Review-g186338-d187547-Reviews-Tower_of_London-London_England.html']

    def parse(self, response):
    
      # 'This is the main function called when parsing. It will start in the main attractions page'  
    
      # this get the attractions of one page 
      for href in response.xpath('//div[@class="_2pZeTjmb"]/a/@href'):
      
        url = response.urljoin(href.extract())
        yield scrapy.Request(url, self.parse_attraction)
      
      '''
      Format for the url when turning pages:
      https://www.tripadvisor.com/Attractions-g186338-Activities-a_allAttractions.true-London_England.html -> page 1
      https://www.tripadvisor.com/Attractions-g186338-Activities-oa30-a_allAttractions.true-London_England.html -> page 2
      '''
      
      current_page = int(response.xpath('//span[@class="pageNum current disabled"]/text()')[0].extract())
      all_pages = list(map(int, response.xpath('//div[@class="pageNumbers"]/child::*[self::a]/text()').extract()))
      
      hyphen_ocurrences = [i for i, letter in enumerate(response.url) if letter == '-']
      
      # if this is not the last page
      if current_page < max(all_pages):
        url = response.url[:hyphen_ocurrences[2]+1] + 'oa' + str((current_page)*30) + response.url[hyphen_ocurrences[2]:]
        yield scrapy.Request(url, self.parse)
    
    
    
    def parse_attraction(self, response):
        
      'This function parses the attraction page. It also calls the function parse_review'

      item = TripadvisorAttractionItem()
      
      # regular expression to remove html tags
      # regex = re.compile("<(.*?)>")
      
      # very long names have a smaller header type
      name = response.xpath('//h1[@class="ui_header h1"]/text()')
      if name:
        item['attraction_name'] = name[0].extract()
      else:
        item['attraction_name'] = response.xpath('//h1[@class="ui_header h2"]/text()')[0].extract()
      
      # not all attractions have reviews
      n_reviews = response.xpath('//span[@class="_1yuvE2vR"]/text()')
      if n_reviews:
        item['attraction_n_reviews'] = n_reviews[0].extract()
      
      n_reviews_eng = response.xpath('//span[@class="mxlinKbW"]/text()')
      if n_reviews_eng:
        item['attraction_n_reviews_eng'] = n_reviews_eng[1].extract().replace("\"", "")

      rating_string = response.xpath('//div[@class="_1NKYRldB"]/child::*[self::span]')
      if rating_string:
        digits = [int(s) for s in rating_string[0].extract() if s.isdigit()]
        item['attraction_rating'] = (digits[0]*10 + digits[1])/10

      address = response.xpath('//div[@class="LjCWTZdN"]/child::*[self::span]/text()')
      if address:
        try:
          item['distance_to_center'] = get_distance_to_center(address[0].extract())
        except:
          pass

      # n_photos = response.xpath('//div[@class="WwXGt5FE"]/div[@class="_3l73Kcue _1KdpnWoY"]')
      # item['attraction_n_photos'] =  #no idea yet

      # duration = response.xpath('//div[@class="_2y7puPsQ"]')
      # print(duration.extract())
      # if duration:
      #   item['duration'] = duration[0].extract()
      
      restaurants_nearby = response.xpath('//span[@class="_2SSx3Jmy _2E0OqmuR"]/text()')
      if restaurants_nearby:
        item['restaurants_nearby'] = restaurants_nearby[0].extract()
        
      attractions_nearby = response.xpath('//span[@class="_2SSx3Jmy K4di_Un0"]/text()')
      if attractions_nearby:
        item['attractions_nearby'] = attractions_nearby[0].extract()
      
        
      attraction_rank = response.xpath('//div[@class="eQSJNhO6"]/span/b/span/text()')
      if attraction_rank:
        item['attraction_rank'] =  attraction_rank[0].extract().replace('#', '')
      
      # we need a string because list separator can interfere with csv format
      cat_list = ''
      for cat in list(set(response.xpath('//a[@class="_1cn4vjE4"]/text()').extract())):
        cat_list += cat + ';'
        
      item['categories'] = cat_list
      
      yield scrapy.Request(response.url, self.parse_review, dont_filter=True)

      yield item


    def parse_review(self, response):
      
      # for every review in the page
      for review in response.xpath('//div[@class="Dq9MAugU T870kzTX LnVzGwUB"]'):
        
        # user = review.xpath('.//a[@class="ui_header_link _1r_My98y"]/text()')[0].extract()
        
        item = TripadvisorReviewItem()
        
        attraction = response.xpath('//h1[@class="ui_header h1"]/text()')
        if attraction:
          item['attraction'] = attraction[0].extract()
        else:
          item['attraction'] = response.xpath('//h1[@class="ui_header h2"]/text()')[0].extract()
        
        # regular expression to remove html tags
        regex = re.compile("<(.*?)>")
        
        title = review.xpath('.//a[@class="ocfR3SKN"]/child::*[self::span]')[0].extract()
        item['title'] = re.sub(regex, '', title)
          
        # some spam attractions have no rating
        rating_string = review.xpath('.//div[@class="nf9vGX55"]/child::*[self::span]')
        if rating_string:
          rating = rating_string[0].extract()
          digits = [int(s) for s in rating if s.isdigit()]
          item['rating'] = (digits[0]*10 + digits[1])/10
        
        # not all the reviews have long content
        content = review.xpath('.//q[@class="IRsGHoPm"]/child::*').extract()
        if len(content) != 1:
          item['content'] = re.sub(regex, '', content[0]) + re.sub(regex, '', content[1])
        else:
          item['content'] = re.sub(regex, '', content[0])
        
        date = review.xpath('.//span[@class="_34Xs-BQm"]/text()')
        if date:
          item['date'] = date[0].extract()[1:]
        
        # helpful_votes is not always present
        helpful_votes = review.xpath('.//span[@class="_3kbymg8R _2o1bmw1O"]/text()')
        if helpful_votes:
          item['helpful_votes'] = helpful_votes[0].extract().split(' ')[0]
        
        yield item
          
      '''
      Format for the url when turning pages:
      https://www.tripadvisor.com/Attraction_Review-g186338-d187547-Reviews-Tower_of_London-London_England.html -> page 1
      https://www.tripadvisor.com/Attraction_Review-g186338-d187547-Reviews-or5-Tower_of_London-London_England.html -> page 2
      '''
      
      # not all attractions have review pages
      current_page = response.xpath('//span[@class="pageNum current disabled"]/text()')
      if current_page:
        current_page_num = int(current_page[0].extract())
        all_pages = list(map(int, response.xpath('//div[@class="pageNumbers"]/child::*[self::a]/text()').extract()))
        
        hyphen_ocurrences = [i for i, letter in enumerate(response.url) if letter == '-']
        
        # if this is not the last page
        if current_page_num < max(all_pages):
          url = response.url[:hyphen_ocurrences[3]+1] + 'or' + str((current_page_num)*5) + response.url[hyphen_ocurrences[3]:]
          yield scrapy.Request(url, self.parse_review)
