from flask import Flask, render_template,request, redirect, flash, url_for
from flask_bootstrap import Bootstrap
import pymysql
from forms import SearchForm, LoginForm, RegisterForm, NewLogForm, NewReviewForm
import json

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


#########################################################################################################
# Global Variables                                                                                      #
#########################################################################################################
loggedIn = False #set to true once login is completed
username = None #once logged in will hold name of user


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


#########################################################################################################
# Routes                                                                                                #
#########################################################################################################
@app.route("/",methods=['GET', 'POST'])
@app.route("/index",methods=['GET', 'POST'])
def main():
    global loggedIn
    global username
    form = LoginForm()
    if request.method == "POST":
        result = getQuery("SELECT * FROM users WHERE username = '"+form.username.data+"'")
        correct = processLogin(result,form.password.data)
        if (correct):
            loggedIn = True
            username = form.username.data
            return redirect('/profile')
        else:
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route("/profile",methods=['GET', 'POST'])
def profile():
    global loggedIn
    global username
    if (loggedIn):
        print ("User Name: ",username)
        result = getQuery("SELECT * FROM users WHERE username = '"+username+"'")
        print (result)
        return render_template('profile.html',result = result[0])
    else:
        return redirect('/index')

@app.route("/register",methods=['GET', 'POST'])	
def register():
    global loggedIn
    global username
    form = RegisterForm()
    if request.method == "POST":
        correct = processRegister(form)
        if (correct):
            loggedIn = True
            username = form.username.data
            return redirect('/profile')
        else:
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)
	

@app.route("/newlog",methods=['GET', 'POST'])	
def newlog():
	form = NewLogForm()
	return render_template('newlog.html', form=form)

@app.route("/viewlog",methods=['GET', 'POST'])	
def viewlog():
	return render_template('viewlog.html')
	
@app.route("/newreview",methods=['GET', 'POST'])	
def newreview():
	form = NewReviewForm()
	return render_template('newreview.html', form=form)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
        result = getQuery("SELECT * FROM reviews WHERE username ='" + username + "'"
                + " ORDER BY points DESC"
                )
        return render_template('reviews.html',result = result)
	

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
	return render_template('stats.html')

@app.route("/visualization",methods=['GET', 'POST'])	
def visualization():
    top_wines = getQuery(" SELECT DISTINCT (variety), count(variety) AS count FROM (select * from wines) AS w GROUP BY(variety) HAVING count(variety) > 500;")
    top_wines = json.dumps(top_wines, indent=2)
    data = {'top_wines': top_wines}
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




