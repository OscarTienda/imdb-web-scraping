# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
# from scrapy.loader.processors import MapCompose, TakeFirst
from itemloaders.processors import MapCompose, TakeFirst

def remove_newline(value):
    return value.strip('\n').strip()

def remove_whitespace(value):
    return value.strip()

# class ImdbMovie(scrapy.Item):
#     title = scrapy.Field(
#         input_processor=MapCompose(remove_newline),
#         output_processor=TakeFirst()
#     )
#     year = scrapy.Field(
#         input_processor=MapCompose(remove_whitespace),
#         output_processor=TakeFirst()
#     )
#     duration = scrapy.Field(
#         input_processor=MapCompose(remove_whitespace),
#         output_processor=TakeFirst()
#     )
#     rating = scrapy.Field(
#         input_processor=MapCompose(remove_whitespace),
#         output_processor=TakeFirst()
#     )
#     genre = scrapy.Field(
#         input_processor=MapCompose(remove_newline)
#     )
#     summary = scrapy.Field(
#         input_processor=MapCompose(remove_newline),
#         output_processor=TakeFirst()
#     )
#     stars = scrapy.Field()
#     votes = scrapy.Field(
#         input_processor=MapCompose(remove_whitespace),
#         output_processor=TakeFirst()
#     )
#     num_user_reviews = scrapy.Field()
#     num_critic_reviews = scrapy.Field()

class ImdbMovie(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(output_processor=TakeFirst())
    genre = scrapy.Field(input_processor=MapCompose(str.strip))
    rating = scrapy.Field(output_processor=TakeFirst())
    duration = scrapy.Field(output_processor=TakeFirst())
    summary = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    stars = scrapy.Field(input_processor=MapCompose(str.strip))
    votes = scrapy.Field(output_processor=TakeFirst())
    num_user_reviews = scrapy.Field(output_processor=TakeFirst())
    num_critic_reviews = scrapy.Field(output_processor=TakeFirst())