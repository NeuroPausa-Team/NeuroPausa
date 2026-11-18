import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def enviar_bienvenida_paciente(correo_paciente, nombre_paciente):
    # Configurar la API key de Brevo
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = os.getenv("BREVO_API_KEY")

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    # El diseño HTML exacto que tenías preparado
    html = f"""
    <html>
    <body style="margin: 0; padding: 0; background-color: #F5F0E8; font-family: 'Open Sans', Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #F5F0E8; padding: 30px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" style="background-color: #FFFFFF; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                        
                        <!-- CABECERA CON LOGO Y COLOR VERDE SALVIA -->
                        <tr>
                            <td style="background-color: #6B9E7E; text-align: center; padding: 30px;">
                                <img src="https://neuropausa-team.github.io/NeuroPausa/assets/images/LogoNeuroGitHub.png" width="100" style="margin-bottom: 10px;">
                                <h1 style="color: #FFFFFF; margin: 0; font-family: 'Montserrat', Arial, sans-serif; font-size: 28px;">NeuroPausa</h1>
                            </td>
                        </tr>
                        
                        <!-- CUERPO DEL MENSAJE -->
                        <tr>
                            <td style="padding: 40px; color: #3D3830;">
                                <h2 style="color: #4A7A5A; margin-top: 0;">¡Hola, {nombre_paciente}!</h2>
                                <p style="font-size: 16px; line-height: 1.6;">Tu registro se ha completado exitosamente. Estamos muy felices de acompañarte en tu transición hacia el bienestar.</p>
                                <p style="font-size: 16px; line-height: 1.6;">Desde ahora podrás registrar tus síntomas diarios, acceder a ejercicios de estimulación cognitiva y mantener el control de tu salud con empatía y rigor científico.</p>
                                
                                <!-- BOTÓN DE ACCIÓN (Verde Menta Suave) -->
                                <div style="text-align: center; margin-top: 35px; margin-bottom: 10px;">
                                    <a href="https://neuropausa-team.github.io/NeuroPausa/index.html" style="background-color: #8CB89A; color: #FFFFFF; text-decoration: none; padding: 14px 30px; border-radius: 5px; font-size: 16px; font-weight: bold; display: inline-block;">Acceder a mi cuenta</a>
                                </div>
                            </td>
                        </tr>
                        
                        <!-- PIE DE PÁGINA (GRIS TOPO) -->
                        <tr>
                            <td style="background-color: #F5F0E8; text-align: center; padding: 20px; font-size: 12px; color: #9B9189;">
                                <p style="margin: 5px 0;">Este es un mensaje automático, por favor no respondas a este correo.</p>
                                <p style="margin: 5px 0;">&copy; 2026 NeuroPausa Team. Todos los derechos reservados.</p>
                            </td>
                        </tr>
                        
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Crear el objeto de correo para Brevo
    correo = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": "NeuroPausa",
            "email": "neuropausa2@gmail.com"
        },
        to=[
            {
                "email": correo_paciente,
                "name": nombre_paciente
            }
        ],
        subject="¡Bienvenida a NeuroPausa!",
        html_content=html
    )

    # Enviar a través de la API HTTP de Brevo
    try:
        api_instance.send_transac_email(correo)
        print(f"¡Correo de bienvenida enviado exitosamente a {correo_paciente}!")
        return True
    except ApiException as e:
        print(f"Error al enviar el correo con Brevo: {e}")
        return False