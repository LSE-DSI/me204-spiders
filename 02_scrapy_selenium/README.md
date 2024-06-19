## Setup

Here we are building on the previous project, where we scraped the LSE website for information on their degrees. We will now use Selenium to scrape the same information, but this time we will be able to interact with the website and click on the links for pagination. 

It is important to note that Selenium will almost always be slower than pure Scrapy, but it provides us with a way around some restrictions where the website requires the client to be able to render JavaScript to load the HTML content.

This is usually a sign that the website relies on an API under the hood, and how you can take advantage of this will be covered in the next section.

## Other uses for Selenium

Selenium might be more useful in some distinct cases when you need an actual browser to obtain some cookies and headers that are dynamic and cannot be imitated by Scrapy.

For example, if you need to scrape a website that requires you to log in, you can use Selenium to open a browser, log in, and then pass the cookies to Scrapy to continue scraping.


