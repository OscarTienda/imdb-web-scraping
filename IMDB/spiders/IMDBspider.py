import scrapy

class IMDBSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/search/title/?release_date=2010-01-01,2023-04-03&user_rating=7.5,10.0&num_votes=5000,&count=250']

    def parse(self, response):
        for movie in response.css('.lister-item-header a::attr(href)').getall():
            movie_url = response.urljoin(movie)
            yield scrapy.Request(movie_url, callback=self.parse_movie)

        # Go to the next page
        next_page = response.css('.next-page::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_movie(self, response):
        # Extract movie information
        writers_selector = 'div.ipc-metadata-list-item__content-container ul li'
        writer_elements = response.css(writers_selector)
    
        writers = []
        for writer_element in writer_elements:
            writer_name = writer_element.css('a.ipc-metadata-list-item__list-content-item::text').get()
            writers.append(writer_name)

        yield {
            'title': response.css('.sc-afe43def-1::text').get().strip(),
            'original_title': response.css('.sc-afe43def-3::text').get(),
            'year': response.css('.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color::text').get().strip(),
            'duration': response.css('li.ipc-inline-list__item time::text').get(),
            'presentation': response.css('.sc-35061649-0.fjlUgo::text').get().strip(),
            'director': response.css('a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link::text').get().strip(),
            'writers': writers
        }

