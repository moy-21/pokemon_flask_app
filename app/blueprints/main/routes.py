from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm
from . import bp as main
from flask_login import login_required, current_user
from ...models import Pokemon, Deck, User

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
        poke = Pokemon.query.filter_by(name=pokemon).first()

        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon.lower()}'
        response_ = requests.get(url)
            
        if not response_.ok:
            error_string = 'We had an error'
            return render_template('pokemon_.html.j2', error=error_string, form = form)
        
        if response_:
            if not poke:
                
                base_ = response_.json()['base_experience']
                name = response_.json()['forms'][0]['name']
                sprite = response_.json()['sprites']['other']['home']['front_default']
                attack = response_.json()['stats'][1]['base_stat']
                hp = response_.json()['stats'][0]['base_stat']
                defense = response_.json()['stats'][2]['base_stat']

                poke = Pokemon(name=name, hp=hp,attack=attack, base_ = base_, sprite=sprite, defense=defense)
                poke.save()

            return render_template('pokemon_.html.j2', poke = poke, form=form)
    return render_template('pokemon_.html.j2', form = form)

@main.route('/catch_poke/<string:name>')
@login_required
def catch_poke(name):
    poke = Pokemon.query.filter_by(name=name).first()
    
    if poke not in  current_user.pokemen:
        current_user.catch_poke(poke)
        Deck(poke_id=poke.poke_id, user_id = current_user.id )
        flash(f'Successfully added to deck', "success")
            
    else:
        flash(f'Sorry you already have this pokemon.', "warning")
        return redirect(request.referrer or url_for('main.pokemon_'))
    return redirect(request.referrer or url_for('main.pokemon_', poke= poke))


