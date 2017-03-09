## this python file map url to functions
##http://leafletjs.com/
##https://www.mediawiki.org/wiki/Extension:GeoData
from flask import Flask, render_template,request,redirect, url_for, session
from model import db, User,Place ## import db method and user class from model.py file
from form import SignUp, LogIn, Address ## Using to render sign up form into browser
app = Flask(__name__,static_url_path='/static')##create a new instance flask named app
db.init_app(app) ## flask init_app use to initialize app to use db setup

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/learningflask'
## connect to postgres sql database

app.secret_key = "development-key" ##define a secret key that for Flask-WTF
##to generate secure forms avoid CSRF

@app.route('/io', methods=['GET', 'POST'])
def upload_file():
    f1 = open('newlog.txt','w')##file i /o write file into assign3.txt
    return f1.write('Something wrong with this page');
## response = self.handle_exception(e)


@app.route("/")## user type in url"/", the function index will run
def index():
    return render_template("index.html")##python use route to render index.html

@app.route("/about")
def about():
    return render_template("about.html")##python use route to render about.html

@app.route("/sign", methods=['GET','POST'])##flask method to distinguish
##between get or post request
def sign():

     if 'email' in session:
         return redirect(url_for('returnPage'))
     form = SignUp()
     if request.method == 'POST':##form submit post method will happen
         if form.validate()==False: ##fail validate, reload the sign page
            return render_template('sign.html',form=form)
         else:
            ##validate data will be saved into database
            ##newuser instance of user object and initialize with data from sign form by using .data
            newuser =  User(form.f_name.data,form.l_name.data,form.email.data,form.password.data)
            ##insert the new user object into user table
            db.session.add(newuser)
            db.session.commit()
            ##after new user signs up, it create new session
            session['email'] = newuser.email ##python associated the key email with user`s email
            ##if the user is login, the key email will exist in this object.
            ##after new session create, it should get redirect to returnpage
            return redirect(url_for('returnPage'))
     elif request.method =='GET':##render signup as usual
         return render_template("sign.html",form=form)

@app.route("/login",methods=["Get","POST"])#get post request
def login():
    if 'email' in session:
        return redirect(url_for('returnPage'))
    form = LogIn()
    if request.method == "POST":
        if form.validate()==False:#user enter wrong info
            return render_template("login.html",form=form)
        else:
          ##collect email data and pswd data
            email = form.email.data
            password = form.password.data
           ##using email and password check if user exist in database or not
            user = User.query.filter_by(email=email).first()
            if user is not None and user.check_password(password):
           ##login the user by creating new session
              session['email'] = form.email.data
              return redirect(url_for('returnPage'))
            else:
              return redirect(url_for('login'))

    elif request.method == 'GET':
        return render_template('login.html',form=form)

@app.route("/logout")
def logout():
    ##use session.pop() to delete the cookie
    session.pop('email',None)
    return redirect(url_for('index'))## return main page



@app.route("/returnpage", methods=["Get","POST"])
def returnPage():##check the user login or not
     if 'email' not in session:
         return redirect(url_for('login'))
     form = Address()
     places = []
     my_coordinates = (45.348306,-75.756240) ##default algonquin college latitude and longitude

     if request.method == 'POST':
         if form.validate() == False:
             return render_template('returnpage.html',form=form)
         else:
             ##retrieve the address from the form and save into varigable Address
             address=form.address.data
             ##query the places in flask
             p = Place()##new useable of place model
             ##convert the address input into latitude and longitude
             my_coordinates = p.address_to_latlng(address)
             places = p.query(address)##query these places around coordinates
             return render_template('returnpage.html', form=form,my_coordinates=my_coordinates,places=places)
     elif request.method == 'GET':
          return render_template("returnpage.html",form = form,my_coordinates=my_coordinates,places=places)

if __name__=="__main__":
    app.run(debug=True)
