import scrapy
from bs4 import BeautifulSoup
import csv

def UTF8 (data):
	try:
		return data.encode('utf-8', 'ignore')
	except:
		return data


class UrbanSpider(scrapy.Spider):
	name = "parse_school_main"

	start_urls = [
		'https://www.urbanpro.com/',
	]

	custom_settings = {
		'CONCURRENT_REQUESTS':  '1000000',
		'CONCURRENT_REQUESTS_PER_DOMAIN' : '1000000',
		'CONCURRENT_REQUESTS_PER_IP' : '1000000'
	}

	def parse(self, response):
		print "Scrapping Urbanpro, please wait..."

		with open('school.csv', 'w') as f:
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

			writer = csv.DictWriter(f,fieldnames=fieldnames, dialect=csv.excel)
			writer.writeheader()

		categories = response.css('div.shdwPart a::attr(href)').extract()

		
		flag = 0

		future_url =""

		for i, var in enumerate(categories):
			if flag == 1:
				try:
					yield scrapy.Request(response.urljoin(var), callback=self.parse_city)
					print "scraping a city, link: ",response.urljoin(var),"\n\n"
					#inp = input()
				except:
					print "\n\n",var,"\n\nplease hit a button to continue"
					inp=input()
			elif var == unicode('/all-categories'):
				flag = 1
				all_categories = response.urljoin(var)

		#yield scrapy.Request(response.urljoin(all_categories), callback=self.parse_all_categories)

	def parse_city(self, response):

		print "link: ",response,"\n\n"
		nextpages = response.css('div.popularBlock').extract()

		for f, nextpage in enumerate(nextpages):
			soup = BeautifulSoup(nextpage,'html.parser')
			length = len(soup.find_all('a'))

			if f == 0:
				for i in range(length):
					yield scrapy.Request(response.urljoin(soup.find_all('a')[i]['href']), callback=self.parse_categories_schools)

	
	def parse_categories_schools(self, response):
		
		#print "inside parse_categories_schools: ",response,"\n\n"

		#members = response.css('div.listing-image-box a::attr(href)').extract()
		#print "members previous: ",members,"\n\n"
		members = response.css('div.schoolDataContainer a::attr(href)').extract()
		#print "members new: ",members,"\n\n"
		for i in members:
			yield scrapy.Request(response.urljoin(i),callback=self.parse_school)

		members = response.css('div.alsoSeeSchools a::attr(href)').extract()
		#print "Also see schools: ",members,"\n\n"
		for i in members:
			yield scrapy.Request(response.urljoin(i), callback=self.parse_categories_schools_alsoSee)

	def parse_categories_schools_alsoSee(self, response):
		
		#print "inside parse_categories_schools: ",response,"\n\n"

		#members = response.css('div.listing-image-box a::attr(href)').extract()
		#print "members previous: ",members,"\n\n"
		members = response.css('div.schoolDataContainer a::attr(href)').extract()
		#print "members new: ",members,"\n\n"
		for i in members:
			yield scrapy.Request(response.urljoin(i),callback=self.parse_school)




	def parse_school (self, response):
		print "School: ",response,"\n\n"

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

		with open('school.csv', 'a') as csvfile:
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