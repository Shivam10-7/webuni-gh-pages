# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import os
# import cloudinary
# import cloudinary.uploader
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)

# # Configure Cloudinary
# cloudinary.config(
#     cloud_name="djr33abwe",
#     api_key="326571775883622",
#     api_secret="m8pWggycsPmoUUR6y9vYuWwAliY"
# )

# # Configure SQLite Database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
# db = SQLAlchemy(app)

# # Define a model for uploaded files
# class UploadedFile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), nullable=False)
#     type = db.Column(db.String(50), nullable=False)
#     date = db.Column(db.String(10), nullable=False)
#     size = db.Column(db.String(20), nullable=False)
#     url = db.Column(db.String(500), nullable=False)

# # Create the database tables
# with app.app_context():
#     db.create_all()

# @app.route("/")
# def index():
#     return render_template('index.html')

# @app.route('/admin', methods=['POST', 'GET'])
# def admin():
#     if request.method == 'POST':
#         # Handle file upload
#         if 'file' not in request.files:
#             return jsonify({"error": "No file part"}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({"error": "No selected file"}), 400
        
#         # Upload file to Cloudinary
#         try:
#             upload_result = cloudinary.uploader.upload(file)
#             print("File uploaded successfully:", upload_result['url'])  # Debugging
            
#             # Save file metadata to the database
#             new_file = UploadedFile(
#                 name=file.filename,
#                 type='file',  # Customize based on file type
#                 date=datetime.now().strftime('%Y-%m-%d'),
#                 size=f"{(upload_result['bytes'] / 1024 / 1024):.2f}MB",
#                 url=upload_result['url']
#             )
#             db.session.add(new_file)
#             db.session.commit()
            
#             return jsonify({
#                 'id': new_file.id,
#                 'name': new_file.name,
#                 'type': new_file.type,
#                 'date': new_file.date,
#                 'size': new_file.size,
#                 'url': new_file.url
#             })
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
    
#     # Fetch all files from the database for GET requests
#     files = UploadedFile.query.all()
#     return render_template('admin.html', files=files)

# @app.route('/user')
# def user():
#     files = UploadedFile.query.all()
#     return render_template('user.html', files=files)

# if __name__ == "__main__":
#     app.run(debug=True)