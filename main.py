from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("inicio.html")

@app.route("/juego")
def juego():
    return "<h2>¡Aquí empieza el juego de cumpleaños!</h2>"

if __name__ == "__main__":
    app.run(debug=True)