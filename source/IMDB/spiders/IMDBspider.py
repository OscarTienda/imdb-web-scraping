import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from IMDB.items import ImdbMovie

class IMDBSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?release_date=2000-01-01,2023-04-03&user_rating=0.0,10.0&num_votes=150000,&sort=user_rating,asc']

    # Parse the main list of movies and tv shows. From now on the term movie references both movies and tv shows.
    def parse(self, response):
        # Get all movie containers in the current page
        movies = response.xpath('//div[@class="lister-item-content"]')
        for movie in movies:
            # Extract votes, rating, and duration for each movie
            votes = movie.xpath('.//span[@name="nv"]/@data-value').get()
            rating = response.css('.ratings-bar .inline-block.ratings-imdb-rating > strong::text').get()
            duration = movie.xpath('.//span[@class="runtime"]/text()').get()

            # Get the detail page link and follow it
            link = movie.css('a::attr(href)').get()
            yield response.follow(link, self.parse_detail, meta={'votes': votes, 'rating': rating, 'duration': duration})

        # Go to the next page if available
        next_page = response.css('.next-page::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Parse the movie detail page
    def parse_detail(self, response):
        # Create an ItemLoader to fill the ImdbMovie item
        item_loader = ItemLoader(item=ImdbMovie(), response=response)

        # Extract and add various movie attributes to the ItemLoader
        title = response.css("h1[data-testid='hero__pageTitle'] span::text").get()
        item_loader.add_value('title', title)
        
        # Extract the release year of the movie
        year = response.css('a.ipc-link--baseAlt[href*="/releaseinfo"]::text').get()
        item_loader.add_value('year', year)
        
        # Add the duration of the movie, obtained from the previous parse method
        duration = response.meta['duration']
        item_loader.add_value('duration', duration)
        
        # Extract genres of the movie
        genre = response.css('div.ipc-chip-list__scroller span.ipc-chip__text::text').extract()
        item_loader.add_value('genre', genre)
        
        # Add the movie rating, obtained from the previous parse method
        rating = response.meta['rating']
        item_loader.add_value('rating', rating)
        
        # Add the number of votes, obtained from the previous parse method
        votes = response.meta['votes']
        item_loader.add_value('votes', votes)

        # Add the movie URL
        url = response.url
        item_loader.add_value('url', url)

        # Extract the movie summary
        summary = response.css('span[data-testid="plot-xs_to_m"]::text').extract_first()
        item_loader.add_value('summary', f'"{summary}"')

        # Extract the number of user reviews
        num_user_reviews = response.css('a[href*="/reviews/"] .score::text').get()
        item_loader.add_value('num_user_reviews', num_user_reviews)

        # Extract the movie director
        director = response.css('li[data-testid="title-pc-principal-credit"] a::text').get()
        item_loader.add_value('director', director)

        # Extract the number of critic reviews
        num_critic_reviews = response.css('a[href*="/externalreviews/"] .score::text').get()
        item_loader.add_value('num_critic_reviews', num_critic_reviews)

        # Extract the movie stars
        for cast_item in response.css('a[data-testid="title-cast-item__actor"]'):
            star = cast_item.css('::text').get()
            item_loader.add_value('stars', star)

        # Load the item and print it
        item = item_loader.load_item()
        print(item)

        yield item
