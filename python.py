from flask import Flask,render_template,request,send_file,jsonify,send_from_directory,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from gtts import gTTS
import os
import PyPDF2
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename
from datetime import datetime

# result = cloudinary.uploader.upload("path_to_your_file")
# print(result)


# from transformers import AutoModelForCausalLM, AutoTokenizer;

#error while importing render_template form flask module (error mentions no module named flask found )
app = Flask(__name__)

uploads = []

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyBM5C2-QageRRyXI-oRpnHUd41C9DUWt3E",
    "authDomain": "greatest-project-22b73.firebaseapp.com",
    "projectId": "greatest-project-22b73",
    "storageBucket": "greatest-project-22b73.firebasestorage.app",
    "messagingSenderId": "737065353592",
    "appId": "1:737065353592:web:af3f07444d773e0879088d",
    "measurementId": "G-GWVRREHMCX"
}

UPLOAD_FOLDER = "uploads"
AUDIO_FOLDER = "audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def extract_text_from_file(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            return None, str(e)

    elif file_path.endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
        except Exception as e:
            return None, str(e)
    
    return text.strip(), None

def convert_text_to_audio(text, filename="output.mp3"):
    if not text:
        return None, "No valid text found in the file."

    audio_path = os.path.join(AUDIO_FOLDER, filename)
    try:
        tts = gTTS(text=text, lang="en")
        tts.save(audio_path)
        return audio_path, None
    except Exception as e:
        return None, str(e)



@app.route("/convert", methods=['GET', 'POST'])
def convert():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No selected file"})

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Extract text
    text, text_error = extract_text_from_file(file_path)
    if text_error:
        return jsonify({"success": False, "error": text_error})

    # Convert to Audio
    audio_filename = filename.rsplit(".", 1)[0] + ".mp3"
    audio_path, audio_error = convert_text_to_audio(text, audio_filename)
    if audio_error:
        return jsonify({"success": False, "error": audio_error})

    return jsonify({"success": True, "audio_url": f"/audio/{audio_filename}"})

@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_FOLDER, filename)

# model = AutoModelForCausalLM.from_pretrained("D:/projects/webuni-gh-pages/webuni-gh-pages/trained_model", local_files_only=True)
# tokenizer = AutoTokenizer.from_pretrained("./trained_model")
# tts = gTTS("tts_models/en/ljspeech/tacotron2-DDC")

# def generate_conversation(text):
#     inputs = tokenizer(text, return_tensors="pt")
#     output = model.generate(**inputs)
#     return tokenizer.decode(output[0])

# @app.route('/', methods=['POST'])
# def generate_podcast():
#     text = request.form.get("text")
#     conversation = generate_conversation(text)

#     audio_files = []
#     for i, line in enumerate(conversation.split("\n")):
#         filename = f"voice_{i}.wav"
#         tts.tts_to_file(text=line, file_path=filename)
#         audio_files.append(filename)

#     return send_file(audio_files[0], as_attachment=True)

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/addlog")
def courses():
    return render_template('admin_login.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/elements")
def elements():
    return render_template('elements.html')

# @app.route("/user")
# def user():
#     # Fetch list of uploaded files from Cloudinary (optional)
#     files = []  # Placeholder for file list
#     return render_template('user.html', files=files)



@app.route('/admin', methods=['POST','GET'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html', files=[])
    return jsonify({"error": "Method not allowed"}), 405



@app.route('/user')
def user():
        if request.args.get('file'):
            return redirect(url_for('user')) 
        return render_template('user.html', files=uploads)

# Route to fetch uploaded files
@app.route('/files', methods=['GET'])
def get_files():
    return jsonify(uploads)





if __name__ == "__main__":
    app.run(debug=True)
