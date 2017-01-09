import scrapy
import pickle as pk

items = {}

class petitionsSpider(scrapy.Spider):
	name = 'petitions'

	custom_settings = {"DOWNLOAD_DELAY": 1,
	"CONCURRENT_REQUESTS_PER_DOMAIN": 2,
	"BOT_NAME": 'pet',
	}

	def __init__(self, filename=None):
		if filename:
			with open(filename, 'rb') as f:
				self.start_urls = pk.load(f)
		self.output_filename = filename[:-4]

	# def start_requests(self):
	# 	# urls = ['https://www.change.org/p/president-of-the-united-states-the-penalty-of-love-let-people-who-has-a-disability-to-get-married', 
	# 	# 'https://www.change.org/p/democratic-national-committee-shorten-the-us-presidential-election-cycle',
	# 	# 'https://www.change.org/p/remove-sheriff-kyle-kirchmeier-from-the-morton-county-sheriff-s-office']

	# 	for url in urls: # scale up to all urls afterwards
	# 		yield scrapy.Request(url=url, callback=self.parse)

    # # from scrapy tutorial        
    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'petitions-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

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

			# getting # of signatures
			signatures = response.xpath('//div[@class = "js-sign-and-share-components"]')

			# number of signatures
			supporters = signatures.xpath('.//div[@class = "type-s type-weak"]/text()').extract()[0].split()[0].replace(',','')

			# number remaining and goal (need to get first and last)
			goal = signatures.xpath('.//div[@class = "txt-r"]/text()').extract()[0].split()[-1].replace(',','')

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
			'goal': goal,
			'tags': tags,
			'story': story}
		except:
			pass
		
		with open(self.output_filename + '_save.pkl', 'wb') as f:
			pk.dump(items,f,-1)
	 #   	# # comments
	   	# comments = response.xpath('//a[@class = "link-block"]')
	   	# for comment in comments:
	   	# 	pass









