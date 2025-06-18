from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/medicalImages"
mongo = PyMongo(app)

# File Upload Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Home route
@app.route('/')
def index():
    images = mongo.db.images.find()  # Fetch all images from the database
    return render_template('index.html', images=images)  # Pass images to the template


# Image upload route
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return redirect('/')
    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Save file information to MongoDB
        mongo.db.images.insert_one({'filename': filename, 'filepath': filepath})

        return redirect('/')

    return 'File type not allowed'


if __name__ == '__main__':
    app.run(debug=True)
