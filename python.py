from flask import Flask,render_template
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

@app.route("/admin")
def admin():
    return render_template('wrefw.html')





if __name__ == "__main__":
    app.run(debug=True)
