from flask import Flask, render_template
from flask import request, url_for, redirect, session
from flask import send_from_directory
from werkzeug import secure_filename
import os

from contentManagement import Content, Display, Delete

IMAGE_UPLOAD_FOLDER = './media'
PPT_UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['ppt', 'pptx'])
image_list = Content()

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = PPT_UPLOAD_FOLDER

@app.route('/logout/')
@app.route('/')
def index():
	# image_list = Content()
	session['logged_in'] = False
	return render_template("index.html", image_list=image_list)

@app.route('/login/index/')
@app.route('/adminPanel/index/')
def back_to_index():
	session['logged_in'] = False
	return redirect(url_for("index"))

@app.route('/media/<filename>')
def uploaded_image_file(filename):
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
		ppt_list = Display()
		return render_template("adminPanel.html", PPT_LIST=ppt_list)
	else:
		return "Kindly log in"

@app.route('/delete/', methods = ['GET','POST'])
def deletePpt():
	if request.method == "POST":
		print(request.form['deleteIt'])
		Delete(request.form['deleteIt'])
		return redirect(url_for("adminPanel"))
	else:
		return redirect(url_for("adminPanel"))

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods = ['GET', 'POST'])
def upload_file():
	if request.method == "POST":
		if 'file' not in request.files:
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			Content()
			return redirect(url_for("adminPanel"))
			# return redirect(url_for('uploaded_ppt_file', filename=filename))

@app.route('/uploads/<filename>')
def uploaded_ppt_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
	# app.run(host='192.168.12.155')
	app.run(debug=True)