# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst, Join

# Function to extract the year from a string
def extract_year(value):
    match = re.search(r"\d{4}", value)
    if match:
        return match.group()
    else:
        return None

# Function to extract the duration in minutes from a string
def extract_duration(value):
    duration = re.findall(r'\d+', value)
    return int(duration[0])

# Function to remove newline characters from a string
def remove_newline(value):
    return value.strip('\n').strip()

# Function to remove whitespaces from a string
def remove_whitespace(value):
    return value.strip()

# Define the ImdbMovie item class
class ImdbMovie(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(
        input_processor=MapCompose(extract_year),
        output_processor=TakeFirst()
    )
    duration = scrapy.Field(
        input_processor=MapCompose(extract_duration),
        output_processor=TakeFirst()
    )
    director = scrapy.Field(output_processor=TakeFirst())
    genre = scrapy.Field(input_processor=MapCompose(str.strip), 
                         output_processor=Join(','))
    rating = scrapy.Field(output_processor=TakeFirst())
    summary = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    stars = scrapy.Field(input_processor=MapCompose(str.strip),
                        output_processor=Join(','))
    votes = scrapy.Field(output_processor=TakeFirst())
    num_user_reviews = scrapy.Field(output_processor=TakeFirst())
    num_critic_reviews = scrapy.Field(output_processor=TakeFirst())