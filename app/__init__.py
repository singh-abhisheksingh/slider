from flask import Flask, render_template
from flask import request, url_for, redirect, session
from flask import send_from_directory
from werkzeug import secure_filename
import config
import os

from conMan import Content, Display, Delete

IMAGE_UPLOAD_FOLDER = './media'
PPT_UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['ppt', 'pptx'])
image_list = Content()
slide_duration = 5000
reload_count = 2

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = PPT_UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME'] =  3000

@app.route('/')
def index():
	# image_list = Content()
	# session['logged_in'] = False
	global image_list
	print ("Rendered index with updated image list")
	print (len(image_list))
	print ("slide_duration = ", slide_duration)
	print ("reload_count = ", reload_count)
	return render_template("index.html", image_list=image_list, slide_duration=slide_duration, reload_count=reload_count)

@app.route('/login/index/')
@app.route('/adminPanel/index/')
def back_to_index():
	# image_list = Content()
	# session['logged_in'] = False
	return redirect(url_for("index"))

@app.route('/media/<filename>')
def uploaded_image_file(filename):
	return send_from_directory(app.config['IMAGE_UPLOAD_FOLDER'], filename)

@app.route('/login/', methods = ['GET','POST'])
def loginpage():
	error = None
	# session['logged_in'] = False
	try:
		print ("in try")
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			if attempted_username == config.name and attempted_password == config.password:
				session['logged_in'] = "admin"
				print (session['logged_in'])
				return redirect(url_for("adminPanel"))
			else:
				error = "Invalid Credentials. Try Again."
				
		return render_template("login.html", error=error)

	except Exception as e:
		print("in except")
		return render_template("login.html", error=error)

@app.route('/adminPanel/')
def adminPanel():
	try:
		if (session['logged_in'] == "admin"):
			ppt_list = Display()
			return render_template("adminPanel.html", PPT_LIST=ppt_list)
		else:
			return "You are logged out. Kindly log in to make changes."
	except Exception as e:
		return "You are logged out. Kindly log in to make changes."

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for("index"))

@app.route('/delete/', methods = ['GET','POST'])
def deletePpt():
	if request.method == "POST":
		print(request.form['deleteIt'])
		Delete(request.form['deleteIt'])
		global image_list
		image_list = Content()
		print (image_list)
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
			global image_list
			image_list = Content()
			return redirect(url_for("adminPanel"))
			# return redirect(url_for('uploaded_ppt_file', filename=filename))
	else:
		return redirect(url_for("index"))

@app.route('/uploads/<filename>')
def uploaded_ppt_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/customize/', methods=['GET', 'POST'])
def customize():
	global slide_duration
	global reload_count
	if request.method == "POST":
		slide_duration = request.form['slideIt']
		slide_duration = int(slide_duration) * 1000
		reload_count = request.form['reloadIt']
		return redirect(url_for("index"))

if __name__ == '__main__':
	# app.run(host='192.168.12.155', debug=True)
	app.run(debug=True)