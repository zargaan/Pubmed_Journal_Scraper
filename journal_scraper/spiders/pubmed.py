import scrapy
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class PubMedSpider(scrapy.Spider):
    name = 'pubmed_spider'
    allowed_domains = ['pubmed.ncbi.nlm.nih.gov']
    start_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term=information+system']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
        'RETRY_TIMES': 2,
        'MAX_PAGES': 5,
        'CONCURRENT_REQUESTS': 1,
        'HTTPCACHE_ENABLED': False,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 4,
        'FEEDS': {
            'shared_data/scraping_hasil_is.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'indent': 4,
                'overwrite': True
            }
        },
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={'page_number': 1, 'max_pages': self.settings.getint('MAX_PAGES', 5)}
        )

    def parse(self, response):
        page_number = response.meta['page_number']
        max_pages = response.meta['max_pages']

        self.logger.info(f"📄 Parsing halaman ke-{page_number} dari {max_pages} halaman")

        articles = response.css('div.docsum-content')
        for article in articles:
            title_parts = article.css('a.docsum-title ::text').getall()
            title = self.clean_text(title_parts)
            
            meta_data = {
                'title': title,
                'authors': self.extract_authors(article),
                'citation': article.css('span.docsum-journal-citation::text').get('').strip()
            }

            detail_link = article.css('a.docsum-title::attr(href)').get()
            full_url = response.urljoin(detail_link)
            yield response.follow(full_url, callback=self.parse_detail, meta=meta_data)

        # Pagination yang dikontrol manual
        if page_number < max_pages:
            next_page = page_number + 1
            next_url = self.build_next_url(response.url, next_page)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse,
                meta={'page_number': next_page, 'max_pages': max_pages}
            )

    def parse_detail(self, response):
        item = {
            'title': response.meta['title'],
            'abstract': self.extract_abstract(response),
            'authors': response.meta['authors'],
            'journal_conference_name': self.extract_journal(response.meta['citation']),
            'publisher': 'PubMed',
            'year': self.extract_year(response.meta['citation']),
            'doi': self.extract_doi(response),
            'group_name': self.extract_group(response)
        }
        yield item

    def clean_text(self, text_list):
        return ' '.join(''.join(text_list).split()).strip()

    def extract_authors(self, article):
        authors_text = article.css('span.docsum-authors.full-authors::text').get('')
        return [a.strip() for a in authors_text.split(',') if a.strip()]

    def extract_abstract(self, response):
        paragraphs = response.css('div.abstract-content.selected p::text').getall()
        return ' '.join([p.strip() for p in paragraphs if p.strip()]) or 'Unavailable'

    def extract_journal(self, citation):
        return citation.split('.')[0].strip() if citation else 'Unavailable'

    def extract_year(self, citation):
        if match := re.search(r'\b(19|20)\d{2}\b', citation):
            return int(match.group())
        return None

    def extract_doi(self, response):
        doi = response.css('meta[name="citation_doi"]::attr(content)').get()
        return doi.rstrip('.') if doi else 'Unavailable'

    def extract_group(self, response):
        return "Kelompok Nyasar"

    def build_next_url(self, current_url, next_page):
        parsed = urlparse(current_url)
        query = parse_qs(parsed.query)
        query['page'] = [str(next_page)]
        new_query = urlencode(query, doseq=True)
        return urlunparse(parsed._replace(query=new_query))
