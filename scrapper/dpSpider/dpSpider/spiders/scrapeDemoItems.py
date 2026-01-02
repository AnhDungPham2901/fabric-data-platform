from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import DemoItem


class DemoSpider(CrawlSpider):
    name = "demo"
    allowed_domains = ["anhdungpham2901.github.io"]
    start_urls = [
        "https://anhdungpham2901.github.io/scrapping-demo-website/"
    ]

    rules = [
        Rule(
            LinkExtractor(allow=r"detail_\d+\.html"),
            callback="parse_item",
            follow=False,
        )
    ]

    def parse_item(self, response):
        item = DemoItem()

        item["item_name"] = response.css("h1.title::text").get()
        item["item_url"] = response.url
        item["item_price"] = response.css(
            'li[data-key="price"]::text'
        ).get()
        item["item_category"] = response.css(
            'li[data-key="category"]::text'
        ).get()
        item["item_status"] = response.css(
            'li[data-key="stock"]::text'
        ).get()
        return item
