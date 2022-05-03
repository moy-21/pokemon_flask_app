from flask import Flask, render_template, request
import requests



app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/pokemon_', methods=['GET','POST'])
def pokemon_():
    if request.method == 'POST':
        pokemon = request.form.get('pokemon')

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
        response_ = requests.get(url)
        
        if not response_.ok:
            error_string = 'We had an error'
            return render_template('pokemon_.html.j2', error=error_string)
        
        
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
        
        return render_template('pokemon_.html.j2', pokemon_dic = pokemon_dic)
    return render_template('pokemon_.html.j2')