import scrapy
from bs4 import BeautifulSoup
import csv

class UrbanSpider(scrapy.Spider):
	name = "parse_main"

	start_urls = [
		'https://www.urbanpro.com/',
	]

	def parse(self, response):
		with open('urbanpro.csv','a') as f:
			fieldnames = ['name', 'profileContent', 'locality', 'region', 'country', 'postalCode', 'aboutUs', 'galleryImage', 'classesConducted', 'image', 'reviews']
			writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=csv.excel)
			writer.writeheader()

		categories = response.css('div.shdwPart a::attr(href)').extract()

		city_names = response.css('div.shdwPart a::text').extract()
		
		flag = 0

		for i , var in enumerate(city_names):
			if flag == 1:
				filename = var.strip() + '.csv'
				filename = filename.lower()
				with open(filename, 'a') as f:
					fieldnames = ['name', 'profileContent', 'locality', 'region', 'country', 'postalCode', 'aboutUs', 'galleryImage', 'classesConducted', 'image', 'reviews']
					writer = csv.DictWriter(f, fieldnames=fieldnames, dialect=csv.excel)
					writer.writeheader()
			elif var == unicode('All Categories'):
				flag = 1

		flag = 0

		future_url =""

		for i, var in enumerate(categories):
			if flag == 1:
				try:
					yield scrapy.Request(response.urljoin(var), callback=self.parse_city)
				except:
					print "\n\n",var,"\n\n"
					inp=input()
			elif var == unicode('/all-categories'):
				flag = 1
				all_categories = response.urljoin(var)

		yield scrapy.Request(response.urljoin(all_categories), callback=self.parse_all_categories)



	def parse_all_categories(self, response):
		list_categories = response.css('ul.list li a::attr(href)').extract()

		for category in list_categories:
			yield scrapy.Request(response.urljoin(category), callback=self.parse_all_categories_city)

		paginates = response.css('div.paginateButtons a::attr(href)').extract()

		for paginate in paginates:
			yield scrapy.Request(response.urljoin(paginate), callback=self.parse_all_categories_city)


	def parse_all_categories_city(self,response):
		list_cities = response.css('div.atCity ul li a::attr(href)').extract()
		for city in list_cities:
			yield scrapy.Request(response.urljoin(city), callback=self.parse_category)




	def parse_city(self, response):

		#nextpages = response.css('div.popularBlock a::attr(href)').extract()

		#for nextpage in nextpages:
		#	try:
		#		yield scrapy.Request(response.urljoin(nextpage), callback=self.parse_category)
		#	except:
		#		print "\n\n",nextpages[0],"\n\n"
		#		inp=input()

		nextpages = response.css('div.popularBlock').extract()

		for f, nextpage in enumerate(nextpages):
			soup = BeautifulSoup(nextpage,'html.parser')
			length = len(soup.find_all('a'))

			if f == 0:
				for i in range(length):
					yield scrapy.Request(response.urljoin(soup.find_all('a')[i]['href']), callback=self.parse_categories_schools)

			else:
				for i in range(length):
					yield scrapy.Request(response.urljoin(soup.find_all('a')[i]['href']), callback=self.parse_category)


	def parse_categories_schools(self, response):
		members = response.css('div.listing-image-box a::attr(href)').extract()

		for member in members:
			responding = response.urljoin(member)
			try:
				yield scrapy.Request(responding, callback=self.parse_school)
			except:
				print "\nfailed:\n",responding,"\n\n"
				


	def parse_category(self, response):

		members = response.css('div.listing-image-box a::attr(href)').extract()

		for member in members:
			responding = response.urljoin(member)
			try:
				yield scrapy.Request(responding, callback=self.parse_members)
			except:
				print "\nfailed:\n",responding,"\n\n"
				inp=input()

	def parse_members(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip().encode('utf-8').replace("\n","").replace("\t","")

		image = extract_with_css('div.profileImageHeader img::attr(src)')
		name = extract_with_css('div.rightProfileHead h1::text')
		try:
			profileContent = extract_with_css('div.profileContentTxt::text')
			profileContent = profileContent.replace("\t","").replace("\n","").replace(" ","")
		except:
			profileContent = None
			print "\n\ndiv.profileContentTxt::text\n\n",response,"\n\n"
			#inp=input()
		try:
			locality = extract_with_css('span.locality::text')
			locality = locality.replace("\t","").replace("\n","").replace(" ","")
		except:
			locality = None
			print "\n\nspan.locality::text\n\n",response,"\n\n"
			#inp=input()

		try:
			region = extract_with_css('span.region::text')
			region = region.replace("\t","").replace("\n","").replace(" ","")
			filename = region.encode('utf-8') + '.csv'
			filename = filename.lower()
		except:
			region = None
			print "\n\nspan.region.txt\n\n",response,"\n\n"
			#inp=input()
		try:
			country = response.xpath('//span[@class="country-name."]/text()').extract_first().replace(" ","").replace("\n","").replace("\t","")
		except:
			country = None
			print "\n\ncountry not found\n\n",response,"\n\n"
			#inp=input()
		try:
			postalCode = extract_with_css('span.postal-code::text')
		except:
			postalCode = None
			print "\n\npostalCode Not found\n\n",response,"\n\n"
			#inp=input()
		try:
			aboutUs = extract_with_css('div.description_txt::text')
			aboutUs = aboutUs.replace("\t","").replace("\n","").replace(" ","")
		except:
			aboutUs = None
			print "\n\naboutUs not found\n\n",response,"\n\n"
			#inp=input()
		
		try:
			galleryImage = []
			galleryImage = galleryImage + response.css('div.galleryContainer a::attr(href)').extract()
			for e, var in enumerate(galleryImage):
				galleryImage[e] = var.strip().decode('utf-8','ignore').encode('utf-8')
				galleryImage[e] = var.replace("\t","").replace("\n","").replace(" ","")

		except:
			galleryImage = [None]
			print "\n\ngalleryImage Not found\n\n",response,"\n\n"
			#inp=input()

		try:
			classesConducted = []
			classesConducted = response.css('span.categText::text').extract()
			for e, var in enumerate(classesConducted):
				classesConducted[e] = var.strip().encode('utf-8').replace("\n","").replace("\t","").replace(" ","")
		except:
			classesConducted =[None]
			print "\n\nclasses not found\n\n",response,"\n\n"
			#inp=input()

		
		try:
			review = response.css('div.reviewContainer').extract()
			reviews = []

			for var in review:
				soup = BeautifulSoup(var, 'html.parser')
				reviews.append(soup.get_text().strip().replace("\t","").replace("\n",""))
		except:
			print "\n\nreviews\n\n",response,"\n\n"
			#inp=input()

			



		with open(filename, 'a') as csvfile:
			fieldnames = ['name', 'profileContent','locality','region','country','postalCode','aboutUs', 'galleryImage', 'classesConducted', 'image', 'reviews']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
			writer.writerow({'name': name, 'profileContent': profileContent, 'locality': locality, 'region': region, 'country': country, 'postalCode': postalCode, 'aboutUs': aboutUs, 'galleryImage': galleryImage, 'classesConducted': classesConducted, 'image': image, 'reviews':reviews})

		with open('urbanpro.csv', 'a') as csvfile:
			fieldnames = ['name', 'profileContent','locality','region','country','postalCode','aboutUs', 'galleryImage', 'classesConducted', 'image', 'reviews']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
			writer.writerow({'name': name, 'profileContent': profileContent, 'locality': locality, 'region': region, 'country': country, 'postalCode': postalCode, 'aboutUs': aboutUs, 'galleryImage': galleryImage, 'classesConducted': classesConducted, 'image': image, 'reviews':reviews})


	def parse_school(self, response):
		def extract_with_css(query):
			return response.css(query).extract_first().strip().replace("\t","").replace("\n","")

		name = extract_with_css('h1.schoolTitle::text')
		image = extract_with_css('div.schoolLogo img::attr(src)')
