import pandas as pd
import nltk

class MenuItem:
	def __init__(self, item_name, price, description):
		self.item_name = self.clean_item_name(item_name)
		self.price = self.clean_price(price)
		self.description = self.clean_description(description)

	def __eq__(self, other):
		
		if type(other) is type(self):
			return self.item_name == other.item_name
		
		else:
			return False

	def __hash__(self):
		
		return hash((self.item_name))

	def __str__(self):
		if self.description == "NULL":
			return ("{} selling for ${} with the following description: {}".format(self.item_name, self.price, self.description))

		else:
			return ("{} selling for ${}.".format(self.item_name, self.price))

	def clean_string(self, var):
		''' remove innner quotes, semi-colons, and add quotes around var '''

		var = var.replace("'","")
		var = var.replace("\"","")
		var = var.replace(";","")
		var = "'" + var + "'"
		
		return var

	def get_ingredients(self, description):
		
		is_noun = lambda pos: pos[:2] == 'NN'
		tokenized = nltk.word_tokenize(description)

		item_name = self.item_name.replace("'","")

		tokenized2 = nltk.word_tokenize(item_name)

		nouns = [word.lower().rstrip('s') for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
		nouns += [word.lower().rstrip('s') for (word, pos) in nltk.pos_tag(tokenized2) if is_noun(pos)]
		
		return set(nouns)

	def clean_item_name(self, item_name):

		if pd.isnull(item_name):
			item_name = "NULL"

		else:
			item_name = self.clean_string(item_name)

		return item_name

	def clean_description(self,description):

		if pd.isnull(description):
			description = "NULL"
			self.ingredients = []

		else:
			description = self.clean_string(description)
			self.ingredients = self.get_ingredients(description[1:-1])

		return description

	def clean_price(self, price):

		if pd.isnull(price):
			price = "NULL"
			return price

		if "$" in price:
			price = price.strip("$")

		return price

class Restaurant:
	def __init__(self, restaurant_name, address, items, \
		phone_number, page_link, image_link, ratings, city, state):

		self.restaurant_name = self.clean_name(restaurant_name)
		self.address = self.clean_string(address)
		self.items = items
		self.phone_number = self.clean_phone_number(phone_number)
		self.page_link = self.clean_page_link(page_link)
		self.image_link = self.clean_image_link(image_link)
		self.get_ratings(ratings)
		self.city = city
		self.state = state

	def clean_string(self, var):
		''' remove innner quotes, semi-colons, and add quotes around var '''

		var = var.replace("'","")
		var = var.replace("\"","")
		# var = var.replace("(","")
		# var = var.replace(")","")
		# var = var.replace("#","")
		var = var.replace(";","")
		var = "'" + var + "'"
		
		return var

	def clean_name(self, restaurant_name):
		
		restaurant_name = self.clean_string(restaurant_name)

		return ''.join(i for i in restaurant_name if not i.isdigit()).strip("()").strip(" ")

	def clean_phone_number(self, phone_number):
		if pd.isnull(phone_number):
			phone_number = "NULL"

		else:
			phone_number = "'" + phone_number + "'"

		return phone_number

	def clean_page_link(self, page_link):
		if pd.isnull(page_link):
			page_link = "NULL"

		else:
			page_link = "'" + page_link + "'"

		return page_link

	def clean_image_link(self, image_link):
		if pd.isnull(image_link):
			image_link = "NULL"

		else:
			image_link = "'" + image_link + "'"

		return image_link

	def get_ratings(self, ratings):

		num_ratings = ratings[0]

		if pd.isnull(num_ratings):
			num_ratings = "NULL"

		else:
			num_ratings = num_ratings.split(" ")[0]

		self.num_ratings = num_ratings

		other_ratings = ratings[1:]

		for i in range(len(other_ratings)):
			r = other_ratings[i]
			if pd.isnull(r):
				other_ratings[i] = "NULL"
			else:
				other_ratings[i] = str(int(r))

		self.tasty_rating, self.timely_rating, self.correct_rating = other_ratings







