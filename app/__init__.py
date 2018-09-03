from flask import Flask, render_template
from flask import request, url_for, redirect, session
from flask import send_from_directory

from contentManagement import Content, Display

UPLOAD_FOLDER = './media'
image_list = Content()
ppt_list = Display()

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/logout/')
@app.route('/')
def index():
	session['logged_in'] = False
	return render_template("index.html", image_list=image_list)

@app.route('/login/index/')
@app.route('/adminPanel/index/')
def back_to_index():
	session['logged_in'] = False
	return redirect(url_for("index"))

@app.route('/media/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login/', methods = ['GET','POST'])
def loginpage():
	error = None
	session['logged_in'] = False
	try:
		print ("in try")
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			if attempted_username == "admin" and attempted_password == "password":
				session['logged_in'] = True
				return redirect(url_for("adminPanel"))
			else:
				error = "Invalid Credentials. Try Again."
				
		return render_template("login.html", error=error)

	except Exception as e:
		print("in except")
		return render_template("login.html", error=error)

@app.route('/adminPanel/')
def adminPanel():
	if (session['logged_in'] == True):
		return render_template("adminPanel.html", PPT_LIST=ppt_list)
	else:
		return "Kindly log in"

if __name__ == '__main__':
	# app.run(host='192.168.12.155')

	app.run(debug=True)