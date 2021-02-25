# -*- coding: utf-8 -*-
import scrapy

# [1]
from trabalho.items import AsascarItem

# [2]
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re


class G1Spider(CrawlSpider):
    name = 'g1'

    # dominios permitidos
    allowed_domains = [
        'g1.globo.com'

    ]

    # Onde começar a busca
    start_urls = [
        'https://g1.globo.com/tudo-sobre/bndes/',
        'https://g1.globo.com/tudo-sobre/eletrobras/',
        'https://g1.globo.com/tudo-sobre/ibge/'
    ]

    # Regras para a extração de itens
    rules = [
        Rule(LinkExtractor(allow=['eletrobras','bndes','ibge'], deny=['2018', '2017', '2016', '2015', '2014', '2013']),
             callback=('parse_item'), follow=True)
    ]

    #  Função de callback que será executada para todas as urls encontradas
    def parse_item(self, response):
        # [8]
        sel = Selector(response)

        # [9]
        item = AsascarItem()

        # Aqui é onde era feito a antiga separação, porém ela era limitada a um padrão de item
        #item['url'] = response.url
        #item['categoria'] = response.url.split("/")[-6]
        #item['mes'] = response.url.split("/")[6]
        #item['dia'] = response.url.split("/")[7]
        #item['ano'] = response.url.split("/")[5]
        #item['titulo'] = response.url.split("/")[8]

        # essa linha extraí o conteúdo:
        #item['conteudo'] = sel.xpath('normalize-space(//article)').extract_first()

        # [10] Aqui é feito a separação da url usando / como parametro para gerar titulo e data
        contador = 0
        item['url'] = response.url
        urltemp = response.url.split("/")
        while (contador < len(urltemp)):
            temp = urltemp[contador]
            if 'ibge' in temp or 'bndes' in temp or 'eletrobras' in temp:
                item['titulo'] = urltemp[contador]
                contador = contador + 1
            elif '2020' in temp or '2019' in temp:
                item['ano'] = urltemp[contador]
                item['mes'] = urltemp[contador + 1]
                item['dia'] = urltemp[contador + 2]
                contador = contador + 1
            else:
                contador = contador + 1

        # [11]
        yield item
