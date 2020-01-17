from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

### logging into MFA 
# driver = webdriver.Chrome(desired_capabilities=caps, executable_path="/usr/lib/chromium-browser/chromedriver")
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
driver.get("https://www.seamless.com/lets-eat") 

# enter address
address_field = driver.find_element_by_xpath('//*[@id="homepage-logged-out-top"]/ghs-welcome-view/div/div[2]/div[2]/div[2]/ghs-start-order-form/div/div[1]/div/div/ghs-address-input/div/div/div/input')

# street_address = "1616 Guadalupe St"
# city = "Austin"
# city_abbreviated = "Austin"
# state = "Texas" 
# state_initials = "TX"

# street_address = "27 West 4th Street"
# city = "New York"
# city_abbreviated = "NY"
# state = "New York"
# state_initials = "NY"

street_address = "749 9th St"
city = "Durham"
city_abbreviated = "Durham"
state = "North Carolina"
state_initials = "NC"

address_field.send_keys(street_address + ", " + city + ", " + state_initials)
address_field.send_keys(Keys.ENTER)

def get_data_from_restaurant(driver):

	check_for_pop_up2(driver)

	try:
		driver.find_element_by_xpath('//*[@id="chiri-modal"]/div[2]/div[2]/div[3]/a[2]').click()

	except:
		pass 

	restaurant_data = []
	restaurant_name = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[1]/h1').text.encode('cp1252').decode('utf-8')
	restaurant_address = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[2]/div[1]/div[1]/span/a').text.encode('cp1252').decode('utf-8')
	page_url = driver.current_url.encode('cp1252').decode('utf-8')
	image_link = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[1]/img').get_attribute('src').encode('cp1252').decode('utf-8')

	try:
		phone_number = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[2]/div[1]/div/ghs-restaurant-phone/a/span').text.encode('cp1252').decode('utf-8')
	
	except:
		phone_number = ""

	try:
		num_ratings = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[3]/ghs-popover/span/div/ghs-star-rating/div/span').text.encode('cp1252').decode('utf-8')
	
	except:
		num_ratings = ""

	try:
		tasty_rating = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[3]/ghs-rating-facets/div/div/ul/li[1]/span[1]').text.encode('cp1252').decode('utf-8')

	except:
		tasty_rating = ""

	try:
		timely_rating = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[3]/ghs-rating-facets/div/div/ul/li[2]/span[1]').text.encode('cp1252').decode('utf-8')
		
	except:
		timely_rating = ""

	try:
		correct_rating = driver.find_element_by_xpath('//*[@id="ghs-restaurant-summary"]/div/div/div/div[2]/div[3]/ghs-rating-facets/div/div/ul/li[3]/span[1]').text.encode('cp1252').decode('utf-8')
	
	except:
		correct_rating = ""

	try:
		delivery_min = driver.find_element_by_xpath('//*[@id="navSection-menu"]/div[3]/div/div/ghs-cart-header/header/ghs-cart-header-in-restaurant/ghs-simplified-address-change/div/div[1]/ghs-restaurant-large-fees/span/ghs-restaurant-fees/span/ghs-restaurant-delivery-min/span/span[1]').text.encode('cp1252').decode('utf-8')
	except:
		delivery_min = ""

	try:
		delivery_hours = driver.find_element_by_xpath('//*[@id="ghs-restaurant-about"]/div/div[2]/ghs-restaurant-hours/div/div[1]/div/div/span[2]').text.encode('cp1252').decode('utf-8')

	except:
		delivery_hours = ""

	try:
		pickup_hours = driver.find_element_by_xpath('//*[@id="ghs-restaurant-about"]/div/div[2]/ghs-restaurant-hours/div/div[1]/div/div[1]/span[2]').text.encode('cp1252').decode('utf-8')
	
	except:
		pickup_hours = ""


	# get all food items
	items = driver.find_elements_by_xpath("//*[contains(@class,'menuItem u-background')]")

	# get attributes from each food item
	for item in items:
		name = item.find_element_by_tag_name('a').get_attribute("title")
		price = item.find_element_by_xpath(".//span[@class='menuItem-displayPrice']").text.encode('cp1252').decode("utf-8")

		try:
			description = item.find_element_by_tag_name('p').text.encode('cp1252').decode("utf-8")

		except:
			description = ""

		restaurant_data.append([restaurant_name, restaurant_address, name, price, description, \
			phone_number, page_url, image_link, num_ratings, tasty_rating, timely_rating, \
			correct_rating, delivery_min, delivery_hours, pickup_hours, city, state])

	print ("{} done...".format(restaurant_name))

	return restaurant_data

def get_data_from_current_page(driver):
	
	data_from_page = []

	try:
		i = 1
		# open each restaurant
		while True:
			restaurant = driver.find_element_by_xpath('//*[@id="ghs-search-results-container"]/div/div[2]/div/div/ghs-search-results/div[1]/div/div[3]/div/ghs-impression-tracker/div/div[' + str(i) + ']')
			restaurant.click()
				
			try:
				restaurant_data = get_data_from_restaurant(driver)
				data_from_page += restaurant_data

			# skip restaurant if doesn't work
			except:
				pass

			driver.execute_script("window.history.go(-1)")
			i = i + 1

	except:
		return data_from_page

def check_for_pop_up(driver):

	time.sleep(3)

	try:
		driver.find_element_by_xpath('//*[@id="chiri-modal"]/div[2]/div[2]/div[3]/a[2]').click()

	except:
		pass

def check_for_pop_up2(driver):

	time.sleep(2)

	try:
		driver.find_element_by_xpath('//*[@id="chiri-modal"]/div[2]/div[2]/div[2]/a').click()

	except:
		pass

def update_file(file_name, data):
	with open(file_name, "w") as f:
	    writer = csv.writer(f)
	    writer.writerows(data)

data_from_all_restaurants = []
check_for_pop_up(driver)
num_pages = int(driver.find_element_by_xpath('//*[@id="ghs-search-results-container"]/div/div[2]/div/div/ghs-search-results/div[2]/div/div/p').text.split(" ")[-1])

# output_file_name = "{}_{}.csv".format(city_abbreviated.lower(), state_initials.lower())

output_file_name = "test.csv"

try:

	#iterate through each page 
	for i in range(num_pages):
		data_from_all_restaurants += get_data_from_current_page(driver)
		
		# no more pages 
		if i == num_pages-1:
			break
		
		driver.find_element_by_xpath('//*[@id="ghs-search-results-container"]/div/div[2]/div/div/ghs-search-results/div[2]/div/div/ghs-pagination/ul/li[8]/a').click()
		check_for_pop_up(driver)

	update_file(output_file_name, \
		data_from_all_restaurants)

# still update database
except:
	update_file(output_file_name, \
		data_from_all_restaurants)
	print ("stopped unexpectedly...")











