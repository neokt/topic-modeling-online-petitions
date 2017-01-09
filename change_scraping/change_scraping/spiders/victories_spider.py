import scrapy
import pickle as pk

items = {}

class victoriesSpider(scrapy.Spider):
	name = 'victories'

	custom_settings = {"DOWNLOAD_DELAY": 1,
	"CONCURRENT_REQUESTS_PER_DOMAIN": 2,
	"BOT_NAME": 'pet',
	}

	def __init__(self, filename=None):
		if filename:
			with open(filename, 'rb') as f:
				self.start_urls = pk.load(f)
		self.output_filename = filename[:-4]

	def parse(self, response):  
		try:
			header = response.xpath('//div[@data-content = "petition-title"]')
			petition_id = header.xpath('.//div[@class="num-decision-maker-responses-badge display-inline-block"]/@data-petition_id').extract()[0]
			petition_title = header.xpath('//h1[@class = "xs-mtn xs-mbl"]/text()').extract()[0]

			# petitioner and all decision makers! last = petitioner, first = primary decision maker
			people = header.xpath('.//div[@class = "type-ellipsis"]/strong/text()').extract()
			petitioner = people[-1]
			primary_decision_maker = people[0]
			other_decision_makers = people[1:-1] # should be empty list if this is not 0

			# petitioner location (if does not exist, is an organization)
			try:
				petitioner_location = header.xpath('.//span[@class = "plxxs type-weak type-ellipsis"]/text()').extract()[0]
				petitioner_type = 'person'
			except:
				petitioner_location = ''
				petitioner_type = 'organization'

			# # getting # of signatures
			# signatures = response.xpath('//div[@class = "js-sign-and-share-components"]')

			# number of signatures
			supporters = response.xpath('//div[@class="col-xs-4 type-s js-mobile-supporter-count"]/strong/text()').extract()[0].replace(',','')

			# number remaining and goal (need to get first and last)
			goal = supporters

			# list of tags (unindexed)
			tags = response.xpath('//li[@class = "man"]//a/@title').extract()

			# list of story paragraphs
			story_lines = response.xpath('//div[@class="rte js-description-content"]//text()').extract()
			story = filter(lambda x: x != '\n', story_lines)

			items[petition_id] = {'petition_title': petition_title,
			'petitioner': petitioner,
			'primary_decision_maker': primary_decision_maker,
			'other_decision_makers': other_decision_makers,
			'petitioner_location':  petitioner_location,
			'petitioner_type': petitioner_type,
			'supporters': supporters,
			'goal': supporters,
			'tags': tags,
			'story': story}
		except:
			pass
		
		with open(self.output_filename + '_save.pkl', 'wb') as f:
			pk.dump(items,f,-1)









