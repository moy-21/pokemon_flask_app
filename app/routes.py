from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm, LoginForm, RegisterForm
from app import app
from .models import User
from flask_login import current_user, logout_user, login_user, login_required

@app.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@app.route('/pokemon_', methods=['GET','POST'])
@login_required
def pokemon_():
    form = PokemonForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon = form.pokemon.data.lower()

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
        response_ = requests.get(url)
            
        if not response_.ok:
            error_string = 'We had an error'
            return render_template('pokemon_.html.j2', error=error_string, form = form)
        
        if response_:
            pokemon_dic = {}
            
            base_ = response_.json()['base_experience']
            name = response_.json()['forms'][0]['name']
            sprite = response_.json()['sprites']['front_shiny']
            attack = response_.json()['stats'][1]['base_stat']
            hp = response_.json()['stats'][0]['base_stat']
            defense = response_.json()['stats'][2]['base_stat']

            pokemon_dic['name']= name
            pokemon_dic['baseXP']= base_
            pokemon_dic['sprite']= sprite
            pokemon_dic['hp']= hp
            pokemon_dic['attack']= attack
            pokemon_dic['defense']= defense

            return render_template('pokemon_.html.j2', pokemon_dic = pokemon_dic, form=form)
    return render_template('pokemon_.html.j2', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method=='POST' and form.validate_on_submit():
        # Do Login stuff
        email = form.email.data.lower()
        password = form.password.data

        #Look up user by email address that is trying to log in
        u=User.query.filter_by(email=email).first()
        if u and u.check_hashed_password(password):
            login_user(u)
            flash('Welcome to Pokemon Battle','success')
            return redirect(url_for('index'))
        flash('Incorrect Email Password Combo', 'danger')
        return render_template('login.html.j2', form=form)
    return render_template("login.html.j2", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method =='POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name":form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email":form.email.data.lower(),
                "password":form.password.data
            }
            # Create an empty User
            new_user_object = User()
            #build user with the form data
            new_user_object.from_dict(new_user_data)
            #save user to the database
            new_user_object.save()

        except:
            flash("There was an unexpected Error creating you account Please Try again Later","danger")
            return render_template('register.html.j2', form=form)
        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html.j2', form=form)


@app.route('/logout')
@login_required
def logout():
    if current_user:
        logout_user()
        flash('You have logged out','warning')
        return redirect(url_for('login'))
