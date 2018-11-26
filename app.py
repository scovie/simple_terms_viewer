''' 
Contains the bulk of the code for the Simple Terms Viewer
See comments below on what to change related to database usage
Tested locally on Windows 10 using a virtual environment with Flask and PyMySQL installed
@scovie on github 26-Nov-2018
'''

from flask import Flask, render_template, flash, url_for, request
import pymysql.cursors

app = Flask(__name__)

'''
Modify based on local database connection details
User and password should match actual credentials, localdb should be the db name
Works with MariaDB/MySQL
'''
def db_connect():
	# Connect to the database
	connection = pymysql.connect(host='localhost', 
								 user='user',
								 password='password',
								 db='localdb',
								 charset='utf8mb4',
								 cursorclass=pymysql.cursors.DictCursor)
	return connection
	
# Index page can be access via three urls
@app.route('/')
@app.route('/index')
@app.route('/help')
def help():
	return render_template('help.html')

'''
refdata page is meant to display the available Terms and Conditions
field names used are:
	TERMS_COND_VERSION varchar(10), 
	TERMS_COND_DESCRIPTION varchar(2048), 
	EFFECTIVE_START date, 
	EFFECTIVE_END date
	where a is an auto incremented index of type BIGINT
'''
@app.route('/refdata')
def refdata():
	try:
		# opening db connection
		connection = db_connect()
		with connection.cursor() as cursor:
			sql = "SELECT TERMS_COND_VERSION, TERMS_COND_DESCRIPTION, EFFECTIVE_START, EFFECTIVE_END FROM local_terms_conditions ORDER BY a"
			cursor.execute(sql)
			results = cursor.fetchall()
	finally:
		# closing db connection
		cursor.close()
		connection.close()
		
	return render_template('refdata.html', results=results)

''' 
customer page allows a user to search for active Terms based on a telephone number
field names used are:
	CTN varchar(10),
	EFFECTIVE_TERMS varchar(10) - would match TERMS_COND_VERSION,
	EXPIRATION_DATE date - would match EFFECTIVE_END
	where a is an auto incremented index of type BIGINT
'''
@app.route('/customer', methods=['GET', 'POST'])
def customer():
	if request.method == 'POST':
		text = request.form['text']
		try:
			# opening db connection
			connection = db_connect()
			with connection.cursor() as cursor:
				sql = "SELECT CTN, EFFECTIVE_TERMS, EXPIRATION_DATE from customer_lookup WHERE CTN = (%s) ORDER BY a"
				cursor.execute(sql, text)
				results = cursor.fetchall()
		finally:
			# closing db connection
			cursor.close()
			connection.close()
		return render_template('customer.html', results=results)
	else:
		return render_template('customer.html')
	
if __name__ == '__main__':
	app.run()