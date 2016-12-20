import scrapy
from bs4 import BeautifulSoup
import csv

def UTF8 (data):
	try:
		return data.encode('utf-8', 'ignore')
	except:
		return data

class UrbanSpider(scrapy.Spider):
	name = "parse_tutor_main"

	start_urls = [
		'https://www.urbanpro.com/',
	]

	def parse(self, response):
		print "Scrapping Urbanpro, please wait..."

		with open('urbanpro.csv', 'w') as f:
			fieldnames = [
				'Image',
				'Name',
				'featured',
				'Location',
				'Region',
				'Country',
				'Pincode',
				'About Us',
				'Category',
				'Gallery',
				'Details',
				'Information',
				'Reviews'
			]

			writer = csv.DictWriter(f,fieldnames=fieldnames, dialect=csv.excel)
			writer.writeheader()

		categories = response.css('div.shdwPart a::attr(href)').extract()

		city_names = response.css('div.shdwPart a::text').extract()
		
		flag = 0

		for i , var in enumerate(city_names):
			if flag == 1:
				filename = 'output/'+var.strip() + '.csv'
				filename = filename.lower()
				with open(filename, 'w') as f:
					fieldnames = [
						'Image',
						'Name',
						'featured',
						'Location',
						'Region',
						'Country',
						'Pincode',
						'About Us',
						'Category',
						'Gallery',
						'Details',
						'Information',
						'Reviews'
					]
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

		#yield scrapy.Request(response.urljoin(all_categories), callback=self.parse_all_categories)

	def allCategories(self, response):
		categories = response.css('ul.list a::attr(href)').extract()

		for var in categories:
			yield scrapy.Request(response.urljoin(var),callback=self.categories)

		categories = response.css('a.nextLink::attr(href)').extract()
		yield scrapy.Request(response.urljoin(var),callback=self.allCategories)


	def categories(self, response):
		categories = response.css('div.atCity a::attr(href)').extract()
		
		#to include special members here later

		for var in categories:
			try:
				yield scrapy.Request(response.urljoin(var),callback=self.parse_category)
			except:
				yield scrapy.Request(response.urljoin(var),callback=self.categories)


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
				continue
			else:
				for i in range(length):
					yield scrapy.Request(response.urljoin(soup.find_all('a')[i]['href']), callback=self.parse_category)

	def parse_category(self, response):

		print "tutors: ",response,"\n\n"

		members = response.css('div.listing-image-box a::attr(href)').extract()

		for member in members:
			responding = response.urljoin(member)
			try:
				yield scrapy.Request(responding, callback=self.parse_members)
			except:
				print "\nfailed:\n",responding,"\n\n"
				inp=input()

		try:
			members = response.css('#nearLocality li a::attr(href)').extract()

			for member in members:
				responding = response.urljoin(member)
				try:
					yield scrapy.Request(responding, callback=self.parse_city)
				except:
					print "\nfailed:\n",responding,"\n\n"
					inp = input()
		except:
			print "no nearbyLocality"


		try:
			members = response.css('#nearByCityInSEOFooter li a::attr(href)').extract()

			for member in members:
				responding = response.urljoin(member)
				try:
					yield scrapy.Request(responding, callback=self.parse_members)
				except:
					print "\nfailed:\n",responding,"\n\n"
					inp = input()
		except:
			print "no nearByCityInSEOFooter"


	def parse_members(self, response):
		#stores image of the tutor
		tutor_image = response.css('div.profileImageHeader img::attr(src)').extract_first().strip()
		tutor_image = UTF8(tutor_image)

		#stores name of the tutor
		tutor_name = response.css('div.rightProfileHead h1::text').extract_first().strip()
		tutor_name = UTF8(tutor_name)
		#check if featured or not
		try:	
			featured = response.css('span.membershipTag ::text').extract_first().strip()
			featured = 'YES'
		except:
			featured = 'NO'

		#get location of tutor
		tutor_location = response.css('span.locality ::text').extract_first().strip()
		tutor_location = UTF8(tutor_location.replace('\n',' ').replace('\t',' '))

		#get region of tutor
		tutor_region = response.css('span.region ::text').extract_first().strip()
		tutor_region = UTF8 (tutor_region.replace('\n',' ').replace('\t',' '))

		#get country-name of tutor
		tutor_country = response.xpath('//span[@class="country-name."]/text()').extract_first().strip()
		tutor_country = UTF8(tutor_country)


		#get pincode of tutor
		tutor_pincode = response.css('span.postal-code ::text').extract_first().strip()
		tutor_pincode = UTF8 (tutor_pincode)

		#get aboutUs Section of tutor
		tutor_aboutUs = response.css('div.description_txt ::text').extract_first().strip()
		tutor_aboutUs = UTF8(tutor_aboutUs)
	
		#get categories of tutor
		tutor_categ = []
		tutor_categ = response.css('span.categText::text').extract()
		for i, temp in enumerate(tutor_categ):
			tutor_categ[i] = UTF8(temp.strip().replace(' ','').replace('\n',''))
	
		#get gallery start_urls
		tutor_gallery = []
		tutor_gallery = response.css('div.galleryHolder a::attr(href)').extract()
		for i, temp in enumerate(tutor_gallery):
			tutor_gallery[i] = UTF8(temp.strip().replace(' ','').replace('\n',''))
	

		#for profile_details
		tutor_details = response.css('div.profileContentTxt p::text').extract_first().strip()
		tutor_details = UTF8(tutor_details)
	

		#for more information
		tutor_info = response.css('div.profileContentTxt p ::text').extract_first().strip()
		tutor_info = UTF8(tutor_info.replace('\n','').replace('\t','').replace('\r',''))
	

		#for reviews
		temp = response.css('p.reviewContent::text').extract()
		tutor_reviews = []
		for i in range(1,len(temp),2):
			tutor_reviews.append(UTF8(temp[i].strip().replace('\n','').replace('\t','').replace('\r','')))
	
		city = tutor_region.lower().replace(' ','').replace('\t','').replace('\n','')
		filename = "output/"+city+".csv"

		with open(filename, 'a') as csvfile:
			fieldnames = [
							'Image',
							'Name',
							'featured',
							'Location',
							'Region',
							'Country',
							'Pincode',
							'About Us',
							'Category',
							'Gallery',
							'Details',
							'Information',
							'Reviews'
						]			
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
			writer.writerow({
				'Image': tutor_image,
				'Name':tutor_name,
				'featured':featured,
				'Location': tutor_location,
				'Region' : tutor_region,
				'Country' : tutor_country,
				'Pincode': tutor_pincode,
				'About Us': tutor_aboutUs,
				'Category': tutor_categ,
				'Gallery': tutor_gallery,
				'Details': tutor_details,
				'Information': tutor_info,
				'Reviews': tutor_reviews
				})
		with open('urbanpro.csv', 'a') as csvfile:
			fieldnames = [
							'Image',
							'Name',
							'featured',
							'Location',
							'Region',
							'Country',
							'Pincode',
							'About Us',
							'Category',
							'Gallery',
							'Details',
							'Information',
							'Reviews'
						]		
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=csv.excel)
			writer.writerow({
				'Image': tutor_image,
				'Name':tutor_name,
				'featured':featured,
				'Location': tutor_location,
				'Region' : tutor_region,
				'Country' : tutor_country,
				'Pincode': tutor_pincode,
				'About Us': tutor_aboutUs,
				'Category': tutor_categ,
				'Gallery': tutor_gallery,
				'Details': tutor_details,
				'Information': tutor_info,
				'Reviews': tutor_reviews
				})
