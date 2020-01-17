CREATE TABLE Users
(uid INTEGER NOT NULL,
 full_name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL,
 city VARCHAR(256) NOT NULL,
 state VARCHAR(256) NOT NULL,
 password VARCHAR(256) NOT NULL,
 PRIMARY KEY (uid),
 UNIQUE (email));

CREATE TABLE AllergyGroups
(food_group VARCHAR(256) NOT NULL,
 PRIMARY KEY (food_group)); 

CREATE TABLE UserReactsTo
(uid INTEGER NOT NULL,
 food_group VARCHAR(256) NOT NULL,
 PRIMARY KEY (uid, food_group),
 FOREIGN KEY (uid) REFERENCES Users(uid),
 FOREIGN KEY (food_group) REFERENCES AllergyGroups(food_group)); 

CREATE TABLE Ingredients
(ingredient_name VARCHAR(256) NOT NULL,
 PRIMARY KEY (ingredient_name)); 

CREATE TABLE Restaurants
(restaurant_id INTEGER NOT NULL,
 name VARCHAR(256) NOT NULL,
 street_address VARCHAR(256) NOT NULL,
 city VARCHAR(256) NOT NULL,
 state VARCHAR(256) NOT NULL,
 phone_number VARCHAR(256),
 page_link VARCHAR(256),
 image_link VARCHAR(256),
 tasty_rating INTEGER,
 timely_rating INTEGER,
 correct_rating INTEGER,
 --phone_number VARCHAR(256) UNIQUE,
 PRIMARY KEY (restaurant_id)); 

CREATE TABLE IngredientBelongsTo
(ingredient_name VARCHAR(256) NOT NULL,
 food_group VARCHAR(256) NOT NULL,
 PRIMARY KEY (ingredient_name, food_group),
 -- FOREIGN KEY (ingredient_name) REFERENCES Ingredients(ingredient_name),
 FOREIGN KEY (food_group) REFERENCES AllergyGroups(food_group));


CREATE TABLE Dishes
(restaurant_id INTEGER NOT NULL,
 dish_name VARCHAR(256) NOT NULL,
 dish_description VARCHAR(2048),
 dish_price FLOAT,
 PRIMARY KEY (restaurant_id, dish_name),
 FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)); 


CREATE TABLE DishContains
(restaurant_id INTEGER NOT NULL,
 dish_name VARCHAR(256) NOT NULL,
 ingredient_name VARCHAR(256) NOT NULL, --CHECK (ingredient_name in (select ingredient_name from Ingredients)),
 PRIMARY KEY (restaurant_id, dish_name, ingredient_name));
 --FOREIGN KEY (ingredient_name) REFERENCES Ingredients(ingredient_name),
 FOREIGN KEY (restaurant_id, dish_name) REFERENCES Dishes(restaurant_id, dish_name));


CREATE TABLE NearbyRestaurants
(uid INTEGER NOT NULL,
 restaurant_id INTEGER NOT NULL,
 distance FLOAT NOT NULL,
 PRIMARY KEY (uid, restaurant_id),
 FOREIGN KEY (uid) REFERENCES Users(uid),
 FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)); 

-- INSERT INTO Users
-- 	VALUES(1, 'Rick Mortenson', 'richard.mortenson@duke.edu', '749 Ninth Street', 'Durham', 'North Carolina', 'MichiganRulez123',10),
-- 	(2, 'Alex Rubin', 'alex.rubin@duke.edu', '314 Anderson Street', 'Durham', 'North Carolina', 'HeavBuffs1234',5),
-- 	(3, 'David Rothblatt', 'david.rothblatt@duke.edu', '800 Broad Street', 'Durham', 'North Carolina', 'Yankees123',7)
-- 	ON CONFLICT DO NOTHING;

-- INSERT INTO Ingredients
-- VALUES
-- 	('onion'),
-- 	('cheese'),
-- 	('rice'),
-- 	('quinoa'),
-- 	('chicken'),
-- 	('lettuce'),
-- 	('tomato'),
-- 	('tomatoe'),
-- 	('pepper'),
-- 	('hot'),
-- 	('spicy'),
-- 	('bean'),
-- 	('shrimp'),
-- 	('cream'),
-- 	('tortilla'),
-- 	('beef'),
-- 	('mushroom'),
-- 	('avocado'),
-- 	('egg'),
-- 	('eggs'),
-- 	('omelete'),
-- 	('pancake'),
-- 	('waffle'),
-- 	('cucumber'),
-- 	('salad'),
-- 	('mayo'),
-- 	('bacon'),
-- 	('mozzarella'),
-- 	('carrot'),
-- 	('roll'),
-- 	('hot sauce'),
-- 	('cheddar cheese'),
-- 	('steak'),
-- 	('bread'),
-- 	('bell pepper'),
-- 	('milk'),
-- 	('broccoli'),
-- 	('scallions'),
-- 	('french fries'),
-- 	('vegetable'),
-- 	('spinach'),
-- 	('crab'),
-- 	('tuna'),
-- 	('noodle'),
-- 	('spice'),
-- 	('corn'),
-- 	('tender'),
-- 	('pork'),
-- 	('tempura'),
-- 	('bun'),
-- 	('basil'),
-- 	('cilantro'),
-- 	('ham'),
-- 	('guacamole'),
-- 	('sausage'),
-- 	('ranch'),
-- 	('salmon'),
-- 	('romaine'),
-- 	('provolone'),
-- 	('parmesan'),
-- 	('chili'),
-- 	('pickle'),
-- 	('jalapeno'),
-- 	('eel'),
-- 	('zucchini'),
-- 	('chocolate'),
-- 	('sprout'),
-- 	('mayonnaise'),
-- 	('flour'),
-- 	('oil'),
-- 	('jack cheese'),
-- 	('pepperjack'),
-- 	('ginger'),
-- 	('banana'),
-- 	('wheat'),
-- 	('peanut'),
-- 	('turkey'),
-- 	('seed'),
-- 	('butter'),
-- 	('potatoe'),
-- 	('curry'),
-- 	('pineapple'),
-- 	('pea'),
-- 	('olive'),
-- 	('sesame'),
-- 	('pico de gallo'),
-- 	('apple'),
-- 	('cabbage'),
-- 	('bbq sauce'),
-- 	('salsa'),
-- 	('herb'),
-- 	('pepperoni'),
-- 	('thai chili flakes'),
-- 	('crouton'),
-- 	('marinara'),
-- 	('celery'),
-- 	('potato'),
-- 	('lemon'),
-- 	('mango'),
-- 	('soy'),
-- 	('sunflower'),
-- 	('salt'),
-- 	('enchilada'),
-- 	('coconut'),
-- 	('aioli'),
-- 	('lamb'),
-- 	('toast'),
-- 	('sandwich'),
-- 	('masago (fish)'),
-- 	('fruit'),
-- 	('lime'),
-- 	('brioche'),
-- 	('hushpuppie'),
-- 	('taco'),
-- 	('feta cheese'),
-- 	('burrito'),
-- 	('orange'),
-- 	('tofu'),
-- 	('ricotta'),
-- 	('pasta'),
-- 	('pita'),
-- 	('slaw'),
-- 	('squash'),
-- 	('applewood smoked bacon'),
-- 	('veggie'),
-- 	('yogurt'),
-- 	('cauliflower'),
-- 	('walnut'),
-- 	('asparagus'),
-- 	('goat'),
-- 	('chorizo'),
-- 	('arugula'),
-- 	('spring roll'),
-- 	('kale'),
-- 	('burger'),
-- 	('ketchup'),
-- 	('almond'),
-- 	('american cheese'),
-- 	('roma cheese'),
-- 	('coffee'),
-- 	('ice cream'),
-- 	('shake'),
-- 	('pecan'),
-- 	('hazelnut'),
-- 	('cashew'),
-- 	('pistachio'),
-- 	('macadamedia'),
-- 	('pine nut'),
-- 	('pasta'),
-- 	('gnochhi'),
-- 	('pizza'),
-- 	('hero'),
-- 	('couscous'),
-- 	('crackers'),
-- 	('farina'),
-- 	('beer'),
-- 	('edamame'),
-- 	('miso'),
-- 	('soybean'),
-- 	('cookie'),
-- 	('tahini'),
-- 	('anchoivies'),
-- 	('bass'),
-- 	('catfish'),
-- 	('cod'),
-- 	('flounder'),
-- 	('grouper'),
-- 	('haddock'),
-- 	('hake'),
-- 	('halibut'),
-- 	('herring'),
-- 	('mahi mahi'),
-- 	('pollock'),
-- 	('salmon'),
-- 	('sole'),
-- 	('snapper'),
-- 	('trout'),
-- 	('tilapia'),
-- 	('tuna'),
-- 	('worcestershire'),
-- 	('crab'),
-- 	('lobster'),
-- 	('prawn'),
-- 	('shrimp'),
-- 	('clams'),
-- 	('oysters'),
-- 	('scallops'),
-- 	('squid'),
-- 	('snail'),
-- 	('mustard'),
-- 	('coriander'),
-- 	('garlic'),
-- 	('maize'),
-- 	('cherry'),
-- 	('peach'),
-- 	('strawberry'),
-- 	('blueberry'),
-- 	('blackberry')
-- 	ON CONFLICT DO NOTHING;

INSERT INTO AllergyGroups
VALUES
	( 'spice' ),
	( 'soy' ),
	( 'meat' ),
	( 'egg' ),
	( 'fruit' ),
	( 'spicy' ),
	( 'vegetable' ),
	( 'seed' ),
	( 'corn' ),
	( 'sesame' ),
	( 'grain' ),
	( 'sodium' ),
	( 'gluten' ),
	( 'fish' ),
	( 'shellfish' ),
	( 'dairy' ),
	( 'nut' )
	ON CONFLICT DO NOTHING;

INSERT INTO IngredientBelongsTo
VALUES
	('onion', 'vegetable'),
	('cheese', 'dairy'),
	('rice', 'grain'),
	('quinoa', 'grain'),
	('chicken', 'meat'),
	('lettuce', 'vegetable'),
	('tomato','vegetable'),
	('tomatoe','vegetable'),
	('pepper','vegetable'),
	('hot', 'spicy'),
	('spicy', 'spicy'),
	('bean','vegetable'),
	('shrimp', 'shellfish'),
	('cream', 'dairy'),
	('tortilla', 'gluten'),
	('beef', 'meat'),
	('mushroom','vegetable'),
	('avocado','vegetable'),
	('egg', 'egg'),
	('eggs', 'egg'),
	('omelete', 'egg'),
	('pancake', 'gluten'),
	('pancake', 'egg'),
	('waffle', 'gluten'),
	('waffle', 'egg'),
	('cucumber','vegetable'),
	('salad','vegetable'),
	('mayo', 'egg'),
	('bacon', 'meat'),
	('mozzarella', 'dairy'),
	('carrot', 'vegetable'),
	('roll', 'gluten'),
	('hot sauce', 'spicy'),
	('cheddar cheese', 'dairy'),
	('steak', 'meat'),
	('bread', 'gluten'),
	('bell pepper','vegetable'),
	('milk', 'dairy'),
	('broccoli','vegetable'),
	('scallions','vegetable'),
	('french fries', 'gluten'),
	('vegetable','vegetable'),
	('spinach','vegetable'),
	('crab', 'shellfish'),
	('tuna', 'fish'),
	('noodle', 'gluten'),
	('noodle', 'grain'),
	('spice', 'spicy'),
	('corn', 'grain'),
	('tender','meat'),
	('pork','meat'),
	('tempura','shellfish'),
	('tempura','meat'),
	('bun', 'gluten'),
	('basil','vegetable'),
	('cilantro', 'vegetable'),
	('ham', 'meat'),
	('guacamole', 'vegetable'),
	('sausage', 'meat'),
	('ranch', 'dairy'),
	('ranch', 'egg'),
	('salmon', 'fish'),
	('romaine', 'vegetable'),
	('provolone', 'dairy'),
	('parmesan', 'dairy'),
	('chili', 'spicy'),
	('pickle', 'vegetable'),
	('jalapeno', 'spicy'),
	('jalapeno', 'vegetable'),
	('eel', 'fish'),
	('zucchini', 'vegetable'),
	('chocolate', 'dairy'),
	('sprout', 'vegetable'),
	('mayonnaise', 'egg'),
	('flour', 'grain'),
	('flour', 'gluten'),
	('oil', 'nut'),
	('jack cheese', 'dairy'),
	('pepperjack', 'dairy'),
	('ginger', 'spicy'),
	('banana', 'fruit'),
	('wheat', 'gluten'),
	('wheat', 'grain'),
	('peanut', 'nut'),
	('sunflower','seed'),
	('turkey', 'meat'),
	('seed','seed'),
	('butter', 'dairy'),
	('potatoe', 'vegetable'),
	('curry', 'spice'),
	('pineapple', 'fruit'),
	('pea', 'fruit'),
	('olive', 'vegetable'),
	('sesame', 'seed'),
	('pico de gallo', 'vegetable'),
	('apple', 'fruit'),
	('cabbage', 'vegetable'),
	('bbq sauce', 'spice'),
	('bbq sauce', 'egg'),
	('bbq sauce', 'dairy'),
	('salsa', 'vegetable'),
	('herb', 'vegetable'),
	('pepperoni', 'meat'),
	('thai chili flakes', 'spice'),
	('crouton', 'gluten'),
	('marinara', 'vegetable'),
	('celery', 'vegetable'),
	('potato', 'vegetable'),
	('lemon', 'fruit'),
	('mango', 'fruit'),
	('soy', 'soy'),
	('salt', 'sodium'),
	('enchilada', 'gluten'),
	('enchilada', 'corn'),
	('enchilada', 'meat'),
	('coconut', 'nut'),
	('aioli', 'egg'),
	('lamb', 'meat'),
	('toast', 'gluten'),
	('sandwich', 'gluten'),
	('sandwich', 'meat'),
	('masago (fish)', 'fish'),
	('fruit', 'fruit'),
	('lime', 'fruit'),
	('brioche', 'gluten'),
	('hushpuppie', 'gluten'),
	('taco', 'gluten'),
	('taco', 'meat'),
	('feta cheese', 'dairy'),
	('burrito', 'gluten'),
	('burrito', 'meat'),
	('burrito', 'vegetable'),
	('orange', 'fruit'),
	('tofu', 'soy'),
	('ricotta', 'dairy'),
	('pasta', 'gluten'),
	('pita', 'gluten'),
	('slaw', 'egg'),
	('slaw', 'vegetable'),
	('squash', 'vegetable'),
	('applewood smoked bacon', 'meat'),
	('veggie', 'vegetable'),
	('yogurt', 'dairy'),
	('cauliflower', 'vegetable'),
	('walnut', 'nut'),
	('asparagus', 'vegetable'),
	('goat', 'meat'),
	('chorizo', 'meat'),
	('arugula', 'vegetable'),
	('spring roll', 'gluten'),
	('spring roll', 'vegetable'),
	('spring roll', 'shellfish'),
	('kale', 'vegetable'),
	('burger', 'meat'),
	('ketchup', 'vegetable'),
	('almond', 'nut'),
	('american cheese', 'dairy'),
	('roma cheese', 'dairy'),
	('ice cream', 'dairy'),
	('shake', 'dairy'),
	('pecan', 'nut'),
	('hazelnut', 'nut'),
	('cashew', 'nut'),
	('pistachio', 'nut'),
	('macadamedia', 'nut'),
	('pine nut', 'nut'),
	('pasta', 'nut'),
	('gnochhi', 'gluten'),
	('pizza', 'gluten'),
	('pizza', 'dairy'),
	('hero', 'gluten'),
	('couscous', 'grain'),
	('crackers', 'gluten'),
	('farina', 'gluten'),
	('beer', 'gluten'),
	('edamame', 'soy'),
	('miso', 'soy'),
	('soybean', 'soy'),
	('cookie', 'gluten'),
	('cookie', 'dairy'),
	('tahini', 'seed'),
	('anchoivies', 'fish'),
	('bass', 'fish'),
	('catfish', 'fish'),
	('cod', 'fish'),
	('flounder', 'fish'),
	('grouper', 'fish'),
	('haddock', 'fish'),
	('hake', 'fish'),
	('halibut', 'fish'),
	('herring', 'fish'),
	('mahi mahi', 'fish'),
	('pollock', 'fish'),
	('salmon', 'fish'),
	('sole','fish'),
	('snapper', 'fish'),
	('trout', 'fish'),
	('tilapia', 'fish'),
	('tuna', 'fish'),
	('worcestershire','fish'),
	('crab', 'shellfish'),
	('lobster','shellfish'),
	('prawn','shellfish'),
	('shrimp','shellfish'),
	('clams','shellfish'),
	('oysters','shellfish'),
	('scallops','shellfish'),
	('squid','shellfish'),
	('snail', 'meat'),
	('mustard','spicy'),
	('coriander','spicy'),
	('garlic','spicy'),
	('maize','vegetable'),
	('cherry','fruit'),
	('peach','fruit'),
	('strawberry', 'fruit'),
	('blueberry','fruit'),
	('blackberry','fruit')
	ON CONFLICT DO NOTHING;

-- INSERT INTO UserReactsTo
-- 	Values(1, 'nut'),
-- 	(1, 'dairy'),
-- 	(2, 'dairy'), 
-- 	(3, 'shellfish')
-- 	ON CONFLICT DO NOTHING;