from typing import Iterable, Any

from scrapy import Request, Spider

class DemoSpider(Spider):
    name = "demoSpider"

    def start_requests(self) -> Iterable[Any]:
        urls = [
            "https://anhdungpham2901.github.io/scrapping-demo-website/"
        ]
        return [Request(url=url, callback=self.parse) for url in urls]

    def parse(self, response):
        url = response.url
        title = response.css("h1::text").extract_first()
        print(f"URL is: {url}")
        print(f"Title is: {title}")
