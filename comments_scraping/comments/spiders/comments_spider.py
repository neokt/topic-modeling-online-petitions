import scrapy
import pickle as pk
from time import sleep
import os
import ast

d_pet = {}
fails = []

class commentsSpider(scrapy.Spider):
	name = 'comments'

	chromedriver = '/usr/bin/'
	os.environ['webdriver.chrome.driver'] = chromedriver

	custom_settings = {"DOWNLOAD_DELAY": 1,
	"CONCURRENT_REQUESTS_PER_DOMAIN": 2,
	"BOT_NAME": 'comm',
	}

	def __init__(self, filename=None):
		if filename:
			with open(filename, 'rb') as f:
				urls = pk.load(f)
				self.start_urls = [url + '/c' for url in urls]
		self.output_filename = filename[:-4]

	def parse(self, response):
		d_comm = {}
		
		try:
			petition_holder = response.xpath('//div[@data-view="petitions/comments/index"]/@data-fetch_summary').extract()
			petition_id = ast.literal_eval(petition_holder[0])['petition']['id']

			try:
				comments_holder = response.xpath('//div[@class="js-show-comments-top-rated"]')
				comments = comments_holder.xpath('.//div[@data-view="components/comments_feed/comment_card"]')

				for comment in comments:
					comment_id = ast.literal_eval(comment.xpath('@data-fetch_summary').extract()[0])['model']['id']
					comment_text = comment.xpath('.//p[@class="type-break-word mbxs"]/text()').extract()[0]
					commenter_name = comment.xpath('.//div[@class="col-xs-8"]/strong/text()').extract()[0]
					commenter_location = comment.xpath('.//div[@class="col-xs-8"]/span[@class="type-weak"]/text()').extract()[0][2:]
					comment_date = comment.xpath('.//div[@class="col-xs-4 txt-r"]/span[@class="type-weak"]/span[@class="link-stealth"]/text()').extract()[0]
					comment_hearts = comment.xpath('.//div[@class="type-s mvxxs"]/span/text()').extract()[0]

					d_comm[comment_id] = {'comment_text': comment_text,
					'commenter_name': commenter_name,
					'commenter_location': commenter_location,
					'comment_date': comment_date,
					'comment_hearts': comment_hearts}
			except:
				d_comm = "No Comments"

			d_pet[petition_id] = d_comm

			with open(self.output_filename + '_comments.pkl', 'wb') as f:
				pk.dump(d_pet,f,-1)

		except:
			fails.append(response.url)
			with open(self.output_filename + '_fails.pkl', 'wb') as f:
				pk.dump(fails,f,-1)   

        

        



