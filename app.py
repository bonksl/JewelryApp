from flask import Flask, render_template, request, flash, redirect, send_file
from werkzeug.utils import secure_filename
from data import Articles
import os
import urllib.request

# Init app
app = Flask(__name__)
UPLOAD_FOLDER = "static/img/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Articles = Articles()

#Upload API
@app.route('/Upload', methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		#check if the post request has the file part
		if 'file' not in request.files:
			print ('no file')
			return redirect(request.url)
		file = request.files['file']
		# if user does not select file, browser also submit an empty part without file name
		if file.filename == '':
			print ('no filename')
			return redirect (request.url)
		else:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print("saved file successfully")
			# send file name as parameter to download
			return redirect('/downloadfile/' + filename)
	return render_template('Upload.html')

#Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
	return render_template('Download.html', value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
	file_path = UPLOAD_FOLDER + filename
	return send_file(file_path, as_attachment=True, attachment_filename='')


@app.route('/', methods =['GET'])
def index():
	return render_template('home.html')


@app.route('/home', methods =['GET'])
def home():
	return render_template('home.html')


@app.route('/About')
def about():
	return render_template('about.html')


@app.route('/Articles')
def articles():
	return render_template('articles.html', articles = Articles)


@app.route('/article/<string:id>/')
def article(id):
	return render_template('article.html', id=id)


# Run Server
if __name__ == '__main__':
	app.run(debug=True)