import scrapy
import csv

def UTF8 (data):
	try:
		return data.encode('utf-8', 'ignore')
	except:
		return data

class UrbanSpider(scrapy.Spider):
	name = "school"

	start_urls = [
		'https://www.urbanpro.com/legacy-school-bangalore-bangalore/2454',
	]

	def parse (self, response):
		logo = response.css('div.schoolLogo img::attr(src)').extract_first()
		logo = UTF8(logo.strip().replace(' ','').replace('\n','').replace('\t',''))
	
		name = response.css('h1.schoolTitle ::text').extract_first()
		name = UTF8(name.strip().replace(' ','').replace('\n','').replace('\t',''))

		address = ''
		temp = response.css('div.schoolAddress p ::text').extract()
		for i in temp:
			address = address + i.strip().replace(' ','').replace('\n','').replace('\t','')
		address = UTF8(address)

		phone = ''
		temp = response.css('p.addressDetail ::text').extract()
		for i in temp:
			phone = phone + i.strip().replace('\n','').replace('\t','')
		phone = UTF8(phone)

		board = ''
		temp = response.css('div.schoolBoard div.floatLeft::text').extract()
		for i in temp:
			board = board + i.strip().replace(' ','').replace('\t','').replace('\n','')
		board = UTF8(board)

		overview = ''
		temp = response.css('div.schoolOverview p ::text').extract()
		for i in temp:
			overview = overview + i.strip().replace('\n','').replace('\t','')
		overview = UTF8(overview)

		image = []
		temp = response.css('div.galleryImageContainer a::attr(href)').extract()
		for i in temp:
			image.append(UTF8(i.strip().replace(' ','').replace('\n','').replace('\t','')))

		review = []
		temp = response.css('p.reviewComment ::text').extract()
		for i in temp:
			review.append(UTF8(i.strip().replace('\n','').replace('\t','')))

		with open('school.csv', 'w') as csvfile:
			fieldnames = [
				'Logo',
				'Name',
				'Address',
				'Phone',
				'Board or Medium',
				'Overview',
				'Image',
				'Reviews'
			]

			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
			writer.writeheader()
			writer.writerow({
				'Logo': logo,
				'Name': name,
				'Address': address,
				'Phone': phone,
				'Board or Medium': board,
				'Overview': overview,
				'Image': image,
				'Reviews': review
				})