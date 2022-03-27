from flask import flash, redirect, url_for, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from convert import app, db
from convert.forms import LoginForm, RegistrationForm, InputData
from convert.models import User, Convert
from convert.utilities import check_base_data, convert

db.create_all()


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Accueil')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
            flash("connexion impossible! Vérifier vos identifiants", "danger")
    return render_template('login.html', title='Connexion', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = generate_password_hash(form.password.data)
            user = User(email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f'Le compte pour {form.email.data} est créé.', "success")
            return redirect(url_for('login'))
        else:
            flash("Une erreur s'est produite!", "danger")
    return render_template('register.html', title='Inscription', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    """ gestion du compte de l'utilisateur connecté """
    datas = {}
    form = InputData()
    if form.validate_on_submit():
        if not check_base_data(form.base, form.data_to_convert):
            return render_template('account.html', title='Mon compte', form=form, datas=datas)
        data_to_convert = form.data_to_convert.data.upper()
        base = form.base.data
        data = convert(base, data_to_convert)
        user = User.query.filter_by(email=current_user.email).first()
        results = Convert(value_dec=data.get('dec'),
                          value_bin=data.get('bin'),
                          value_hex=data.get('hex'),
                          base=base,
                          user_id=user.id)
        db.session.add(results)
        db.session.commit()
        form.data_to_convert.data = ''
        return redirect(url_for('account'))
    datas = Convert.query.filter_by(user_id=current_user.id)
    return render_template('account.html', title='Mon compte', form=form, datas=datas)


@app.route('/delete')
@login_required
def delete():
    """ efface l'historique de l'utilisateur connecté """
    datas = Convert.query.filter_by(user_id=current_user.id)
    for data in datas:
        db.session.delete(data)
    db.session.commit()
    return redirect(url_for('account'))
