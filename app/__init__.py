from flask import Flask, render_template
from flask import send_from_directory

from contentManagement import Content

UPLOAD_FOLDER = './media'
image_list = Content()

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template("index.html", image_list=image_list)

@app.route('/login/index/')
def back_to_index():
	return redirect(url_for("index"))

@app.route('/media/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login/', methods = ['GET','POST'])
def loginpage():
	error = None
	try:
		print ("in try")
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			if attempted_username == "admin" and attempted_password == "password":
				return redirect(url_for("adminPanel"))
			else:
				error = "Invalid Credentials. Try Again."
				
		return render_template("login.html", error=error)

	except Exception as e:
		print("in except")
		return render_template("login.html", error=error)


if __name__ == '__main__':
	# app.run(host='192.168.43.108')
	
	app.run(debug=True)