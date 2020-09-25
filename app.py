from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def homepage():
	print("Welcome to my webpage :" + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	return "Welcome to my webpage :" + datetime.now().strftime("%d/%m/%Y %H:%M:%S")

@app.route('/hi')
def hi():
	print("hi :" + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
	return "hi :" + datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == '__main__':
	print("    ***     **     ***    ")
	print("   ** **    **    ** **   ")
	print("  *******   **   *******  ")
	print(" **     **  **  **     ** ")
	app.run(host='0.0.0.0', port='5000')
	