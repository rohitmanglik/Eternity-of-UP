import scrapy
import csv

def UTF8 (data):
	try:
		return data.encode('utf-8', 'ignore')
	except:
		return data

class UrbanSpider(scrapy.Spider):
	name = "path_1"

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

		categories = response.css('p.footext a::attr(href)').extract()
		flag = 0
		for var in categories:
			if flag == 0:
				yield scrapy.Request(response.urljoin(var),callback=self.categories)
			elif var == unicode('/all-categories'):
				yield scrapy.Request(response.urljoin(var),callback=self.allCategories)
				flag = 1
			elif flag == 1:
				yield scrapy.Request(response.urljoin(var),callback=self.cities)

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
				yield scrapy.Request(response.urljoin(var),callback=self.group)
			except:
				yield scrapy.Request(response.urljoin(var),callback=self.categories)


	def cities(self, response):
		categories = response.css('div.popularBlock a::attr(href)').extract()

		for var in categories:
			yield scrapy.Request(response.urljoin(var),callback=self.group)

		categories = response.css('div.nearByCity a::attr(href)').extract()

		for var in categories:
			yield scrapy.Request(response.urljoin(var),callback=self.cities)

	def group(self, response):
		categories = response.css('div.listing-card-box a::attr(href)').extract()

		for var in categories:
			yield scrapy.Request(response.urljoin(var),callback=self.tutor)


	def tutor(self, response):
		#stores image of the tutor
		tutor_image = response.css('div.profileImageHeader img::attr(src)').extract_first()
		if tutor_image is not None:
			tutor_image = tutor_image.strip()
		tutor_image = UTF8(tutor_image)

		#stores name of the tutor
		tutor_name = response.css('div.rightProfileHead h1::text').extract_first()
		if tutor_name is not None:
			tutor_name = tutor_name.strip()
		tutor_name = UTF8(tutor_name)
		#check if featured or not
		try:	
			featured = response.css('span.membershipTag ::text').extract_first()
			if featured is not None:
				featured = featured.strip()
			featured = 'YES'
		except:
			featured = 'NO'

		#get location of tutor
		try:
			tutor_location = response.css('span.locality ::text').extract_first()
			tutor_location = UTF8(tutor_location.replace('\n',' ').replace('\t',' '))
		except:
			tutor_location = ''


		#get region of tutor
		try:
			tutor_region = response.css('span.region ::text').extract_first()
			tutor_region = UTF8 (tutor_region.replace('\n',' ').replace('\t',' '))
		except:
			tutor_region = ''


		#get country-name of tutor
		try:
			tutor_country = response.xpath('//span[@class="country-name."]/text()').extract_first()
			if tutor_country is not None:
				tutor_country = tutor_country.strip()
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
