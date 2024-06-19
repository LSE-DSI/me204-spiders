from selenium import webdriver
from scrapy import Selector
from pprint import pprint as print

url = "https://www.lse.ac.uk/programmes/search-courses?pageIndex=1"

def main(url):
    driver = webdriver.Chrome()
    response = start_requests(url, driver)
    while response:
        for item in process_page(response):
            print(item)
        response = paginate(response, driver)
    driver.quit()

def start_requests(url, driver: webdriver.Chrome):
    driver.get(url)
    response = Selector(text=driver.page_source)
    return response    

def paginate(response, driver: webdriver.Chrome):
    next_page = response.css("button[aria-label^='Go to next page']").get()
    if next_page:
        driver.find_element(by="css selector", value="button[aria-label^='Go to next page']").click()
        response = Selector(text=driver.page_source)
        return response
    else:
        return None

def process_page(response):
    cards = response.css('.card__content')
    for card in cards:
        yield {
            "degree_type": card.css("span.study-type ::text").get(),
            "degree_url": card.css('h2 > a::attr(href)').get(),
            "date": card.css(".card__infoTag::text").get(),
        }

if __name__ == "__main__":
    main(url)