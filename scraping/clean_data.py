from functions import *
import pandas as pd

# city = "Durham"
# city_abbreviated = "Durham"
# state = "North Carolina" 
# state_initials = "NC"

# f_name = "{}_{}2.csv".format(city_abbreviated.lower(), state_initials.lower())

f_name = "data.csv"

data = pd.read_csv(f_name, \
	names=['restaurant_name', 'restaurant_address', 'menu_item',\
	'price', 'description', 'phone_number', 'page_link', 'image_link', 'num_ratings',\
	'tasty_rating', 'timely_rating', 'correct_rating', 'delivery_min', 'delivery_hours',\
	'pickup_hours', 'city', 'state']) 

restaurants = set(data['restaurant_name'])

modified_data = []

for restaurant in restaurants:

	address = list(data['restaurant_address'][data['restaurant_name'] == restaurant])[0]

	items = list(data['menu_item'][data['restaurant_name'] == restaurant])
	prices = list(data['price'][data['restaurant_name'] == restaurant])
	descriptions = list(data['description'][data['restaurant_name'] == restaurant])
	phone_number = list(data['phone_number'][data['restaurant_name'] == restaurant])[0]
	page_link = list(data['page_link'][data['restaurant_name'] == restaurant])[0]
	image_link = list(data['image_link'][data['restaurant_name'] == restaurant])[0]
	num_ratings = list(data['num_ratings'][data['restaurant_name'] == restaurant])[0]
	tasty_rating = list(data['tasty_rating'][data['restaurant_name'] == restaurant])[0]
	timely_rating = list(data['timely_rating'][data['restaurant_name'] == restaurant])[0]
	correct_rating = list(data['correct_rating'][data['restaurant_name'] == restaurant])[0]
	city = list(data['city'][data['restaurant_name'] == restaurant])[0]
	state = list(data['state'][data['restaurant_name'] == restaurant])[0]
	# delivery_min = list(data['delivery_min'][data['restaurant_name'] == restaurant])[0]

	ratings = [num_ratings, tasty_rating, timely_rating, correct_rating]

	menu_items = set()
	for i in range(len(items)):
		name = items[i]
		price = prices[i]
		description = descriptions[i]
		menu_item = MenuItem(name, price, description)

		menu_items.add(menu_item)

	restaurant_obj = Restaurant(restaurant, address, menu_items, \
	phone_number, page_link, image_link, ratings, city, state)

	modified_data.append(restaurant_obj)

# sort objects by restaurant name
# modified_data = sorted(modified_data, key=lambda x: x.restaurant_name)

# r = modified_data[7]
# items = r.items
# print (r.restaurant_name)
# for item in items:
# 	print (item)

#create insert statements 

restaurant_ids = {}

# insert statement statements for Restaurants table
restaurant_insert_statement = "INSERT INTO Restaurants\nVALUES\n"
for i, restaurant in enumerate(modified_data):
	restaurant_insert_statement += "\t({}, {}, {}, '{}', '{}', {}, {}, {}, {}, {}, {}),\n".format(i+1, \
		restaurant.restaurant_name, restaurant.address, restaurant.city, restaurant.state, \
		restaurant.phone_number, \
		restaurant.page_link, restaurant.image_link, restaurant.tasty_rating, \
		restaurant.timely_rating, restaurant.correct_rating)
	restaurant_ids[restaurant.restaurant_name] = i+1

restaurant_insert_statement = restaurant_insert_statement.rstrip().strip(",")
restaurant_insert_statement += "\n\tON CONFLICT DO NOTHING;"
# print (restaurant_insert_statement)

dish_insert_statement = "INSERT INTO Dishes\nVALUES\n"
for i, restaurant in enumerate(modified_data):
	restaurant_id = restaurant_ids[restaurant.restaurant_name]
	menu_items = restaurant.items
	for item in menu_items:
		dish_insert_statement +="\t({}, {}, {}, {}),\n".format(restaurant_id, \
			item.item_name, item.description, item.price)

dish_insert_statement = dish_insert_statement.rstrip().strip(",") + ";"
dish_insert_statement += "\n\tON CONFLICT DO NOTHING;"

ingredient_count = {}

ingredient_set = set()

dish_contains_insert_statement = "INSERT INTO DishContains\nVALUES\n"
for i, restaurant in enumerate(modified_data):
	restaurant_id = restaurant_ids[restaurant.restaurant_name]
	menu_items = restaurant.items
	for item in menu_items:
		if item.description != "NULL":
			ingredients = item.ingredients
			for ingredient in ingredients:

				ingredient_set.add(ingredient)

				if ingredient not in ingredient_count:
					ingredient_count[ingredient] = 0

				ingredient_count[ingredient] += 1

				dish_contains_insert_statement +="\t({}, {}, '{}'),\n".format(restaurant_id, \
					item.item_name, ingredient)

dish_contains_insert_statement = dish_contains_insert_statement.rstrip().strip(",") 
dish_contains_insert_statement += "\n\tON CONFLICT DO NOTHING;"

ingredient_statement = "INSERT INTO Ingredients\nVALUES\n"
for ingredient in ingredient_set:
	ingredient_statement += "\t('{}'),\n".format(ingredient)

ingredient_statement = ingredient_statement.rstrip().strip(",") 
ingredient_statement += "\n\tON CONFLICT DO NOTHING;"

# sorted_ingredients = sorted(ingredient_count.items(), key=lambda x: x[1], reverse=True)

# print (sorted_ingredients[:200])

# print (dish_contains_insert_statement)

creates = open("create_tables.sql", 'r').read()

output = open("statements.sql", "w")
output.write(creates)
output.write("\n\n" + restaurant_insert_statement)
output.write("\n\n" + dish_insert_statement)
output.write("\n\n" + ingredient_statement)
output.write("\n\n" + dish_contains_insert_statement)
output.close()





