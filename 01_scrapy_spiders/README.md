# Scrapy Spiders

Scrapy is a powerful web scraping framework that allows you to extract data from websites in an asynchronous (\neq sequential) manner. It provides a lot of the same functionality as we've explored previously in the using the `requests` and `Scrapy Selector` modules, but it is more efficient and can handle more complex tasks. 

Let's compare spiders and requests:

<!-- md table to compare -->

|Characteristic| `requests` \+ `Scrapy Selectors`| `Scrapy` framework |
|---|---|---|
|**Asynchronous**| ❌| ✅ |
|**Pagination**| ❌| ✅|
|**Middleware**| ❌| ✅|
|**Pipelines**| ❌| ✅|
|**Caching**| ❌| ✅|
|**`robots.txt` settings**| ❌| ✅|
|**User-Agent settings**| ✅| ✅|
|**Built-in saving to JSON, CSV, JSONL etc.**| ❌| ✅|
|**Built-in `shell` for testing selectors**| ❌| ✅|
|**Built-in `crawl` command**| ❌| ✅|
|**Built-in `scrapyrt` for API**| ❌| ✅|


## Setup

Let's set up a Scrapy project to scrape the LSE website for information on their degrees.

```shell 
scrapy startproject lse_degrees lse.ac.uk
```

```shell 
cd lse.ac.uk
scrapy genspider lse lse.ac.uk
```

Now navigate to the `spiders` directory and open the `lse.py` file, where you will see the following code:

```python
import scrapy


class LseSpider(scrapy.Spider):
    name = "lse"
    allowed_domains = ["lse.ac.uk"]
    start_urls = ["https://lse.ac.uk"]

    def parse(self, response):
        pass
```

We will need to replace the `start_urls` list with the following: 

```python
    start_urls = [f"https://www.lse.ac.uk/programmes/search-courses?pageIndex={str(x)}" for x in range(1, 30)]
```

to deal with the pagination. 

## Using the Scrapy Shell to test your selectors

Before we start writing our spider, let's test our selectors using the Scrapy shell. To do this, run the following command:

```shell
scrapy shell "https://www.lse.ac.uk/programmes/search-courses"
```

Try the following selector:

```python
response.css('.card__content ::text').getall()
```

Recall what the space ` ` does in a CSS selector: it selects all descendants, not just the direct children. 

Once you are satisfied with your selectors, you can close the shell by typing `exit()`.

## Spider structure

A spider is a class that Scrapy uses to scrape information from a website, and whenever you generate a new one, it will always forllow the same template. 

1. The `name` attribute is the name of the spider.
2. The `allowed_domains` attribute is a list of websites (not necessarily pages) the spider is allowed to scrape.
3. The `start_urls` attribute is a list of URLs that the spider will start scraping from.
4. The `parse` method is the method that will be called to handle the response downloaded for each of the requests made.

You can add other parsing methods such as `parse_item`, `parse_details`, etc. to handle different types of responses.

Each parsing method should yield a dictionary with the data you want to scrape. In our case, let's focus on degree titles, links, and start dates. 

Since a spider is a class, you cannot run it directly from the command line. Instead, you need to use the `crawl` command. 

```shell
scrapy crawl lse
```

This will run the spider and output the scraped data to the console, but you can also save it to a file by using the `-o` flag. The format will be inferred from the file extension, and you can use `json`, `jsonl`, `csv`, `xml`.

```shell
scrapy crawl lse -o degrees.jsonl
```

A lowercase `-o` will append to the existing file, while an uppercase `-O` will overwrite it. 

## Pagination 

If you have multiple pages to scrape, you can use the `parse` method to extract the links to the next pages and then yield a `Request` object to scrape them. This page does not have a url for the next page, a button needs to be clicked--we will cover this in headless scraping. If it did, the code would look something like:

```python
class LseSpider(scrapy.Spider):
    # ...
    def parse(self, response):
        # ...

        next_page = response.css("button[aria-label^='Go to next page']")
        # ^= means starts with

        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
```

The `callback=self.parse` argument tells Scrapy to call the `parse` method with the response from the next page. It does not need brackets `()` because we are passing a reference to the method, not calling it.




