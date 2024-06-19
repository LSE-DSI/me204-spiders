# Scrapy Spiders

Scrapy is a powerful web scraping framework that allows you to extract data from websites in an asynchronous ($\neq$ sequential) manner. It provides a lot of the same functionality as we've explored previously in the using the `requests` and `Scrapy Selector` modules, but it is more efficient and can handle more complex tasks. 

Let's compare `spiders` and `requests`:

<!-- md table to compare -->

|Characteristic| `requests` \+ `Scrapy Selectors`| `Scrapy` framework |
|---|---|---|
|**Asynchronous**| ❌| ✅ |
|**Built-in pagination**| ❌| ✅|
|**Middleware and pipelines**[^1]| ❌| ✅|
|**Caching**[^2]| ❌| ✅|
|**`robots.txt` settings**[^3]| ❌| ✅|
|**User-Agent settings**| ✅| ✅|
|**Built-in saving to JSON, CSV, JSONL etc.**| ❌| ✅|
|**Built-in `shell` for testing selectors**[^4]| ❌| ✅|
|**Built-in `crawl` command**| ❌| ✅|
|**Boilerplate code generation**[^5]| ❌| ✅|
|**Intergration with headless browsers**[^6]| ❌| ✅|
|**Built-in sitemap parsers and link extractors**[^7]| ❌| ✅|
|**Works well in Jupyter Notebooks**| ✅| ❌|
|**Built-in `FormRequest` for submitting forms**[^8]| ❌| ✅|
|**Integration with `scrapyd` for cloud deployment**[^9]| ❌| ✅|


[^1]: Middleware and pipelines are used to process requests and responses before and after they are sent and received, respectively.
[^2]: Caching is the process of storing data in a temporary storage area so that it can be accessed more quickly.
[^3]: `robots.txt` is a file that tells search engine crawlers which pages or files the crawler can or can't request from your site.
[^4]: The Scrapy shell is a powerful tool for testing your CSS selectors and XPath expressions in the terminal. 
[^5]: Scrapy can generate boilerplate code for a new spider, project, or item.
[^6]: Scrapy can be used with headless browsers like Puppeteer and Playwright to scrape websites that require JavaScript to render.
[^7]: Scrapy has built-in classes for parsing `sitemap.xml` (eg. [LSE sitemap](https://www.lse.ac.uk/sitemap.xml)) and extracting links.
[^8]: Scrapy has a `FormRequest` class that can be used to submit forms.
[^9]: `scrapyd` is a service for running, scheduling, and monitoring Scrapy spiders in the cloud.

# Scapy architecture

Spiders are not just a single file, but a collection of files that work together to scrape a website. The main components of a spider are:

|#|Component|Functionality|
|---|---|---|
|1|`items.py`|Defines the data structure that will be scraped.|
|2|`middlewares.py`|Processes requests and responses before and after they are sent and received.|
|3|`pipelines.py`|Processes the scraped data before it is saved to a file or database.|
|4|`settings.py`|Contains the configuration settings for the spider.|
|5|`spiders/`|Contains the spider classes that will scrape the website.|

> [!TIP]
> We will not be dealing with `middlewares`, `pipelines`, or `items` in this tutorial, but they are important components of a Scrapy project––do not delete them. 

## `Spider` class

> [!IMPORTANT]  
> **Spiders are not functions!** They have to be instantiated and invoked by the Scrapy framework. So, if with `request` you were able to run a Jupyter Notebook cell, with Scrapy you will instead need to perform a `scrapy crawl` command in the terminal and specify the output file and its format, eg. `scrapy crawl your_spider_name -o output.jsonl`.

A class represents a blueprint for an object and is a collection of attributes ($\eq$ properties associated with an object) and methods ($\eq$ functions associated with an object). In Scrapy, a spider is a class that inherits from the `scrapy.Spider` class and has the following attributes:

1. `name`: The name of the spider.
2. `allowed_domains`: A list of domains that the spider is allowed to scrape.
3. `start_urls`: A list of URLs that the spider will start scraping from.
4. `parse`: The method that will be called to handle the response downloaded for each of the requests made, for example, `parse_page`, `parse_item`, etc. 

> [!IMPORTANT]  
> There can be multiple parse methods depending on the structure of the website being scraped.
> Each parse method **should `yield` (not `return`) a dictionary** with the data you want to scrape.
> **Dictionaries are the best data structure** for these data, but they can nest lists and other dictionaries.

# Getting to business

## Setup

Let's set up a Scrapy project to scrape the LSE website for information on their degrees.

```shell 
scrapy startproject lse_degrees lse.ac.uk
```

```shell 
cd lse.ac.uk
scrapy genspider lse lse.ac.uk
```

Now navigate to the `spiders` directory (use the `cd` command in the terminal) and open the `lse.py` file, where you will see the following code:

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
> [!TIP]
> <details>
> <summary>Recall what the space ` ` does in a CSS selector:</summary>
it selects all descendants, not just the direct children. 
> </details>

Once you are satisfied with your selectors, copy them to your spider and close the shell by typing `exit()`.

## Spider structure

A spider is a class that Scrapy uses to scrape information from a website, and whenever you generate a new one, it will always forllow the same template. 

1. The `name` attribute is the name of the spider.
2. The `allowed_domains` attribute is a list of websites (not necessarily pages) the spider is allowed to scrape.
3. The `start_urls` attribute is a list of URLs that the spider will start scraping from.
4. The `parse` method is the method that will be called to handle the response downloaded for each of the requests made.

You can add other parsing methods such as `parse_item`, `parse_details`, etc. to handle different types of responses.

Each parsing method should yield **either a dictionary** with the data you want to scrape **or another request** if you are dealing with multiple pages. In our case, let's focus on degree titles, links, and start dates. 

Since a spider is a class, you cannot run it directly from the command line. Instead, you need to use the `crawl` command. 

```shell
scrapy crawl lse
```

This will run the spider and output the scraped data to the console, but you can also save it to a file by using the `-o` flag. The format will be inferred from the file extension, and you can use `json`, `jsonl`, `csv`, `xml`.

```shell
scrapy crawl lse -o degrees.jsonl
```

A lowercase `-o` will **append** to the existing file, while an uppercase `-O` will **overwrite** it. 

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
            yield scrapy.Request(next_page, callback=self.parse) # callback means call the parse method with the response from the next page
```

The `callback=self.parse` argument tells Scrapy to call the `parse` method with the response from the next page. It does not need brackets `()` because we are passing a reference to the method, not calling it.




