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
        <img src="https://neuropausa-team.github.io/NeuroPausa/assets/images/ImagenNeuroPausaLogo.png" width="120">
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
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        # Intentamos enviar el correo y capturamos cualquier fallo de Brevo
        configuration = sib_api_v3_sdk.Configuration()
        api_key = os.getenv("BREVO_API_KEY")
        if not api_key:
            return jsonify({"error": "Falta configurar la variable BREVO_API_KEY en Render"}), 500
            
        configuration.api_key["api-key"] = api_key
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

        html = f"""
        <html>
        <body style="margin:0;padding:0;background:#F5F0E8;font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F0E8;padding:20px 0;">
        <tr><td align="center">
        <table width="600" style="background:white;border-radius:10px;overflow:hidden;box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
        
        <!-- Cabecera -->
        <tr><td style="background:#6B9E7E;padding:30px;text-align:center;">
        <h1 style="color:white;margin:0;font-size:28px;">NeuroPausa</h1>
        <p style="color:#E8F5E9;margin:5px 0 0 0;font-size:14px;">Tu camino hacia el bienestar</p>
        </td></tr>
        
        <!-- Cuerpo de información -->
        <tr><td style="padding:40px 30px;">
        <h2 style="color:#2C3E50;margin-top:0;">¡Hola, {nombre}! 👋</h2>
        <p style="color:#555;font-size:16px;line-height:1.5;">
            Nos alegra mucho darte la bienvenida a <b>NeuroPausa</b>. Tu cuenta ha sido creada exitosamente y ya puedes acceder a todas nuestras herramientas diseñadas para ayudarte a encontrar el equilibrio y la tranquilidad en tu día a día.
        </p>
        
        <!-- Caja de información destacada -->
        <div style="background:#F8F9FA;border-left:4px solid #6B9E7E;padding:15px;margin:20px 0;border-radius:4px;">
            <p style="margin:0;color:#333;font-size:14px;">
                💡 <b>Consejo rápido:</b> Recuerda tomar descansos activos durante tu jornada para cuidar tu salud mental y física.
            </p>
        </div>

        <p style="color:#555;font-size:16px;line-height:1.5;margin-bottom:30px;">
            Haz clic en el siguiente botón para iniciar sesión en tu cuenta:
        </p>

        <!-- Botón de acción -->
        <div style="text-align:center;">
            <a href="https://neuropausa-team.github.io/NeuroPausa/login.html" style="background:#6B9E7E;color:white;padding:14px 28px;text-decoration:none;border-radius:6px;font-weight:bold;font-size:16px;display:inline-block;">Acceder a mi cuenta</a>
        </div>
        </td></tr>

        <!-- Pie de página -->
        <tr><td style="background:#F1F4F2;padding:20px;text-align:center;color:#888;font-size:12px;">
            <p style="margin:0;">© 2026 NeuroPausa. Todos los derechos reservados.</p>
            <p style="margin:5px 0 0 0;">Lima, Perú</p>
        </td></tr>

        </table></td></tr></table>
        </body></html>
        """

        correo_obj = sib_api_v3_sdk.SendSmtpEmail(
            sender={"name": "NeuroPausa", "email": "neuropausa2@gmail.com"},
            to=[{"email": correo, "name": nombre}],
            subject="¡Bienvenida a NeuroPausa!",
            html_content=html
        )

        api_instance.send_transac_email(correo_obj)
        return jsonify({"mensaje": "Registro exitoso"}), 200

    except ApiException as e:
        # AQUÍ ESTÁ EL TRUCO: Devolvemos el error exacto de Brevo a la pantalla
        error_detallado = e.body if hasattr(e, 'body') else str(e)
        print("Error ApiException:", error_detallado)
        return jsonify({"error": f"Brevo API Error: {error_detallado}"}), 500

    except Exception as ex:
        print("Error General:", str(ex))
        return jsonify({"error": f"Error interno: {str(ex)}"}), 500

@app.route("/")
def home():
    return "Backend funcionando"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)