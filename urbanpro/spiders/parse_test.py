import scrapy
import csv

def UTF8 (data):
	try:
		return data.encode('utf-8', 'ignore')
	except:
		return data

class UrbanSpider(scrapy.Spider):
	name = "path"

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
		
		for i, var in enumerate(categories):
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_categories)
			#yield scrapy.Request(response.urljoin(var), callback=self.parse_cities)

	
	def parse_categories(self, response):
		sub_categ = response.css('ul li a::attr(href)').extract()
		print sub_categ
		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_categories_1)
			#print "\n\ncontrol flowed to category_1\n\n"
			#inp = input()
			yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_cities)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_group)
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_class)

		sub_categ = response.css('div.articleCard a::attr(href)').extract()

		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_categories_1)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_cities)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_group)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_class)

	def parse_categories_1(self,response):
		sub_categ = response.css('div.articleCard a::attr(href)').extract()
		print sub_categ
		#inp = input()
		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_cities)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_group)
			yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_class)


	def parse_cities(self,response):
		sub_categ = response.css('recentContainer a::attr(href)').extract()

		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_class)

		sub_categ = response.css('div.popularDiv a::attr(href)').extract()

		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_group)

		sub_categ = response.css('div.nearByCity a::attr(href)').extract()

		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_cities)

	def parse_group(self,response):
		sub_categ = response.css('div.listing-card-box a::attr(href)').extract()

		for var in sub_categ:
			yield scrapy.Request(response.urljoin(var),callback=self.parse_tutor)
			#yield scrapy.Request(response.urljoin(var),callback=self.parse_class)


	def parse_tutor(self, response):
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
		try:
			tutor_location = response.css('span.locality ::text').extract_first().strip()
			tutor_location = UTF8(tutor_location.replace('\n',' ').replace('\t',' '))
		except:
			tutor_location = ''


		#get region of tutor
		try:
			tutor_region = response.css('span.region ::text').extract_first().strip()
			tutor_region = UTF8 (tutor_region.replace('\n',' ').replace('\t',' '))
		except:
			tutor_region = ''


		#get country-name of tutor
		try:
			tutor_country = response.xpath('//span[@class="country-name."]/text()').extract_first().strip()
			tutor_country = UTF8(tutor_country)
		except:
			tutor_country = ''

		#get pincode of tutor
		try:
			tutor_pincode = response.css('span.postal-code ::text').extract_first().strip()
			tutor_pincode = UTF8 (tutor_pincode)
		except:
			tutor_pincode = ''

		#get aboutUs Section of tutor
		try:
			tutor_aboutUs = response.css('div.description_txt ::text').extract_first().strip()
			tutor_aboutUs = UTF8(tutor_aboutUs)
		except:
			tutor_aboutUs = ''


		#get categories of tutor
		try:
			tutor_categ = []
			tutor_categ = response.css('span.categText::text').extract()
			for i, temp in enumerate(tutor_categ):
				tutor_categ[i] = UTF8(temp.strip().replace(' ','').replace('\n',''))
		except:
			tutor_categ = []

		#get gallery start_urls
		try:
			tutor_gallery = []
			tutor_gallery = response.css('div.galleryHolder a::attr(href)').extract()
			for i, temp in enumerate(tutor_gallery):
				tutor_gallery[i] = UTF8(temp.strip().replace(' ','').replace('\n',''))
		except:
			tutor_gallery = []		

		#for profile_details
		try:
			tutor_details = response.css('div.profileContentTxt p::text').extract_first().strip()
			tutor_details = UTF8(tutor_details)
		except:
			tutor_details = ''		

		#for more information
		try:
			tutor_info = response.css('div.profileContentTxt p ::text').extract_first().strip()
			tutor_info = UTF8(tutor_info.replace('\n','').replace('\t','').replace('\r',''))
		except:
			tutor_info = ''		

		#for reviews
		try:
			temp = response.css('p.reviewContent::text').extract()
			tutor_reviews = []
			for i in range(1,len(temp),2):
				tutor_reviews.append(UTF8(temp[i].strip().replace('\n','').replace('\t','').replace('\r','')))
		except:
			tutor_reviews = ''


		city = tutor_region.lower().replace(' ','').replace('\t','').replace('\n','')

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


##############################################################
