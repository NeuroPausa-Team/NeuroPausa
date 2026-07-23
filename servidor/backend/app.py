from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import traceback
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)


# ===========================================================
# ENVÍO DE CORREO
# ===========================================================

def enviar_bienvenida_paciente(correo_paciente, nombre_paciente):

    remitente = "neuropausa2@gmail.com"
    password = "usgfquslqylccecx"

    print("====================================")
    print("INICIANDO ENVÍO DE CORREO")
    print("Destino:", correo_paciente)
    print("Nombre :", nombre_paciente)
    print("====================================")

    mensaje = MIMEMultipart()
    mensaje["From"] = remitente
    mensaje["To"] = correo_paciente
    mensaje["Subject"] = "¡Bienvenida a NeuroPausa!"

    html = f"""
    <html>
    <body style="margin:0;padding:0;background:#F5F0E8;font-family:Arial">

    <table width="100%">
    <tr>
    <td align="center">

    <table width="600" style="background:white;border-radius:10px">

    <tr>
    <td style="background:#6B9E7E;padding:30px;text-align:center">

    <img
    src="https://neuropausa-team.github.io/NeuroPausa/assets/images/LogoNeuroGitHub.png"
    width="100">

    <h1 style="color:white">
    NeuroPausa
    </h1>

    </td>
    </tr>

    <tr>

    <td style="padding:40px">

    <h2>¡Hola {nombre_paciente}!</h2>

    <p>
    Tu registro fue exitoso.
    </p>

    <a href="https://neuropausa-team.github.io/NeuroPausa/index.html">
    Acceder a mi cuenta
    </a>

    </td>

    </tr>

    </table>

    </td>
    </tr>
    </table>

    </body>
    </html>
    """

    mensaje.attach(MIMEText(html, "html"))

    try:

        print("Conectando con Gmail...")

        servidor = smtplib.SMTP("smtp.gmail.com", 587)

        print("Conectado.")

        servidor.starttls()

        print("TLS iniciado.")

        servidor.login(remitente, password)

        print("Login correcto.")

        servidor.send_message(mensaje)

        print("Correo enviado correctamente.")

        servidor.quit()

        return True

    except Exception as e:

        print("====================================")
        print("ERROR EN SMTP")
        print(traceback.format_exc())
        print("====================================")

        return False


# ===========================================================
# API
# ===========================================================

@app.route("/api/registrar", methods=["POST"])
def registrar_paciente():

    try:

        print("\n\n========== NUEVA PETICIÓN ==========")

        datos = request.get_json()

        print("JSON recibido:", datos)

        nombre = datos.get("nombre")
        correo = datos.get("correo")

        print("Nombre:", nombre)
        print("Correo:", correo)

        exito = enviar_bienvenida_paciente(correo, nombre)

        print("Resultado:", exito)

        if exito:

            return jsonify({
                "mensaje":"Registro exitoso"
            }),200

        else:

            return jsonify({
                "mensaje":"Falló el envío del correo"
            }),500

    except Exception:

        print(traceback.format_exc())

        return jsonify({
            "error": traceback.format_exc()
        }),500


@app.route("/")
def home():
    return "Backend funcionando"


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )