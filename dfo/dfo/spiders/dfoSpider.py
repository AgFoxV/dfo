import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
import time
from dfo.items import DfoItem

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome()
wait = ui.WebDriverWait(browser,150)

class DfoSpider(scrapy.Spider):

	name = "dfo"
	start_urls = [
		'http://www.baidu.com'
	]

	def parse(self,response):

		browser.get('http://fsl-bsf.summon.serialssolutions.com/en/search?q=&ho=t&l=en&wb-srch-sub=&fvf=SourceType%2CLibrary+Catalog%2Cf%7CLibrary%2CDFO-MPO%2Cf#!/search?ho=t&fvf=SourceType,Library%20Catalog,f%7CLibrary,DFO-MPO,f%7CContentType,Book%20%2F%20eBook,f%7CContentType,Journal%20%2F%20eJournal,f%7CContentType,Government%20Document,f%7CContentType,Conference%20Proceeding,f%7CContentType,Journal%20Article,f%7CContentType,Book%20Chapter,f%7CContentType,Paper,f%7CContentType,Dissertation,f%7CLanguage,English,f&rf=PublicationDate,2004-12-30:2017-12-31&l=en&q=')
		
		while True:
			article_urls = wait.until(lambda browser: browser.find_elements_by_class_name('ng-scope'))

			for url in article_urls:
				try:
					if 'searchscope' in url.get_attribute('href'):
						with open('11.txt','a+') as f:
							f.write(url.get_attribute('href') + "\n")
				
						yield scrapy.Request(url = url.get_attribute('href'),callback = self.parse_content)
				except:
					print ('item has no arrt named "href"')
			browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
			

	def parse_content(self,response):

		item = DfoItem()
		pdf_url = response.xpath('//*[@id="resource-links"]/ul/li/a/@href').extract_first()
		with open('112.txt','a+') as f:
			f.write(response.url + "\n")
		
		item['pdf_url'] = pdf_url

		yield scrapy.Request(url = pdf_url)


