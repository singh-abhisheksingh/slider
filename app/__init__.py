from flask import Flask, render_template
from contentManagement import Content

image_list = Content()

app = Flask(__name__)

@app.route('/')

def index():
	return render_template("index.html", image_list=image_list)

if __name__ == '__main__':
	app.run(host='192.168.43.108')
	# app.run()