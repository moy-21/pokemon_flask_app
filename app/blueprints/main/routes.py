from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from . import bp as main
from flask_login import login_required

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/pokemon_', methods=['GET','POST'])
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
            sprite = response_.json()['sprites']['other']['home']['front_default']
            attack = response_.json()['stats'][1]['base_stat']
            hp = response_.json()['stats'][0]['base_stat']
            defense = response_.json()['stats'][2]['base_stat']

            pokemon_dic['name']= name
            pokemon_dic['base_']= base_
            pokemon_dic['sprite']= sprite
            pokemon_dic['hp']= hp
            pokemon_dic['attack']= attack
            pokemon_dic['defense']= defense

            return render_template('pokemon_.html.j2', pokemon_dic = pokemon_dic, form=form)
    return render_template('pokemon_.html.j2', form = form)
