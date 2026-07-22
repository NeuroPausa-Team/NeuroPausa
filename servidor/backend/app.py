from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
# Habilitar CORS permite que tu HTML (incluso desde GitHub Pages) se comunique con este servidor
CORS(app) 

# Esta es tu función de correo (la misma que ya probaste y funciona)
def enviar_bienvenida_paciente(correo_paciente, nombre_paciente):
    remitente = "neuropausa2@gmail.com" 
    password = "usgfquslqylccecx" 

    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = correo_paciente
    mensaje['Subject'] = "¡Bienvenida a NeuroPausa!"

    html = f"""
    <html>
    <body style="margin: 0; padding: 0; background-color: #F5F0E8; font-family: 'Open Sans', Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #F5F0E8; padding: 30px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #FFFFFF; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background-color: #6B9E7E; text-align: center; padding: 30px;">
                                <img src="https://neuropausa-team.github.io/NeuroPausa/assets/images/LogoNeuroGitHub.png" alt="Logo NeuroPausa" width="100" style="margin-bottom: 10px;">
                                <h1 style="color: #FFFFFF; margin: 0; font-family: 'Montserrat', Arial, sans-serif; font-size: 28px;">NeuroPausa</h1>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 40px; color: #3D3830;">
                                <h2 style="color: #4A7A5A; margin-top: 0;">¡Hola, {nombre_paciente}!</h2>
                                <p style="font-size: 16px; line-height: 1.6;">Tu registro se ha completado exitosamente. Estamos muy felices de acompañarte en tu transición hacia el bienestar.</p>
                                <p style="font-size: 16px; line-height: 1.6;">Desde ahora podrás registrar tus síntomas diarios, acceder a ejercicios de estimulación cognitiva y mantener el control de tu salud con empatía y rigor científico.</p>
                                <div style="text-align: center; margin-top: 35px; margin-bottom: 10px;">
                                    <a href="https://neuropausa-team.github.io/NeuroPausa/index.html" style="background-color: #8CB89A; color: #FFFFFF; text-decoration: none; padding: 14px 30px; border-radius: 5px; font-size: 16px; font-weight: bold; display: inline-block;">Acceder a mi cuenta</a>
                                </div>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(html, 'html'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.send_message(mensaje)
        servidor.quit()
        return True
    except Exception as e:
        print(f"Error al enviar: {e}")
        return False

# ==========================================
# CREACIÓN DE LA API (El puente con tu HTML)
# ==========================================
import traceback

@app.route('/api/registrar', methods=['POST'])
def registrar_paciente():
    try:
        datos = request.json
        nombre = datos.get('nombre')
        correo = datos.get('correo')
        
        # Enviar el correo
        exito = enviar_bienvenida_paciente(correo, nombre)
        
        if exito:
            return jsonify({"mensaje": "Registro exitoso y correo enviado"}), 200
        else:
            return jsonify({"error": "No se pudo enviar el correo"}), 500

    except Exception as e:
        print("ERROR CRITICO EN PYTHON:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)