from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AddItem, DeleteItem, HelpUser
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Item
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home Page')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username of password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title='Sign In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html', title='Contact')


@app.route('/accounts')
@login_required
def accounts():
    posts = User.query.all()
    return render_template("account.html", title="Accounts", posts=posts)


@app.route('/myitems')
@login_required
def favor_item():
    itmds = Item.query.all()
    return render_template("items.html", title="Items", itmds=itmds)


@app.route('/additem', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItem()
    if form.validate_on_submit():
        item = Item(name_author=current_user.username, name_item=form.name_item.data, body=form.name_body.data)
        db.session.add(item)
        db.session.commit()
        flash("You item added!")
        return redirect(url_for('favor_item'))
    return render_template("add_item.html", title="Add Item", form=form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    form = DeleteItem()
    return render_template("delete.html", title="Delete Item", form=form)


@app.route('/help', methods=['GET', 'POST'])
@login_required
def helpme():
    form = HelpUser()
    if form.validate_on_submit():
        flash('Your question has been sent, expect an answer by mail within 24 hours.')
        return redirect(url_for('index'))
    return render_template("help.html", title='Help', form=form)
