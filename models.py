from app import db

class User(db.Model):
    __tablename__ = 'users'

    uid = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    city = db.Column(db.String(256))
    state = db.Column(db.String(256))
    password = db.Column(db.String(256))

    def __init__(self, uid, full_name, email, city, \
        state, password):
        self.uid = uid
        self.full_name = full_name
        self.email = email
        self.city = city
        self.state = state
        self.password = password

    def __repr__(self):
        return '<User | {} | {} | {} >'.format(self.uid, self.full_name, self.city)
    
    def serialize(self):
        return {
            'id': self.uid, 
            'full_name': self.full_name,
            'email': self.email,
            'city':self.city,
            'state':self.state,
            'password':self.password,
        }

class AllergyGroups(db.Model):
    __tablename__ = 'allergygroups'

    food_group = db.Column(db.String(256), primary_key=True)

    def __repr__(self):
        return '<AllergyGroups | {}>'.format(self.food_group)
    
    def serialize(self):
        return {
            'food_group': self.food_group 
        }

class UserReactsTo(db.Model):
    __tablename__ = 'userreactsto'

    uid = db.Column(db.Integer(), db.ForeignKey('users.uid'), primary_key=True)
    food_group = db.Column(db.String(256), db.ForeignKey('allergygroups.food_group'), \
        primary_key=True)

    def __init__(self, uid, food_group):
        self.uid = uid
        self.food_group = food_group

    def __repr__(self):
        return '<UserReactsTo | {} | >'.format(self.uid, self.food_group)
    
    def serialize(self):
        return {
            'uid': self.uid, 
            'food_group': self.food_group
        }

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    ingredient_name = db.Column(db.String(256), primary_key=True)

    def __repr__(self):
        return '<Ingredient {} | >'.format(self.ingredient_name)
    
    def serialize(self):
        return {
            'ingredient name': self.ingredient_name 
        }

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    restaurant_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(256))
    street_address = db.Column(db.String(256))
    city = db.Column(db.String(256))
    state = db.Column(db.String(256))

    phone_number = db.Column(db.String(256))
    page_link = db.Column(db.String(256))
    image_link = db.Column(db.String(256))
    timely_rating = db.Column(db.Integer())
    tasty_rating = db.Column(db.Integer())
    correct_rating = db.Column(db.Integer())

    def __init__(self, restaurant_id, name, street_address, city, state, 
        phone_number, page_link, image_link, timely_rating, tasty_rating, correct_rating):

        self.restaurant_id = restaurant_id
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state

        self.phone_number = phone_number
        self.page_link = page_link
        self.image_link = image_link

        self.timely_rating = timely_rating
        self.tasty_rating = tasty_rating
        self.correct_rating = correct_rating

    def __repr__(self):
        return '<Restaurant | {}>'.format(self.name)
    
    def serialize(self):
        return {
            'id': self.restaurant_id, 
            'name': self.name,
            'street_address': self.street_address,
            'city':self.city,
            'state':self.state, 
            'phone_number':self.phone_number,

            'url': self.page_link, 
            'image': self.image_link, 
            'timely_rating': self.timely_rating,
            'tasty_rating': self.tasty_rating,
            'correct_rating': self.correct_rating
        }

class IngredientBelongsTo(db.Model):
    __tablename__ = 'ingredientbelongsto'

    ingredient_name = db.Column(db.String(256), primary_key=True)
    food_group = db.Column(db.String(256), db.ForeignKey('allergygroups.food_group'), \
        primary_key=True)

    def __repr__(self):
        return '<IngredientBelongsTo | {} | {} >'.format(self.ingredient_name, self.food_group)
    
    def serialize(self):
        return {
            'ingredient name': self.ingredient_name, 
            'food group': self.food_group
        }

class Dish(db.Model):
    __tablename__ = 'dishes'

    restaurant_id = db.Column(db.Integer(), db.ForeignKey('restaurants.restaurant_id'), \
        primary_key=True)
    dish_name = db.Column(db.String(256), primary_key=True)
    dish_description = db.Column(db.String(2048))
    dish_price = db.Column(db.Float())

    def __init__(self, restaurant_id, dish_name, dish_description, dish_price):
        self.restaurant_id = restaurant_id
        self.dish_name = dish_name
        self.dish_description = dish_description
        self.dish_price = dish_price

    def __repr__(self):
        return '<Dish | {} - made by {}, {}>'.format(self.dish_name, self.restaurant_name, self.restaurant_id)
    
    def serialize(self):
        return {
            'restaurant id': self.restaurant_id, 
            'dish name': self.dish_name,
            'dish description': self.dish_description,
            'dish price': self.dish_price
        }

class DishContains(db.Model):
    __tablename__ = 'dishcontains'

    restaurant_id = db.Column(db.Integer(),primary_key=True)
    dish_name = db.Column(db.String(256), primary_key=True)
    ingredient_name = db.Column(db.String(256), primary_key=True)
    # __table_args__ = (ForeignKeyConstraint([restaurant_id, dish_name],
    #                                        [Dish.restaurant_id, Dish.dish_name]),)

    def __init__(self, restaurant_id, dish_name, ingredient_name):
        self.restaurant_id = restaurant_id
        self.dish_name = dish_name
        self.ingredient_name = ingredient_name

    def __repr__(self):
        return '<DishContains | {} , {}>'.format(self.dish_name, self.ingredient_name)
    
    def serialize(self):
        return {
            'restaurant id': self.restaurant_id, 
            'dish name': self.dish_name,
            'ingredient name': self.ingredient_name
        }

