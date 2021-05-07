from flask import render_template, url_for, redirect, request, Blueprint, flash
from flask_login import login_user, current_user, logout_user, login_required
from Capstone import db
from Capstone.models import User
from Capstone.Users.forms import RegistrationForm, LoginForm, UpdateForm, BenchForm
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler


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

    return render_template('register.html', form = form)

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
    # current_model = load_model('deadlift_predict')
    # user_input = [[  0. ,  29. ,  59.8, 105. ,  55. ,   2. ]]
    # scaler = MinMaxScaler()
    # user_input = scaler.transform(user_input)
    # prediction = current_model.predict(user_input)
    # form = PredictForm()
    #
    # if request.method == 'POST':
    #     if request.form['bench_button'] == 'Bench':
    #         print("Bench")  # do something
    #     elif request.form['squat_button'] == 'Squat':
    #         print("Squat")  # do something else
    #     elif request.form['deadlift_button'] == 'Deadlift':
    #         print("Deadlift")  # do something else
    #     else:
    #         pass # unknown
    # elif request.method == 'GET':
    #     return render_template('predict.html', form=form)

    return render_template('predict.html')

@users.route('/bench', methods=['GET', 'POST'])
@login_required
def bench():

    form = BenchForm()

    if form.validate_on_submit():

        equipment = form.equipment.data
        age = form.age.data
        sex = form.sex.data
        weight = form.weight.data
        squat = form.squat.data
        deadlift = form.deadlift.data

        new_prediction = [sex,equipment,age,weight,squat,deadlift]
        from Capstone.ML.predict_squat import predict
        new_prediction = predict(new_prediction)

        return render_template('bench.html', new_prediction = new_prediction, form=form)


    elif request.method == "GET":
        print("get")

    return render_template('bench.html', form=form)

@users.route('/squat', methods=['GET', 'POST'])
@login_required
def squat():
    dog = "Squat"
    return render_template('squat.html', dog=dog)

@users.route('/deadlift', methods=['GET', 'POST'])
@login_required
def deadlift():
    dog = "Deadlift"
    return render_template('deadlift.html', dog=dog)