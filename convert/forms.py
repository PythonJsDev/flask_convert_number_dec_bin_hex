from flask_wtf import FlaskForm
# from wtforms import StringField, EmailField, SubmitField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms import EmailField, SubmitField, PasswordField, StringField, SelectField

from convert.models import User
from convert.utilities import is_data_valid


class LoginForm(FlaskForm):
    """ Formulaire de login """
    email = EmailField('Email',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit = SubmitField("Se connecter")


class RegistrationForm(FlaskForm):
    """ Formulaire d'inscription """
    email = EmailField('Votre email:',
                       validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe:', validators=[DataRequired(),
                                                          EqualTo("pass_confirm",
                                                          message="Les mots de passe doivent correspondre!")])
    pass_confirm = PasswordField('Confirmer le mot de passe:', validators=[DataRequired()])
    submit = SubmitField("S'inscrire!")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Cet email est déjà utilisé')


class InputData(FlaskForm):
    """ Formulaire de saisie de la valeur à convertir et de sa base  """
    data_to_convert = StringField('Entrez la valeur à convertir:')
    base = SelectField(u'Choix de la base:',
                       choices=[('dec', 'Décimal'),
                                ('hex', 'Hexadécimal'),
                                ('bin', 'Binaire')])
    submit = SubmitField('Validez')

    def validate_data_to_convert(self, data_to_convert):
        if not is_data_valid(data_to_convert):
            raise ValidationError('Entrer une valeur valide svp')
