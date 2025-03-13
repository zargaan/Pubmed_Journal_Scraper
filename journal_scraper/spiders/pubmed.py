import scrapy
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class PubMedSpider(scrapy.Spider):
    name = 'pubmed'
    start_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term=machine%20learning']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 3,
        'AUTOTHROTTLE_ENABLED': True,
        'RETRY_TIMES': 2,
        'MAX_PAGES': 5,
        'CONCURRENT_REQUESTS': 1,
        'HTTPCACHE_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
    }

    def start_requests(self):
        self.logger.info("🔥 Memulai scraping PubMed")
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse,
            meta={'page_number': 1, 'max_pages': self.settings.getint('MAX_PAGES', 5)},
            headers={'Referer': 'https://pubmed.ncbi.nlm.nih.gov/'}
        )

    def parse(self, response):
        current_page = response.meta['page_number']
        max_pages = response.meta['max_pages']
        
        articles = response.css('.docsum-content')
        self.logger.info(f"📖 Halaman {current_page} - Artikel ditemukan: {len(articles)}")

        # Ekstraksi data
        for result in articles:
            yield self.parse_article(response, result, current_page)

        # Pagination logic
        if current_page < max_pages and len(articles) > 0:
            next_page = current_page + 1
            next_url = self.build_next_url(response.url, next_page)
            
            self.logger.info(f"⏭ Membangun URL halaman {next_page}: {next_url}")
            
            yield response.follow(
                next_url,
                callback=self.parse,
                meta={'page_number': next_page, 'max_pages': max_pages},
                headers={'Referer': response.url},
                errback=self.handle_error
            )

    def build_next_url(self, current_url, next_page):
        parsed = urlparse(current_url)
        query = parse_qs(parsed.query)
        
        # Parameter paginasi yang benar untuk PubMed
        query['page'] = [str(next_page)]
        
        # Bersihkan parameter yang mengganggu
        for param in ['format', 'size', 'filter', 'start']:
            query.pop(param, None)
        
        new_query = urlencode(query, doseq=True)
        return urlunparse(parsed._replace(query=new_query))

    def parse_article(self, response, selector, page):
        return {
            'title': self.clean_text(selector.css('.docsum-title ::text').getall()),
            'authors': self.clean_authors(selector.css('.docsum-authors::text').get()),
            'journal': self.parse_journal(selector.css('.docsum-journal-citation::text').get()),
            'pmid': selector.css('.docsum-pmid::text').get('').strip(),
            'page': page,
            'url': response.urljoin(selector.css('a.docsum-title::attr(href)').get())
        }

    def clean_text(self, text_list):
        return ' '.join(''.join(text_list).split()).strip()

    def clean_authors(self, authors):
        if authors:
            return re.sub(r'(\.\.\.|;|\bet al\b\.?)', '', authors).strip()
        return ''

    def parse_journal(self, journal_text):
        if journal_text:
            return {
                'name': journal_text.split('.')[0],
                'year': self.extract_year(journal_text),
                'citation': journal_text.strip()
            }
        return {}

    def extract_year(self, text):
        try:
            match = re.search(r'\b(19|20)\d{2}\b', text)
            return int(match.group()) if match else None
        except:
            return None

    def handle_error(self, failure):
        self.logger.error(f"🚨 Gagal memproses halaman: {failure.request.url}")
        self.logger.error(f"🚨 Detail error: {repr(failure)}")