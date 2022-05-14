from flask import render_template, request, flash, redirect, url_for
import requests
from .forms import PokemonForm, BattleForm
from . import bp as main
from flask_login import login_required, current_user
from ...models import Pokemon, Deck, User

@main.route('/', methods = ['GET'])
@login_required
def index():
    return render_template('index.html.j2')

@main.route('/battle_home', methods = ['GET', 'POST'])
@login_required
def battle_home():
    users=User.query.filter(User.id != current_user.id).all()
    poke = Pokemon.query.filter_by().all()
    form = BattleForm()
    if request.method == 'POST' and form.validate_on_submit():
        return render_template('battle.html.j2', form=form)

    return render_template('battle_home.html.j2', users=users, form = form, poke=poke)

@main.route('/battle_arena/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def battle_arena(user_id):
    user=User.query.filter_by(id = user_id).first()
    poke = Pokemon.query.filter_by().all()
    
    return render_template('battle_arena.html.j2', user=user, poke=poke)

@main.route('/my_poke', methods = ['GET', 'POST'])
@login_required
def my_poke():

    
    
    return render_template('my_poke.html.j2')



@main.route('/battle/<int:user_id>')
@login_required
def battle(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_deck = user.pokemen
    deck_hp= []
    deck_attack = []
    deck_defense = []
    my_deck_hp = []
    my_deck_attack = []
    my_deck_defense = []
    loss = 1
    win = 1
    for poke in user_deck:
        deck_hp.append(poke.hp) 
        deck_attack.append(poke.attack) 
        deck_defense.append(poke.defense) 
        
    for poke in current_user.pokemen:
        my_deck_hp.append(poke.hp) 
        my_deck_attack.append(poke.attack) 
        my_deck_defense.append(poke.defense)
    
    if sum(my_deck_hp) == sum(deck_hp) and sum(my_deck_attack) == sum(deck_attack):
        flash(f"You both have tied no winner here", "success")
        return redirect(url_for('main.battle_home'))
    if sum(my_deck_hp) > sum(deck_hp) and sum(my_deck_attack) > sum(deck_attack):
        current_user.add_win(win)
        user.add_loss(loss)
        flash(f"You have defeated {user.first_name}'s squad.", "success")
        return redirect(url_for('main.battle_home'))
    if sum(my_deck_hp) < sum(deck_hp) and sum(my_deck_attack) < sum(deck_attack):
        current_user.add_loss(loss)
        user.add_win(win)
        flash(f"You have been defeated by {user.first_name}'s squad.", "danger")
        return redirect(url_for('main.battle_home'))
    if sum(my_deck_hp) > sum(deck_hp) and sum(my_deck_attack) < sum(deck_attack):
        if my_deck_hp - deck_attack > 0:
            current_user.add_win(win)
            user.add_loss(loss)
            flash(f"That was a close match, but you defeated {user.first_name}'s squad.", "danger")
            return redirect(url_for('main.battle_home'))
        else:
            current_user.add_loss(loss)
            user.add_win(win)
            flash(f"Close one but you have been defeated by {user.first_name}'s squad.", "danger")
            return redirect(url_for('main.battle_home'))
    return redirect(request.referrer or url_for('main.battle_home'))
    



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
            
            poke 


            return render_template('pokemon_.html.j2', poke = poke, form=form)
    return render_template('pokemon_.html.j2', form = form)

@main.route('/catch_poke/<string:name>')
@login_required
def catch_poke(name):
    poke = Pokemon.query.filter_by(name=name).first()
    
    if poke not in  current_user.pokemen:

        if len(current_user.pokemen.all()) >=5:
            flash(f'Sorry your deck is full', "danger")
            return redirect(request.referrer or url_for('main.pokemon_'))

        current_user.catch_poke(poke)
        Deck(poke_id=poke.poke_id, user_id = current_user.id )
        flash(f'Successfully added to deck', "success")

    else:
        flash(f'Sorry you already have this pokemon.', "warning")
        return redirect(request.referrer or url_for('main.pokemon_'))
    return redirect(request.referrer or url_for('main.pokemon_', poke= poke))




@main.route('/release_poke/<string:name>')
@login_required
def release_poke(name):
    poke = Pokemon.query.filter_by(name=name).first()
    current_user.release_poke(poke)
    flash(f'You have released this pokemon.', "success")
    return redirect(request.referrer or url_for('main.pokemon_', poke= poke))


