from flask import Flask,render_template
#error while importing render_template form flask module (error mentions no module named flask found )
app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
