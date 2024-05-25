import scrapy

class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css('div.ui-search-result__content') #54 item

        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall()
            cents = product.css('span.andes-money-amount__cents::text').getall()

            yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),  
                'name': product.css('h2.ui-search-item__title::text').get(),
                'old_price_reais_1': prices[0] if len(prices) > 0 else None,
                'new_price_centavos_1': cents[0] if len(cents) > 0 else None,
                'old_price_reais_2': prices[1] if len(prices) > 1 else None,
                'new_price_centavos_2': cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get()
            }

        # Correção na indentação para incluir este bloco dentro da função parse
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
