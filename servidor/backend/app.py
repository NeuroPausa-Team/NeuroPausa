from flask import Flask, request, jsonify
from flask_cors import CORS
import traceback
import os

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

app = Flask(__name__)
CORS(app)


# ===========================================================
# ENVÍO DE CORREO CON BREVO
# ===========================================================

def enviar_bienvenida_paciente(correo_paciente, nombre_paciente):
    try:
        configuration = sib_api_v3_sdk.Configuration()
        # Aseguramos la lectura de la variable de entorno
        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            print("ERROR: La variable BREVO_API_KEY no está configurada en el entorno.")
            return False
            
        configuration.api_key["api-key"] = api_key

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        html = f"""
        <html>
        <body style="margin:0;padding:0;background:#F5F0E8;font-family:Arial">
        <table width="100%">
        <tr>
        <td align="center">
        <table width="600" style="background:white;border-radius:10px">
        <tr>
        <td style="background:#6B9E7E;padding:30px;text-align:center">
        <img src="https://neuropausa-team.github.io/NeuroPausa/assets/images/LogoNeuroGitHub.png" width="100">
        <h1 style="color:white">NeuroPausa</h1>
        </td>
        </tr>
        <tr>
        <td style="padding:40px">
        <h2>¡Hola {nombre_paciente}!</h2>
        <p>Tu registro se ha completado exitosamente.</p>
        <a href="https://neuropausa-team.github.io/NeuroPausa/index.html" style="background:#6B9E7E;color:white;padding:12px 20px;text-decoration:none;border-radius:5px;">Acceder a mi cuenta</a>
        </td>
        </tr>
        </table>
        </td>
        </tr>
        </table>
        </body>
        </html>
        """

        # Construcción correcta del objeto SendSmtpEmail para la SDK de Brevo
        remitente = {"name": "NeuroPausa", "email": "neuropausa2@gmail.com"}
        destinatario = [{"email": correo_paciente, "name": nombre_paciente}]

        correo = sib_api_v3_sdk.SendSmtpEmail(
            sender=remitente,
            to=destinatario,
            subject="¡Bienvenida a NeuroPausa!",
            html_content=html
        )

        api_instance.send_transac_email(correo)
        print("¡Correo enviado correctamente a través de Brevo!")
        return True

    except ApiException as e:
        print(f"Error de API Brevo detallado: {e}")
        if hasattr(e, 'body'):
            print(f"Cuerpo del error de Brevo: {e.body}")
        return False
    except Exception as ex:
        print(f"Error general en envío de correo: {ex}")
        return False


# ===========================================================
# API
# ===========================================================

@app.route("/api/registrar", methods=["POST"])
def registrar_paciente():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        nombre = datos.get("nombre")
        correo = datos.get("correo")

        if not nombre or not correo:
            return jsonify({"error": "Faltan campos obligatorios (nombre o correo)"}), 400

        exito = enviar_bienvenida_paciente(correo, nombre)

        if exito:
            return jsonify({"mensaje": "Registro exitoso"}), 200
        else:
            return jsonify({"mensaje": "No se pudo enviar el correo"}), 500

    except Exception:
        print("ERROR CRÍTICO EN /api/registrar:")
        print(traceback.format_exc())
        return jsonify({"error": traceback.format_exc()}), 500


@app.route("/")
def home():
    return "Backend funcionando"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)