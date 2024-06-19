import scrapy
import json

url = "https://www.lse.ac.uk/api/delivery/projects/website/entries/search"

params = {
    'linkDepth': '1',
    'orderBy': '[{"asc":"lsecYear"}]',
    'pageIndex': '0',
    'pageSize': '3',
    'where': '[{"field":"sys.versionStatus","equalTo":"published"},{"or":[{"field":"includeInSearch","equalTo":true},{"field":"includeInSearch","exists":false}]},{"or":[{"and":[{"not":[{"field":"searchDataUrl","contains":"/archive"}]},{"not":[{"field":"searchDataUrl","contains":"/Archive"}]}]},{"field":"searchDataUrl","exists":false}]},{"not":[{"field":"sys.uri","contains":"/archive/"}]},{"not":[{"field":"sys.uri","contains":"/Archive/"}]},{"not":[{"field":"sys.uri","startsWith":"/LSE-test-area/"}]},{"not":[{"field":"sys.uri","startsWith":"/zenTest/"}]},{"not":[{"field":"sys.uri","startsWith":"/Test/"}]},{"not":[{"field":"sys.uri","startsWith":"/test3/"}]},{"not":[{"field":"sys.uri","startsWith":"/Test-NS/"}]},{"and":[{"field":"sys.dataFormat","equalTo":"entry"},{"field":"sys.contentTypeId","in":["lseCourse"]}]}]'
}

headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Accept': '*/*',
  'Sec-Fetch-Site': 'same-origin',
  'Accept-Language': 'en-GB,en;q=0.9',
  'Accept-Encoding': 'gzip, deflate, br',
  'Sec-Fetch-Mode': 'cors',
  'Host': 'www.lse.ac.uk',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15',
  'accesstoken': 'gnIlDXEa99dkods6o6PZfZ3vAVrBqeUecgrywqZ00SUDwRi7'
}

class LseSpider(scrapy.Spider):
    name = "lse"
    allowed_domains = ["lse.ac.uk"]
    # start_urls = ["https://www.lse.ac.uk/programmes/search-courses?pageIndex=1"]

    def start_requests(self):
        for i in range(1, 30):
            params['pageIndex'] = str(i)
            yield scrapy.FormRequest(url, method='GET', headers=headers, 
                                                formdata=params,
                                                callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        yield data