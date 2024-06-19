import scrapy
from selenium import webdriver


class LseSpider(scrapy.Spider):
    name = "lse"
    allowed_domains = ["lse.ac.uk"]
    start_urls = ["https://www.lse.ac.uk/programmes/search-courses?pageIndex=1"]

    def parse(self, response):
        cards = response.css('.card__content')
        
        # next_page = response.css("button[aria-label^='Go to next page']").get()
        # click the button to go to the next page
        driver = webdriver.Chrome()
        driver.get(response.url)
        driver.find_element_by_css_selector("button[aria-label^='Go to next page']").click()
        # get the new url
        response = driver.page_source
        driver.quit()


        for card in cards:
            yield {
                "original_url": response.url,
                "degree_type": card.css("span.study-type ::text").get(),
                "degree_url": card.css('h2 > a::attr(href)').get(),
                "date": card.css(".card__infoTag::text").get(),
            }

        # This page does not have a url for the next page, a button needs to be clicked--we will cover this in headless scraping. If it did, we would use the following code:
        # if next_page:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)