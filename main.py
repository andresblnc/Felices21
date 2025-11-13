from flask import Flask, render_template, session, redirect, url_for, request, flash
from datetime import timedelta
from time import time

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
                    flash("Womp Womp! Intenta de nuevo.")
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
                    flash("Womp Womp! Intenta de nuevo.")
            except (TypeError, ValueError):
                flash("Por favor ingresa valores válidos.")

        # Reto 3: lógica con botón verde en los clics 19, 50 y 99
        if num_juego == 3:
            contador = session.get("contador_reto_3", 0)
            mostrar_verde = session.get("mostrar_verde", False)

            # Define los clics clave donde aparece el botón verde
            clics_clave = [19, 50, 94]

            if request.method == "POST":
                if "rojo" in request.form:
                    # Si se hace clic en el botón rojo
                    if mostrar_verde:
                        contador = 0  # Reinicia el contador si el botón verde está visible
                        session["contador_reto_3"] = contador
                        session["mostrar_verde"] = False
                        flash("¡Hiciste clic en el botón rojo! El contador se reinició.")
                    else:
                        contador += 1
                        session["contador_reto_3"] = contador
                        if contador in clics_clave:  # Si el contador está en un clic clave
                            session["mostrar_verde"] = True  # Muestra el botón verde
                            return redirect(url_for("juego_detalle", num_juego=num_juego))  # Redirige para actualizar el estado
                        elif contador >= 100:
                            correcto = True
                            flash("¡Desafío completado! 🎉")

                elif "verde" in request.form:
                    # Si se hace clic en el botón verde
                    session["mostrar_verde"] = False  # Oculta el botón verde
                    flash("¡Bien hecho! Ahora puedes seguir pulsando el botón rojo.")

            return render_template(
                "juego_detalle.html",
                num_juego=num_juego,
                completado=completado,
                correcto=correcto,
                progreso=get_progreso(),
                total_retos=TOTAL_RETOS,
                contador=contador,
                mostrar_verde=mostrar_verde
            )

        # Reto 4: Pregunta sobre Capi
        if num_juego == 4 and request.method == "POST":
            respuesta = request.form.get("respuesta")
            if respuesta and respuesta.strip() == "12":
                correcto = True
            else:
                flash("Respuesta incorrecta. Intenta de nuevo.")

        # Reto 5: Pregunta sobre un crucigrama
        if num_juego == 5 and request.method == "POST":
            respuesta = request.form.get("respuesta")
            if respuesta and respuesta.strip().lower() == "japon":
                correcto = True
            else:
                flash("Respuesta incorrecta. Intenta de nuevo.")

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
    session.pop("contador_reto_3", None) 
    return redirect(url_for("juegos"))

@app.before_request
def make_session_permanent():
    session.permanent = True

if __name__ == "__main__":
    app.run(debug=True)