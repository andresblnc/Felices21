from flask import Flask, render_template, session, redirect, url_for, request, flash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "cumple21"  # Necesario para sesiones
app.permanent_session_lifetime = timedelta(days=10)  # Sesión dura 10 días

TOTAL_RETOS = 12

def get_progreso():
    completados = session.get("completados", [])
    return len(completados)

@app.route("/")
def home():
    return render_template("inicio.html", progreso=get_progreso(), total_retos=TOTAL_RETOS)

@app.route("/juego")
def juegos():
    return render_template("juego.html", progreso=get_progreso(), total_retos=TOTAL_RETOS)

@app.route("/juego/<int:num_juego>", methods=["GET", "POST"])
def juego_detalle(num_juego):
    if 1 <= num_juego <= TOTAL_RETOS:
        completados = session.get("completados", [])
        completado = num_juego in completados
        correcto = False

        # Reto 1: validar lat/lon
        if num_juego == 1 and request.method == "POST":
            lat = request.form.get("latitud")
            lon = request.form.get("longitud")
            try:
                lat = float(lat)
                lon = float(lon)
                lat_ok = 20.610 <= lat <= 20.612
                lon_ok = -103.463 <= lon <= -103.460
                correcto = lat_ok and lon_ok
                if not correcto:
                    flash("¡Intenta de nuevo! Las coordenadas no son correctas.")
            except (TypeError, ValueError):
                flash("Por favor ingresa valores válidos.")

        # Reto 2: validar lat/lon
        if num_juego == 2 and request.method == "POST":
            lat = request.form.get("latitud")
            lon = request.form.get("longitud")
            try:
                lat = float(lat)
                lon = float(lon)
                # Cambia estos valores por los correctos para tu foto 2
                lat_ok = 20.665 <= lat <= 20.671
                lon_ok = -103.443 <= lon <= -103.438
                correcto = lat_ok and lon_ok
                if not correcto:
                    flash("¡Intenta de nuevo! Las coordenadas no son correctas.")
            except (TypeError, ValueError):
                flash("Por favor ingresa valores válidos.")

        return render_template(
            "juego_detalle.html",
            num_juego=num_juego,
            completado=completado,
            correcto=correcto,
            progreso=get_progreso(),
            total_retos=TOTAL_RETOS
        )
    else:
        return "<h2>Reto no encontrado</h2>", 404

@app.route("/completar/<int:num_juego>")
def completar(num_juego):
    if 1 <= num_juego <= TOTAL_RETOS:
        completados = session.get("completados", [])
        if num_juego not in completados:
            completados.append(num_juego)
            session["completados"] = completados
        return redirect(url_for("juego_detalle", num_juego=num_juego))
    else:
        return "<h2>Reto no encontrado</h2>", 404

@app.route("/reiniciar")
def reiniciar():
    session["completados"] = []
    return redirect(url_for("juegos"))

@app.before_request
def make_session_permanent():
    session.permanent = True

if __name__ == "__main__":
    app.run(debug=True)