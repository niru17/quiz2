from sqlite3 import Row
from math import radians,sin,cos,asin,sqrt
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
import pyodbc
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
driver = '{ODBC Driver 17 for SQL Server}'
database = 'assign2'
server = 'assign02.database.windows.net'
username = "nxs6306"
password = "Nirumondi@1701"
with pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
    with conn.cursor() as cursor:
        temp = []
        cursor.execute("SELECT TOP 3 City, State FROM population")
        while True:
            r = cursor.fetchone()
            if not r:
                break
            print(str(r[0]) + " " + str(r[1]))
            temp.append(r)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/ln')
def ln():
   return render_template('ln.html')

@app.route('/range')
def range1():
   return render_template('range.html')

@app.route('/cluster')
def cluster():
   return render_template('cluster.html')    

@app.route('/net')
def net():
   return render_template('net.html') 

@app.route('/net2')
def net2():
   return render_template('net2.html') 

@app.route('/gap')
def gap():
   return render_template('gap.html') 

@app.route('/gap2')
def gap2():
   return render_template('gap2.html')    

@app.route('/lnsearch',methods=['POST','GET'])
def rangesearch():
    lon=request.form['lon']
    d=request.form['d']
    lonf = float(lon)
    df = float(d) 
    lonstart = str(lonf-df)
    lonend = str(lonf+df)
    querry="SELECT top 5 City, State, Population, lat, lon FROM population WHERE population between ? and ? order by population desc"
    cursor.execute(querry,(lonstart,lonend))
    rows = cursor.fetchall()
    return render_template("list.html",rows = rows)

@app.route("/clusters", methods=['GET', 'POST'])
def Task4():
    n = str(request.form['Num'])
    mag=str(request.form['Mag'])
    count =0
    query=("Select TOP 5 net from population where net in (select net from population where mag>'"+mag+"') group by net order by count(net) desc")
    cursor.execute(query) 
    result=cursor.fetchall()
    return render_template("Task4.html",length=len(result), rows=result)

@app.route('/gapnet', methods = ['GET','POST'])
def gapnet():
    if request.method =='POST':
        N = str(request.form['N'])
        range01=str(request.form['Range1'])
        range02=str(request.form['Range2'])
        query = "SELECT top "+N+"  City, State, Population, lat, lon FROM population WHERE population BETWEEN "+range01+" AND "+range02+" order by population desc"
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("list.html", rows = results)          

@app.route('/gapnet2', methods = ['GET','POST'])
def gapnet2():
    if request.method =='POST':
        N = str(request.form['N'])
        range1=str(request.form['Range1'])
        range2=str(request.form['Range2'])
        query = "SELECT top "+N+" City, State, Population, lat, lon FROM population WHERE population BETWEEN "+range1+" AND "+range2+" order by population asc "
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("list.html", rows = results)                        
          
def distance(lat1, lat2, lon1, lon2):
    	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a))
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	# calculate the result
	return(c * r)

@app.route('/Task3',methods=['POST','GET'])
def lsearch():
    if request.method =='POST':
        lat1=request.form['lat1']
        lon1=request.form['lon1']
        km=request.form['kms']
        querry="Select City, State, Population, lat, lon FROM population "
        cursor.execute(querry)
        lat1=float(lat1)
        lon1=float(lon1)
        km=float(km)
        rows = cursor.fetchall()
        bkm=[]
        for i in rows:
            x=distance(lat1,float(i[2]),lon1,float(i[3]))
            if x<=km:
                bkm.append(i)
        return render_template("Task3.html",rows = bkm)
    else:
        return render_template('Task3.html')            
          
@app.route('/Add', methods=['GET', 'POST'])
def addperson():
    if (request.method=='POST'):
        City= str(request.form['City'])
        State= str(request.form['State'])
        Population= str(request.form['Population'])
        Lat= str(request.form['Lat'])
        Lon= str(request.form['Lon'])
        
        querry="INSERT INTO population VALUES ('"+City+"','"+State+"','"+Population+"','"+Lat+"','"+Lon+"')"
        cursor.execute(querry)
        querry1="select * from population "
        cursor.execute(querry1)
        results = cursor.fetchall()
    return render_template("list.html",rows = results)        
          
if __name__ == '__main__':
    app.run(debug=True)