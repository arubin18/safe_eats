import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, current_app, flash 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import random

app = Flask(__name__)

app.config.from_object('config.DevelopmentConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Restaurant, User, UserReactsTo, AllergyGroups, Dish


@app.route("/edit_profile/<int:uid>",methods=['GET', 'POST'])
def edit_profile(uid):
    if request.method == 'POST':

        user = User.query.filter_by(uid=uid).first()
        
        button = str(request.form.get('button'))

        if user and button=="go_back": 
            return redirect(url_for("profile", uid=user.uid))


        if user and button=="update_profile": 
            name = request.form.get('name')
            email = request.form.get('email')
            city = str(request.form.get('city'))
            state = ''
            user_allergies = [str(allergy) for allergy in request.form.getlist('allergy_groups')]
                

            if city == "Durham":
                state = "NC"
            if city == "New York":
                state = "NY"
            if city == "Austin":
                state = "TX"

            if name is None or len(name) == 0:
                name = user.full_name
            if email is None or len(email) == 0:
                email = user.email
            if city is None or len(city) == 0:
                city = user.city
            if state is ''  or len(state) == 0:
                state = user.state

            try:
                user.full_name = name 
                user.email = email
                user.city = city 
                user.state = state
                db.session.commit()

            except Exception as e:
                db.session.rollback()

            if(len(user_allergies) == 0):
                UserReactsTo.query.filter_by(uid=int(user.uid)).delete()
                db.session.commit()

            try: 
                UserReactsTo.query.filter_by(uid=int(user.uid)).delete()
                for allergy in user_allergies:
                    user_reacts_to = UserReactsTo(
                        uid = uid,
                        food_group = allergy
                    )
                    db.session.add(user_reacts_to)
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                return (str(e))

            return redirect(url_for("profile", uid=user.uid, user_allergies=user_allergies))

    if request.method == 'GET':
        current_user_id = uid
        user = User.query.filter_by(uid=current_user_id).first().serialize()
        user_allergies = [str(allergy.serialize()['food_group']) for allergy in UserReactsTo.query.filter_by(uid=uid).all()]

        for i in range(len(user_allergies)):
            if(user_allergies[i] == 'nut'):
                user_allergies[i] = "Nuts"
            else:
                user_allergies[i] = user_allergies[i].capitalize()

        for a in user_allergies:
            print("Should check " + a)
        return render_template("edit_profile.html", user=user, user_allergies=user_allergies, city=str(request.args['city']))


@app.route("/<int:uid>",methods=['GET', 'POST'])
@app.route("/profile/<int:uid>",methods=['GET', 'POST'])
def profile(uid):

    if request.method == 'POST':

        button = str(request.form.get('button'))

        user = User.query.filter_by(uid=uid).first()
        user_allergies = [str(allergy.serialize()['food_group']) for allergy in UserReactsTo.query.filter_by(uid=uid).all()]
        for i in range(len(user_allergies)):
            if(user_allergies[i] == 'nut'):
                user_allergies[i] = "Nuts"
            else:
                user_allergies[i] = user_allergies[i].capitalize()        

        if user and button=="edit_profile": 
            city = str(user.city)
            if 'Durham' == city:
                print("D")
            if 'New York' == city:
                print("NY")
            else:
                print("A")
            return redirect(url_for('edit_profile', uid=uid, city=city))

        if user and button=="run_query":
            city = str(user.city)
            return redirect(url_for('query_result', 
                uid=uid, city=city, num_allergies=len(user_allergies)))


    if request.method == 'GET':
        user = User.query.filter_by(uid=uid).first().serialize()
        user_allergies = [str(allergy.serialize()['food_group']) for allergy in UserReactsTo.query.filter_by(uid=uid).all()]

        for i in range(len(user_allergies)):
            if(user_allergies[i] == 'nut'):
                user_allergies[i] = "Nuts"
            else:
                user_allergies[i] = user_allergies[i].capitalize()

        print(user_allergies)

        return render_template("profile.html", user=user, user_allergies=user_allergies)



@app.route("/query_result",methods=['GET'])
def query_result():
    if request.method == 'GET':

        try:
            uid = request.args['uid']
            city = (request.args['city']).strip('')
            allergies = int(request.args['num_allergies'])
            print(allergies)

            result = []
       
            if allergies == 0:
                restaurants = [r.serialize() for r in Restaurant.query.filter_by(city=city)]
                for r in restaurants:
                    print (r)
                    result.append((r, "None"))

            else: 
                sql_query = ''' with c1 as (
                                    with r1 as (select restaurants.name, restaurants.restaurant_id, dishcontains.dish_name, ingredientbelongsto.food_group 
                                    from userreactsto, restaurants, dishcontains, ingredientbelongsto 
                                    where userreactsto.uid={}
                                    and restaurants.restaurant_id=dishcontains.restaurant_id 
                                    and restaurants.restaurant_id=dishcontains.restaurant_id
                                    and restaurants.city='{}'
                                    and dishcontains.ingredient_name=ingredientbelongsto.ingredient_name
                                    and ingredientbelongsto.food_group  = userreactsto.food_group 
                                    group by restaurants.name, restaurants.restaurant_id, dishcontains.dish_name, ingredientbelongsto.food_group
                                    )
                                    select name, restaurant_id, food_group, count(*) 
                                    from r1 group by name, restaurant_id, food_group),

                                c2 as (
                                    select restaurant_id, count(*) 
                                    from dishes 
                                    group by restaurant_id 
                                    order by restaurant_id
                                )

                                select c1.restaurant_id as rid, c1.food_group as allergy, cast(c1.count as float)/cast(c2.count as float) as risk_level 
                                    from c1,c2 
                                    where c1.restaurant_id=c2.restaurant_id 
                                    order by risk_level desc
                            '''.format(uid,city)

                restaurants = db.get_engine(current_app).execute(sql_query)


                for r in restaurants:
                    restaurant_record = Restaurant.query.filter_by(restaurant_id=int(r[0])).first().serialize()
                    allergy = str(r[1])
                    risk = round(float(r[2]) * 100, 2)
                    result.append((restaurant_record, allergy, risk))

            print(len(result[0]))
            return render_template("query_result.html", restaurants=result, uid=uid)
    
        except Exception as e:
            return(str(e))


@app.route("/restaurant_page/<int:rid>", methods=['GET'])
def restaurant_page(rid):
    if request.method == 'GET':

        try:
            uid = request.args['uid']
            user_allergies = [str(allergy.serialize()['food_group']) for allergy in UserReactsTo.query.filter_by(uid=uid).all()]

            for i in range(len(user_allergies)):
                if(user_allergies[i] == 'nut'):
                    user_allergies[i] = "Nuts"
                else:
                    user_allergies[i] = user_allergies[i].capitalize()

            print (user_allergies)

           
            sql_query1 = ''' select restaurants.name, dishes.dish_name, dishes.dish_price, dishes.dish_description, dish_price 
                            from dishes, userreactsto, restaurants, dishcontains, ingredientbelongsto 
                            where userreactsto.uid={} and dishcontains.restaurant_id={} 
                            and ingredientbelongsto.ingredient_name=dishcontains.ingredient_name
                            and restaurants.restaurant_id=dishcontains.restaurant_id
                            and userreactsto.food_group=ingredientbelongsto.food_group 
                            and dishes.dish_name=dishcontains.dish_name 
                            and dishes.restaurant_id=dishcontains.restaurant_id;
                        '''.format(uid,rid, "'%'", "'%'")

            bad_food = db.get_engine(current_app).execute(sql_query1)

            sql_query2 = ''' with bad_food as (select restaurants.name, dishes.dish_name, dishes.dish_price, dishes.dish_description
                            from dishes, userreactsto, restaurants, dishcontains, ingredientbelongsto 
                            where userreactsto.uid={} and dishcontains.restaurant_id={} 
                            and ingredientbelongsto.ingredient_name=dishcontains.ingredient_name 
                            and restaurants.restaurant_id=dishcontains.restaurant_id
                            and userreactsto.food_group=ingredientbelongsto.food_group and 
                            dishes.dish_name=dishcontains.dish_name and dishes.restaurant_id=dishcontains.restaurant_id),
                            all_food as (select restaurants.name, dishes.dish_name, dishes.dish_price, dishes.dish_description 
                            from restaurants, dishes
                            where restaurants.restaurant_id={} and dishes.restaurant_id={})
                            select * from all_food 
                            except 
                            select * from bad_food;
                        '''.format(uid,rid,rid,rid)

            good_food = db.get_engine(current_app).execute(sql_query2)
            good_result=[]
            for i in good_food:
                dish_name = str(i[1])
                dish_price = float(i[2])
                print (dish_price)
                if i[3] is None:
                    dish_description=""
                else:
                    dish_description= str(i[3])
                good_result.append((dish_name, dish_price, dish_description))
            bad_result=[]
            for i in bad_food:
                dish_name = str(i[1])
                dish_price = float(i[2])
                print (dish_price)

                if i[3] is None:
                    dish_description="None"
                else:
                    dish_description= str(i[3])
                bad_result.append((dish_name, dish_price, dish_description))
            print(good_result)
            print(bad_result)
            restaurant = Restaurant.query.filter_by(restaurant_id=rid).first().serialize()
    #menu_items = [ dish.serialize() for dish in Dish.query.filter_by(restaurant_id=rid).all() ]
    #allergies =  [ allergy.serialize() for allergy in UserReactsTo.query.filter_by(uid=uid).all() ]
    #dishes = []
            #ret_dict = {}
            #ret_dict['rid'] = rid
            #ret_dict['allergies'] = [str(a['food_group']) for a in allergies]
            #ret_dict['dishes'] = menu_items
            return render_template("display_restaurant.html", restaurant=restaurant, rid=rid, good_food=good_result, bad_food=bad_result, user_allergies=user_allergies)
    #return str(ret_dict)
        except Exception as e:
            return(str(e))

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not user or not check_password_hash(user.password, password): 
            flash('Oops, Try Again.')
            return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

        uid = user.uid
        return redirect( url_for('profile', uid=uid) )

    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        city = request.form.get('city')

        uid = db.session.query(User).count() + 1

        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('signup'))

        city = str(city)
        if city == "Durham":
            state = "NC"
        if city == "New York":
            state = "NY"
        if city == "Austin":
            state = "TX"

        try:
            # create new user with the form data. Hash the password so plaintext version isn't saved.
            new_user = User(uid=uid, full_name=name, email=email, city=city, state=state,
            password=generate_password_hash(password, method='sha256'))
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            flash('Account Made, Please Log In!')
            return redirect(url_for('login'))

        except Exception as e:

            flash('Oops, Try Again.')
            return redirect(url_for('signup'))
    else:
        return render_template("signup.html")

if __name__ == '__main__':
    app.run()




