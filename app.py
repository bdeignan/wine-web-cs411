###########################################
#Version 19.04.2019
#Last Edit: CFB
###########################################


from flask import Flask, render_template,request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pymysql
from forms import SearchForm, LoginForm, RegisterForm, NewLogForm, ReviewForm
import simplejson as json
import datetime
from functools import wraps
from helpers import BlankFormatter


app = Flask(__name__)
app.config['SECRET_KEY'] = "WINE_KEY"
Bootstrap(app)

#########################################################################################################
# SQL Functions                                                                                         #
#########################################################################################################

def getQuery(qry):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        database="wine_web_2",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute(qry)
    result = cursor.fetchall()
    conn.close()
    return result

def insert(sql,val):
    conn = pymysql.connect(
        host="localhost",
        user="root",
        database="wine_web_2",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute(sql, val)
    conn.commit()
    print (cursor.rowcount)
    return cursor.rowcount

# added so i can access connection inside routes
def mysqlConnection():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        database="wine_web_2",
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    return conn


#########################################################################################################
# Global Variables                                                                                      #
#########################################################################################################
loggedIn = False #set to true once login is completed
username = None #once logged in will hold name of user
user_id = None #one looged will hold id of user


#########################################################################################################
# Proces login and register functions                                                                   #
#########################################################################################################
def processLogin(result,pwd):
    correct = False
    if (len(result)==0):
        flash('User name not found')
    else:
        r = result[0]
        if (r['password'] != pwd):
            flash(r['username']+': Password not correct')
        else:
            flash(r['username']+': You were successfully logged in')
            correct = True
    return correct

def processRegister(form):
    correct = False
    result = getQuery("SELECT * FROM users WHERE username = '"+form.username.data+"'")
    if (len(result)!=0):
        flash(form.username.data+': Username already exists')
    else:
        if (form.password.data != form.password_ver.data):
            flash(form.username.data+': Passwords did not match')
        else:
            sql = "INSERT INTO users (username,taster_name,email,password) VALUES (%s,%s,%s,%s)"
            val = (form.username.data,form.name.data,form.email.data,form.password.data)
            r = insert(sql,val)
            flash(str(r)+": rows added")
            flash(form.username.data+': You were successfully registerd')
            correct = True
    return correct

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if loggedIn:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('main'))
    return wrap


#########################################################################################################
# Routes                                                                                                #
#########################################################################################################
@app.route("/",methods=['GET', 'POST'])
@app.route("/index",methods=['GET', 'POST'])
def main():
    global loggedIn
    global username
    global user_id
    form = LoginForm()
    if request.method == "POST":
        result = getQuery("SELECT * FROM users WHERE username = '"+form.username.data+"'")
        correct = processLogin(result,form.password.data)
        if (correct):
            loggedIn = True
            username = form.username.data
            user_id = result[0]['user_id']
            return redirect('/profile')
        else:
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route("/profile",methods=['GET', 'POST'])
def profile():
    global loggedIn
    global username
    global user_id
    if (loggedIn):
        print ("User Name: ",username)
        result = getQuery("SELECT * FROM users WHERE username = '"+username+"'")
        print ("USER ID: ",user_id)
        return render_template('profile.html',result = result[0])
    else:
        return redirect('/index')

@app.route("/register",methods=['GET', 'POST'])	
def register():
    global loggedIn
    global username
    global user_id
    form = RegisterForm()
    if request.method == "POST":
        correct = processRegister(form)
        if (correct):
            loggedIn = True
            username = form.username.data
            result = getQuery("SELECT * FROM users WHERE username = '"+form.username.data+"'")
            user_id = result[0]['user_id']
            return redirect('/profile')
        else:
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)
	

@app.route("/newlog",methods=['GET', 'POST'])	
def newlog():
	form = NewLogForm()
	if request.method == "POST" : 
		print("in the post.")
		dt = datetime.datetime.now()
		sql = "INSERT INTO logs (taster_name, wine_name, log_date, price, purchased_from, description, rating) VALUES (%s, %s, %s, %s, %s, %s, %s)"
		price =  float(form.price.data)
		rate = int(form.rating.data)
		wine_name = form.wineryname.data + " " + form.wineyear.data+" "+form.winevar.data
		val = (username, wine_name, dt.strftime("%Y/%m/%d"),price, form.purchasepoint.data, form.logcontent.data, rate)
		print(val)
		print(sql)
		r = insert(sql,val)
		print(r)
		if(r != 0):
			print("yas.")
			#flash(wine_name+' added to your log.')
			return redirect('/viewlog')
		else:
			print("narp.")
			flash('a problem has occured.') 
	return render_template('newlog.html', form=form)

@app.route("/viewlog",methods=['GET', 'POST'])	
def viewlog():
	#global username
	
	result = getQuery("SELECT DATE_FORMAT(log_date,'%d-%m-%Y') as log_date, wine_name, price, purchased_from, rating, description FROM logs WHERE taster_name = '"+username+"' ORDER BY log_date DESC")

	for r in result:
		print(r)
	
	if(len(result) == 0 ):
		flash('Please enter items in your log.') 
	return render_template('viewlog.html', result = result)
	

# My reviews dashboard
@app.route('/reviews', methods=['GET', 'POST'])
@is_logged_in
def reviews():
    connection = mysqlConnection()
    cur = connection.cursor()

    # Get reviews
    result = cur.execute(
        "SELECT * FROM reviews WHERE username = '"+username+"' ORDER BY points DESC")

    reviews = cur.fetchall()

    if result > 0:
        return render_template('reviews.html', reviews=reviews)
    else:
        msg = 'No Reviews Found'
        return render_template('reviews.html', msg=msg)
    # Close connection
    cur.close()

# All reviews dashboard
@app.route('/allreviews', methods=['GET', 'POST'])
@is_logged_in
def allreviews():
    connection = mysqlConnection()
    cur = connection.cursor()

    # Get reviews
    result = cur.execute(
        "SELECT * FROM reviews ORDER BY points DESC LIMIT 50")

    reviews = cur.fetchall()

    if result > 0:
        return render_template('allreviews.html', reviews=reviews)
    else:
        msg = 'No Reviews Found'
        return render_template('allreviews.html', msg=msg)
    # Close connection
    cur.close()

# View single review
@app.route('/review/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def review(id):
    connection = mysqlConnection()
    # Create cursor
    cur = connection.cursor()

    # Get review
    _ = cur.execute("SELECT * FROM reviews WHERE id = %s", [id])

    review = cur.fetchone()

    return render_template('review.html', review=review)

# Add a new review
@app.route('/add_review', methods=['GET', 'POST'])
@is_logged_in
def add_review():
    global user_id
    print ("Add review, user id: ",user_id)
    form = ReviewForm(request.form)

    if request.method == 'POST' and form.validate():

        fmt = BlankFormatter()
        sql = """INSERT INTO reviews (username, wine_name, winery,
        year, designation, variety, description, points, user_id)
        VALUES('{username}',REPLACE(CONCAT_WS(' ', '{winery}', {year},
        '{designation}', '{variety}'), '  ', ' '),
        '{winery}',
        {year},
        '{designation}',
        '{variety}',
        '{description}',
        {points},
        {user_id}
        )
        ON DUPLICATE KEY UPDATE
        description=VALUES(description), points=VALUES(points)"""

        fixdes = form.description.data
        fixdes = fixdes.replace("'","''")

        args = {'username': username,
                'winery': form.winery.data,
                'year': form.year.data,
                'designation': form.designation.data,
                'variety': form.variety.data,
                'description': fixdes,
                'points': form.points.data,
                'user_id': user_id}
        query = fmt.format(sql, **args)

        connection = mysqlConnection()
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()
        #Close connection
        cur.close()
        flash('Review Created', 'success')

        return redirect(url_for('add_review'))

    return render_template('add_review.html', form=form)

# Edit existing review
@app.route('/edit_review/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_review(id):
    connection = mysqlConnection()
    # Create cursor
    cur = connection.cursor()

    # Get review by id
    result = cur.execute("SELECT * FROM reviews WHERE id = %s", [id])
    review = cur.fetchone()
    cur.close()
    # Get form
    form = ReviewForm(request.form)

    # Populate review form fields
    form.winery.data = review['winery']
    form.year.data = review['year']
    form.designation.data = review['designation']
    form.variety.data = review['variety']
    form.description.data = review['description']
    form.points.data = review['points']

    if request.method == 'POST' and form.validate():
        print('THIS IS WORKS')

        fixdes =  request.form['description']
        fixdes = fixdes.replace("'","''")

        args = {'winery': request.form['winery'],
                'year': request.form['year'],
                'designation': request.form['designation'],
                'variety': request.form['variety'],
                'description': fixdes,
                'points': request.form['points'],
                'id': id
                }

        # Create Cursor
        cur = connection.cursor()
        # Execute
        sql = """UPDATE reviews
        SET wine_name = REPLACE(CONCAT_WS(' ', '{winery}', {year},
        '{designation}', '{variety}'), '  ', ' '),
        winery = '{winery}',
        year = {year},
        designation = '{designation}',
        variety = '{variety}',
        description = '{description}',
        points = {points}
        WHERE id = {id}
        """
        fmt = BlankFormatter()
        query = fmt.format(sql, **args)
        cur = connection.cursor()
        cur.execute(query)
        connection.commit()

        # Close connection
        cur.close()

        flash('Review Updated', 'success')

        return redirect(url_for('reviews'))

    return render_template('edit_review.html', form=form)


# Delete review
@app.route('/delete_review/<string:id>', methods=['POST'])
@is_logged_in
def delete_review(id):
    connection = mysqlConnection()

    # Create cursor
    cur = connection.cursor()

    # Execute
    cur.execute("DELETE FROM reviews WHERE id = %s", [id])

    # Commit to DB
    connection.commit()

    #Close connection
    cur.close()

    flash('Review Deleted', 'success')

    return redirect(url_for('reviews'))


@app.route("/catalog",methods=['GET', 'POST'])	
def catalog():
    variety = getQuery("SELECT DISTINCT variety FROM wines")
    c1 = [(v['variety'],v['variety']) for v in variety]
    c1.sort(key=lambda tup: tup[1])
    year = getQuery("SELECT DISTINCT year FROM wines")
    c2 = [(y['year'],y['year']) for y in year]
    c2.sort(key=lambda tup: tup[1], reverse=True)
    c1 = [('','Select All')] + c1
    c2 = [('','Select All')] + c2
    form = SearchForm()
    form.winevar.choices = c1
    form.wineyear.choices = c2
    form.winevar.default = 0
    form.wineyear.default = 0
    result = None
    if request.method == "POST":
        result = getQuery("SELECT * FROM wines WHERE wine_name LIKE '"+form.winename.data+"%' AND year LIKE '"+form.wineyear.data+"%' AND variety LIKE '"+form.winevar.data+"%' LIMIT 50")
        return render_template('catalog.html',result = result, form = form)
    return render_template('catalog.html',result = result, form = form)	

@app.route("/wine_details",methods=['GET', 'POST'])	
def wine_details():
    name = request.form['details']
    reviews = getQuery("SELECT * FROM reviews WHERE wine_name = '"+name+"'")
    wine = getQuery("SELECT * FROM wines WHERE wine_name = '"+name+"'")
    result = {'reviews': reviews, 'wine' : wine[0]}
    return render_template('wine_details.html',result = result)	


@app.route("/recommend",methods=['GET', 'POST'])	
def recommend():
	return render_template('reccomend.html')	

@app.route("/stats",methods=['GET', 'POST'])	
def stats():
    tot_wines = getQuery("SELECT COUNT(wine_name) as tot from wines;")
    tot_wines = format(int(tot_wines[0]['tot']),',d')
    tot_wineries = getQuery("SELECT COUNT(winery) as tot from winery;")
    tot_wineries = format(int(tot_wineries[0]['tot']),',d')
    data = {'totwin' : tot_wines, 'totwinery' : tot_wineries}
    return render_template('stats.html',data=data)

@app.route("/visualization",methods=['GET', 'POST'])	
def visualization():
    top_var = getQuery(" SELECT DISTINCT (variety) AS name, count(variety) AS count FROM (select * from wines) AS w GROUP BY(variety) ORDER BY count(variety) DESC LIMIT 20;")
    top_var = json.dumps(top_var)
    top_wineries = getQuery("SELECT wines.winery AS name, COUNT(wines.winery) AS count FROM reviews, wines WHERE reviews.wine_name = wines.wine_name GROUP BY wines.winery ORDER BY count(wines.winery) DESC LIMIT 20;")
    top_wineries = json.dumps(top_wineries)
    top_price = getQuery("SELECT country AS name, price AS count FROM country_prices ORDER BY price DESC LIMIT 20;")
    top_price = json.dumps(top_price)
    bot_price = getQuery("SELECT country AS name, price AS count FROM country_prices ORDER BY price LIMIT 20;")
    bot_price = json.dumps(bot_price)
    table_names = [
            {'num' : '0', 'display' : 'Top Varieties', 'name' : 'tpvar','descr': 'Top 20 varieties in the database'},
            {'num' : '1', 'display' : 'Top Wineries Reviewed', 'name' : 'tpwnery','descr': 'Top 20 wineries with most reviews'},
            {'num' : '2', 'display' : 'Most Expensive Countries', 'name' : 'costtop', 'descr' : 'Top 20 most expensive countries based upon average wine price'},
            {'num' : '3', 'display' : 'Least Expensive Countries', 'name' : 'costbot', 'descr' : 'Top 20 least expensive countries based upon average wine price'}
        ]
    
    data = {'tpvar': top_var, 'tpwnery' : top_wineries, 'costtop' : top_price, 'costbot' : bot_price, 'names' : table_names}

    return render_template('visualization.html',data =data)	
	

@app.route("/search",methods=['GET', 'POST'])
def search():
    form = SearchForm()

    result = None
    if request.method == "POST":
        result = getQuery("SELECT * FROM wines WHERE wine_name LIKE '"+form.winename.data+"%' AND year LIKE '"+form.wineyear.data+"%' AND variety LIKE '"+form.winevar.data+"%' LIMIT 50")
        return render_template('wine_search.html',result = result, form = form)
    return render_template('wine_search.html',result = result, form = form)


if __name__ =="__main__":
    app.run(host= '0.0.0.0', port=3030,debug=True,use_reloader=False,threaded=True)




