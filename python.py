from flask import Flask,render_template,request,send_file
from gtts import gTTS
import os
import PyPDF2
from PIL import Image
import pytesseract

#error while importing render_template form flask module (error mentions no module named flask found )
app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/courses")
def courses():
    return render_template('courses.html')

@app.route("/blog")
def blog():
    return render_template('blog.html')

@app.route("/elements")
def elements():
    return render_template('elements.html')

@app.route("/user")
def user():
    return render_template('user.html')
# Route to handle file upload and conversion
@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    
    if file.filename == '':
        return "No selected file", 400

    # Process the file based on its type
    text = ""
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
    elif file.filename.endswith(('.jpg', '.jpeg', '.png')):
        text = extract_text_from_image(file)
    elif file.filename.endswith(('.doc', '.docx')):
        text = extract_text_from_doc(file)

    if text:
        audio_file = convert_text_to_audio(text)
        return send_file(audio_file, as_attachment=True)

    return "Could not extract text", 400

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_doc(file):
    # Implement logic to extract text from DOC/DOCX files
    pass

def convert_text_to_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_file = 'output.mp3'
    tts.save(audio_file)
    return audio_file


@app.route("/admin")
def admin():
    return render_template('wrefw.html')

@app.route("/addlog")
def addlog():
    return render_template("admin_login.html")





if __name__ == "__main__":
    app.run(debug=True)
