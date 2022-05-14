from flask_wtf import FlaskForm
from sqlalchemy import LABEL_STYLE_TABLENAME_PLUS_COL
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    pokemon = StringField('Pokemon', validators = [DataRequired()])
    submit = SubmitField('Search')

class BattleForm(FlaskForm):
    battle = SubmitField('Battle')
