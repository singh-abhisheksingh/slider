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

@app.route('/media/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
	# app.run(host='192.168.43.108')
	
	app.run(debug=True)