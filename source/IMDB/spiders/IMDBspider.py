import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from IMDB.items import ImdbMovie

class IMDBSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?release_date=2010-01-01,2023-04-03&user_rating=7.5,10.0&num_votes=1000000,']

    def parse(self, response):
        movies = response.xpath('//div[@class="lister-item-content"]')
        for movie in movies:
            link = movie.css('a::attr(href)').get()
            yield response.follow(link, self.parse_detail)

        # Go to the next page
        next_page = response.css('.next-page::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)


    def parse_detail(self, response):

        item_loader = ItemLoader(item=ImdbMovie(), response=response)

        # Obtener título de la película
        title = response.css("h1[data-testid='hero__pageTitle'] span::text").get()
        item_loader.add_value('title', title)
        
        # Obtener año de lanzamiento de la película
        year = response.css('a.ipc-link--baseAlt[href*="/releaseinfo"]::text').get()
        item_loader.add_value('year', year)
        
        # Obtener duración de la película
        # duration = response.css('.TitleBlockMetaData__ListItemText-sc-12ein40-2:nth-child(3)::text').get()
        duration = response.xpath('//li[contains(@class, "ipc-inline-list__item")]/text()').get()
        item_loader.add_value('duration', duration)
        
        # Obtener géneros de la película
        # Extraer géneros usando expresión de CSS
        genre = response.css('div.ipc-chip-list__scroller span.ipc-chip__text::text').extract()
        item_loader.add_value('genre', genre)
        
        # Obtener calificación de la película
        rating = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span[@class="sc-e457ee34-1 squoh"]/text()').get()
        item_loader.add_value('rating', rating)
        
        # Obtener cantidad de votos de la película
        votes = response.xpath('//div[@class="sc-e457ee34-0 kqTStR"]/div[@class="sc-e457ee34-3 frEfSL"]/text()').get()
        item_loader.add_value('votes', votes)
        
        # Obtener la descripción de la película
        # summary = response.css('.GenresAndPlot__Plot-cum89p-6 > span::text').get()
        summary = response.css('span[data-testid="plot-xs_to_m"]::text').extract_first()
        item_loader.add_value('summary', summary)

        # Obtener num_user_reviews
        num_user_reviews = response.css('a[href*="/reviews/"] .score::text').get()
        item_loader.add_value('num_user_reviews', num_user_reviews)

        # Obtener num_user_reviews
        num_critic_reviews = response.css('a[href*="/externalreviews/"] .score::text').get()
        item_loader.add_value('num_critic_reviews', num_critic_reviews)

        for cast_item in response.css('a[data-testid="title-cast-item__actor"]'):
            star = cast_item.css('::text').get()
            item_loader.add_value('stars', star)

        item = item_loader.load_item()
        print(item)

        yield item
