import scrapy
from urllib.parse import urljoin

class IIITUSpider(scrapy.Spider):
    name = "iiitu"
    start_urls = ["https://iiitu.ac.in/"]
    allowed_domains = ["iiitu.ac.in"]

    visited = set()

    def parse(self, response):
        self.visited.add(response.url)

        # Extract text
        text = response.xpath("//body//text()").getall()

        # Extract tables
        tables = response.xpath("//table").getall()

        # Extract images
        images = response.xpath("//img/@src").getall()

        # Extract PDFs
        pdfs = response.xpath("//a[contains(@href,'.pdf')]/@href").getall()

        yield {
            "url": response.url,
            "text": text,
            "tables": tables,
            "images": images,
            "pdfs": pdfs
        }

        # Follow links
        links = response.xpath("//a/@href").getall()
        for link in links:
            full_url = urljoin(response.url, link)

            if "iiitu.ac.in" in full_url and full_url not in self.visited:
                yield scrapy.Request(full_url, callback=self.parse)