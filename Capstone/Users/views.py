from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from Capstone import db
from Capstone.models import User
from Capstone.Users.forms import RegistrationForm, LoginForm, UpdateForm, BenchForm, DeadliftForm, SquatForm
from Capstone.ML.predict_squat import predict_squat
from Capstone.ML.predict_deadlift import predict_deadlift
from Capstone.ML.predict_bench import predict_bench


users = Blueprint('users', __name__)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration Complete!')
        return redirect(url_for('users.login'))

    return render_template("register.html", form = form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            flash('Login Complete!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')
            return redirect(next)

    return render_template('login.html', form = form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Update Complete!')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form)


@users.route('/visualize', methods=['GET', 'POST'])
@login_required
def visualize():
    dog = "doggy"
    return render_template('visualize.html', dog=dog)


@users.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():

    return render_template('predict.html')


@users.route('/bench', methods=['GET', 'POST'])
@login_required
def bench():

    form = BenchForm()

    if form.validate_on_submit():
        predictor = predict_bench()

        equipment = form.equipment.data
        age = form.age.data
        sex = form.sex.data
        weight = form.weight.data
        squat = form.squat.data
        deadlift = form.deadlift.data

        new_prediction = [sex,equipment,age,weight,squat,deadlift]
        print("input", new_prediction)
        new_prediction = predictor.predict(new_prediction)

        print("results", new_prediction)

        new_prediction = round(new_prediction.flat[0],1)

        return render_template('bench.html', new_prediction = new_prediction , form=form)


    elif request.method == "GET":
        print("get")

    return render_template('bench.html', form=form)

@users.route('/squat', methods=['GET', 'POST'])
@login_required
def squat():

    form = SquatForm()

    if form.validate_on_submit():
        predictor = predict_squat()

        equipment = form.equipment.data
        age = form.age.data
        sex = form.sex.data
        weight = form.weight.data
        bench = form.bench.data
        deadlift = form.deadlift.data

        new_prediction = [sex,equipment,age,weight,bench,deadlift]
        print("input", new_prediction)
        new_prediction = predictor.predict(new_prediction)

        print("results", new_prediction)

        new_prediction = round(new_prediction.flat[0],1)

        return render_template('squat.html', new_prediction = new_prediction , form=form)


    elif request.method == "GET":
        print("get")

    return render_template('squat.html', form=form)

@users.route('/deadlift', methods=['GET', 'POST'])
@login_required
def deadlift():

    form = DeadliftForm()

    if form.validate_on_submit():
        predictor = predict_deadlift()

        equipment = form.equipment.data
        age = form.age.data
        sex = form.sex.data
        weight = form.weight.data
        bench = form.bench.data
        squat = form.squat.data

        new_prediction = [sex,equipment,age,weight,squat,bench]
        print("input", new_prediction)
        new_prediction = predictor.predict(new_prediction)

        print("results", new_prediction)

        new_prediction = round(new_prediction.flat[0],1)

        return render_template('deadlift.html', new_prediction = new_prediction , form=form)


    elif request.method == "GET":
        print("get")

    return render_template('deadlift.html', form=form)
