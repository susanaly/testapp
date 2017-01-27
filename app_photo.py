# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:17:41 2017

@author: susanalaiyuen
"""
import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif', 'png'])

# Initialize application
app = Flask(__name__)

# path to the upload directory
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define allowed extensions for the file to be uploaded
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def main():
  return render_template('upload.html')

# Display the image in template.html
@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/tmp/' + filename
    return render_template('template.html', filename=filename)

@app.route('/tmp/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
 
# Check the file uploaded by user   
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']  
        # If user does not select a file
        if f.filename == '':
            return render_template('upload.html')
            
        # If a file is selected that satisfies the extensions allowed,
        # display the image
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

if __name__ == '__main__':
    app.run(debug=True)
