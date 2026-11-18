from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import os
import sys
import datetime


import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from database.conexion import get_connection

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cambia_esto_por_una_clave_larga_y_random")
CORS(app, supports_credentials=True)


# ===========================================================
# ENVÍO DE CORREO CON BREVO
# ===========================================================

def enviar_bienvenida_paciente(correo_paciente, nombre_paciente):
    try:
        configuration = sib_api_v3_sdk.Configuration()
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
        <body style="margin:0;padding:0;background:#F5F0E8;font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#F5F0E8;padding:20px 0;">
        <tr><td align="center">
        <table width="600" style="background:white;border-radius:10px;overflow:hidden;box-shadow: 0 4px 10px rgba(0,0,0,0.05);">

        <tr><td style="background:#6B9E7E;padding:30px;text-align:center;">
        <img src="https://neuropausa-team.github.io/NeuroPausa/assets/images/ImagenNeuroPausaLogo.png" width="120" style="display:block;margin:0 auto 15px auto;max-width:120px;height:auto;" alt="NeuroPausa Logo">
        <h1 style="color:white;margin:0;font-size:28px;">NeuroPausa</h1>
        <p style="color:#E8F5E9;margin:5px 0 0 0;font-size:14px;">Tu camino hacia el bienestar</p>
        </td></tr>

        <tr><td style="padding:40px 30px;">
        <h2 style="color:#2C3E50;margin-top:0;">¡Hola, {nombre_paciente}! 👋</h2>
        <p style="color:#555;font-size:16px;line-height:1.5;">
            Nos alegra mucho darte la bienvenida a <b>NeuroPausa</b>. Tu cuenta ha sido creada exitosamente y ya puedes acceder a todas nuestras herramientas diseñadas para ayudarte a encontrar el equilibrio y la tranquilidad en tu día a día.
        </p>

        <div style="background:#F8F9FA;border-left:4px solid #6B9E7E;padding:15px;margin:20px 0;border-radius:4px;">
            <p style="margin:0;color:#333;font-size:14px;">
                💡 <b>Consejo rápido:</b> Recuerda tomar descansos activos durante tu jornada para cuidar tu salud mental y física.
            </p>
        </div>

        <p style="color:#555;font-size:16px;line-height:1.5;margin-bottom:30px;">
            Haz clic en el siguiente botón para iniciar sesión en tu cuenta:
        </p>

        <div style="text-align:center;">
            <a href="https://neuropausa-team.github.io/NeuroPausa/login.html" style="background:#6B9E7E;color:white;padding:14px 28px;text-decoration:none;border-radius:6px;font-weight:bold;font-size:16px;display:inline-block;">Acceder a mi cuenta</a>
        </div>
        </td></tr>

        <tr><td style="background:#F1F4F2;padding:20px;text-align:center;color:#888;font-size:12px;">
            <p style="margin:0;">© 2026 NeuroPausa. Todos los derechos reservados.</p>
            <p style="margin:5px 0 0 0;">Lima, Perú</p>
        </td></tr>

        </table></td></tr></table>
        </body></html>
        """

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
# REGISTRO
# ===========================================================

@app.route("/api/registrar", methods=["POST"])
def registrar_paciente():
    try:
        datos = request.get_json()
        if not datos:
            return jsonify({"error": "No se recibieron datos JSON"}), 400

        nombre = datos.get("nombre")
        apellidos = datos.get("apellidos", "")
        correo = datos.get("correo")
        password = datos.get("password")
        confirm_password = datos.get("confirmPassword")

        if not nombre or not correo or not password or not confirm_password:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        if password != confirm_password:
            return jsonify({"error": "Las contraseñas no coinciden"}), 400

        if len(password) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT IdUsuario FROM Usuario WHERE Correo = %s", (correo,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Este correo ya está registrado"}), 400

        cursor.execute("SELECT IdRol FROM Rol WHERE NombreRol = %s", ("Paciente",))
        rol_row = cursor.fetchone()
        if not rol_row:
            conn.close()
            return jsonify({"error": "Rol 'Paciente' no configurado en la base de datos"}), 500
        id_rol = rol_row[0]

        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO Usuario (IdRol, Correo, PasswordHash, Nombre, Apellidos) VALUES (%s, %s, %s, %s, %s)",
            (id_rol, correo, password_hash, nombre, apellidos)
        )
        conn.commit()
        conn.close()

        enviar_bienvenida_paciente(correo, nombre)

        return jsonify({"mensaje": "Registro exitoso"}), 201

    except Exception:
        print("ERROR CRÍTICO EN /api/registrar:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# LOGIN
# ===========================================================

@app.route("/api/login", methods=["POST"])
def login():
    try:
        datos = request.get_json()
        correo = datos.get("correo")
        password = datos.get("password")

        if not correo or not password:
            return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT IdUsuario, PasswordHash, Nombre, OnboardingCompleto FROM Usuario WHERE Correo = %s",
            (correo,)
        )
        usuario = cursor.fetchone()
        conn.close()

        if not usuario or not check_password_hash(usuario[1], password):
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401

        id_usuario, _, nombre, onboarding_completo = usuario

        session['user_id'] = id_usuario
        session['nombre'] = nombre

        return jsonify({
            "mensaje": "Login exitoso",
            "nombre": nombre,
            "onboardingCompleto": bool(onboarding_completo)
        }), 200

    except Exception:
        print("ERROR CRÍTICO EN /api/login:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# LOGOUT
# ===========================================================

@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada"}), 200


# ===========================================================
# COMPLETAR ONBOARDING
# ===========================================================

@app.route("/api/completar-onboarding", methods=["POST"])
def completar_onboarding():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No has iniciado sesión"}), 401

        datos = request.get_json()
        etapa = datos.get("etapa")
        sintomas = datos.get("sintomas", [])
        que_buscas = datos.get("queBuscas")

        sintomas_texto = ", ".join(sintomas)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE Usuario 
            SET Etapa = %s, SintomasInteres = %s, QueBuscas = %s, OnboardingCompleto = TRUE
            WHERE IdUsuario = %s""",
            (etapa, sintomas_texto, que_buscas, session['user_id'])
        )
        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Perfil completado"}), 200

    except Exception:
        print("ERROR EN /api/completar-onboarding:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# USUARIO ACTUAL
# ===========================================================

@app.route("/api/usuario-actual", methods=["GET"])
def usuario_actual():
    if 'user_id' not in session:
        return jsonify({"error": "No hay sesión activa"}), 401

    return jsonify({
        "nombre": session.get('nombre')
    }), 200


# ===========================================================
# ESTADO DEL PERFIL (¿ya tiene DNI registrado?)
# ===========================================================

@app.route("/api/estado-perfil", methods=["GET"])
def estado_perfil():
    if 'user_id' not in session:
        return jsonify({"error": "No hay sesión activa"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
    fila = cursor.fetchone()
    conn.close()

    return jsonify({"tienePerfil": fila is not None}), 200


# ===========================================================
# COMPLETAR PERFIL BÁSICO (DNI, edad, dirección, teléfono)
# ===========================================================

@app.route("/api/completar-perfil-basico", methods=["POST"])
def completar_perfil_basico():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No has iniciado sesión"}), 401

        datos = request.get_json()
        dni = datos.get("dni")
        edad = datos.get("edad")
        direccion = datos.get("direccion", "")
        telefono = datos.get("telefono", "")

        if not dni or not edad:
            return jsonify({"error": "DNI y edad son obligatorios"}), 400

        if len(dni) != 8 or not dni.isdigit():
            return jsonify({"error": "El DNI debe tener 8 dígitos"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Nombre, Apellidos FROM Usuario WHERE IdUsuario = %s", (session['user_id'],))
        usuario_row = cursor.fetchone()
        nombre, apellidos = usuario_row[0], usuario_row[1]

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE DNIPaciente = %s", (dni,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"error": "Este DNI ya está registrado"}), 400

        cursor.execute(
            """INSERT INTO Paciente (DNIPaciente, IdUsuario, Nombre, Apellidos, Edad, Direccion, Telefono)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (dni, session['user_id'], nombre, apellidos, edad, direccion, telefono)
        )
        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Perfil completado"}), 201

    except Exception:
        print("ERROR EN /api/completar-perfil-basico:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# CATÁLOGO DE SÍNTOMAS
# ===========================================================

@app.route("/api/catalogo-sintomas", methods=["GET"])
def catalogo_sintomas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT IdCatSintoma, NombreSintoma, Categoria FROM CatlogoSintoma")
    filas = cursor.fetchall()
    conn.close()

    sintomas = [{"id": f[0], "nombre": f[1], "categoria": f[2]} for f in filas]
    return jsonify(sintomas), 200


# ===========================================================
# REGISTRAR ENTRADA DEL DIARIO
# ===========================================================

@app.route("/api/registrar-diario", methods=["POST"])
def registrar_diario():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No has iniciado sesión"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        paciente_row = cursor.fetchone()
        if not paciente_row:
            conn.close()
            return jsonify({"error": "Debes completar tu perfil (DNI) antes de usar el diario"}), 400
        dni_paciente = paciente_row[0]

        datos = request.get_json()
        energia = datos.get("energia")  # "Difícil", "Regular", "Bien"
        comentarios = datos.get("comentarios", "")
        sintomas = datos.get("sintomas", [])

        mapa_energia = {"Difícil": 1, "Regular": 3, "Bien": 5}
        calidad_sueno = mapa_energia.get(energia)

        if calidad_sueno is None:
            conn.close()
            return jsonify({"error": "Selecciona tu nivel de energía"}), 400

        cursor.execute(
            """INSERT INTO DiarioSintoma (DNIPaciente, FechaRegistro, CalidadSueno, ComentariosGenerales)
               VALUES (%s, CURRENT_DATE, %s, %s)
               RETURNING IdDiario""",
            (dni_paciente, calidad_sueno, comentarios)
        )
        id_diario = cursor.fetchone()[0]

        for s in sintomas:
            cursor.execute(
                """INSERT INTO DetalleDiarioSintoma (IdDiario, IdCatSintoma, Nivelinternsidad)
                   VALUES (%s, %s, %s)""",
                (id_diario, s["idCatSintoma"], s["intensidad"])
            )

        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Registro guardado correctamente"}), 201

    except Exception:
        print("ERROR EN /api/registrar-diario:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# REGISTROS RECIENTES DEL DIARIO
# ===========================================================

@app.route("/api/diario-reciente", methods=["GET"])
def diario_reciente():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No hay sesión activa"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        paciente_row = cursor.fetchone()
        if not paciente_row:
            conn.close()
            return jsonify([]), 200
        dni_paciente = paciente_row[0]

        cursor.execute(
            """
            SELECT
                d.IdDiario,
                d.FechaRegistro,
                d.CalidadSueno,
                STRING_AGG(c.NombreSintoma, ', ') AS Sintomas
            FROM DiarioSintoma d
            LEFT JOIN DetalleDiarioSintoma dd ON dd.IdDiario = d.IdDiario
            LEFT JOIN CatlogoSintoma c ON c.IdCatSintoma = dd.IdCatSintoma
            WHERE d.DNIPaciente = %s
            GROUP BY d.IdDiario, d.FechaRegistro, d.CalidadSueno
            ORDER BY d.FechaRegistro DESC, d.IdDiario DESC
            LIMIT 5
            """,
            (dni_paciente,)
        )
        filas = cursor.fetchall()
        conn.close()

        mapa_energia = {1: "Difícil", 3: "Regular", 5: "Bien"}

        registros = []
        for f in filas:
            registros.append({
                "fecha": f[1].strftime("%d/%m/%Y") if f[1] else "",
                "energia": mapa_energia.get(f[2], "Regular"),
                "sintomas": f[3] if f[3] else "Sin síntomas registrados"
            })

        return jsonify(registros), 200

    except Exception:
        print("ERROR EN /api/diario-reciente:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500

# ===========================================================
# INDICADORES DE SALUD (últimos 7 días)
# ===========================================================

@app.route("/api/indicadores-salud", methods=["GET"])
def indicadores_salud():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No hay sesión activa"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        paciente_row = cursor.fetchone()
        if not paciente_row:
            conn.close()
            return jsonify({
                "diasRegistrados": 0,
                "calidadSueno": "Sin datos",
                "energia": "Sin datos",
                "bienestarSemana": [],
                "sintomas": []
            }), 200
        dni_paciente = paciente_row[0]

        # --- Promedio por día (últimos 7 días) ---
        cursor.execute(
            """
            SELECT FechaRegistro::date AS Fecha, AVG(CAST(CalidadSueno AS FLOAT)) AS Promedio
            FROM DiarioSintoma
            WHERE DNIPaciente = %s AND FechaRegistro >= CURRENT_DATE - INTERVAL '6 days'
            GROUP BY FechaRegistro::date
            """,
            (dni_paciente,)
        )
        filas_dias = cursor.fetchall()
        promedios_por_fecha = {f[0]: f[1] for f in filas_dias}

        # Construir los últimos 7 días con etiqueta Lun/Mar/...
        import datetime
        dias_semana = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        hoy = datetime.date.today()
        bienestar_semana = []
        for i in range(6, -1, -1):
            fecha = hoy - datetime.timedelta(days=i)
            valor = promedios_por_fecha.get(fecha, 0)
            bienestar_semana.append({
                "dia": dias_semana[fecha.weekday()],
                "valor": round(valor, 1) if valor else 0
            })

        dias_registrados = len(promedios_por_fecha)

        # --- Calidad de sueño promedio (últimos 7 días) ---
        valores = [v for v in promedios_por_fecha.values() if v]
        if valores:
            promedio_general = sum(valores) / len(valores)
            if promedio_general < 2:
                calidad_sueno = "Baja"
            elif promedio_general < 4:
                calidad_sueno = "Media"
            else:
                calidad_sueno = "Alta"
        else:
            calidad_sueno = "Sin datos"

        # --- Nivel de energía (heurística simple según consistencia) ---
        energia = "Estable" if dias_registrados >= 4 else "Variable"

        # --- Síntomas más frecuentes (últimos 7 días) ---
        cursor.execute(
            """
            SELECT c.NombreSintoma, COUNT(DISTINCT dd.IdDiario) AS Cantidad
            FROM DetalleDiarioSintoma dd
            JOIN CatlogoSintoma c ON c.IdCatSintoma = dd.IdCatSintoma
            JOIN DiarioSintoma d ON d.IdDiario = dd.IdDiario
            WHERE d.DNIPaciente = %s AND d.FechaRegistro >= CURRENT_DATE - INTERVAL '6 days'
            GROUP BY c.NombreSintoma
            ORDER BY Cantidad DESC
            LIMIT 1
            """,
            (dni_paciente,)
        )
        filas_sintomas = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(DISTINCT IdDiario) FROM DiarioSintoma
            WHERE DNIPaciente = %s AND FechaRegistro >= CURRENT_DATE - INTERVAL '6 days'
            """,
            (dni_paciente,)
        )
        total_registros = cursor.fetchone()[0] or 0

        conn.close()

        sintomas = []
        if total_registros > 0:
            for f in filas_sintomas:
                porcentaje = round((f[1] / total_registros) * 100)
                sintomas.append({"nombre": f[0], "porcentaje": porcentaje})

        return jsonify({
            "diasRegistrados": dias_registrados,
            "calidadSueno": calidad_sueno,
            "energia": energia,
            "bienestarSemana": bienestar_semana,
            "sintomas": sintomas
        }), 200

    except Exception:
        print("ERROR EN /api/indicadores-salud:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# DATOS DEL PERFIL (para la página Perfil)
# ===========================================================

@app.route("/api/perfil-datos", methods=["GET"])
def perfil_datos():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No hay sesión activa"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT Nombre, Apellidos, Correo, Etapa, FechaRegistro FROM Usuario WHERE IdUsuario = %s",
            (session['user_id'],)
        )
        u = cursor.fetchone()
        nombre, apellidos, correo, etapa, fecha_registro = u

        # Buscar datos de Paciente si ya completó su perfil
        cursor.execute(
            "SELECT DNIPaciente, Telefono, Direccion FROM Paciente WHERE IdUsuario = %s",
            (session['user_id'],)
        )
        p = cursor.fetchone()
        telefono = p[1] if p else ""
        direccion = p[2] if p else ""
        dni_paciente = p[0] if p else None

        # Calcular racha real (días consecutivos con registro en el Diario)
        racha = 0
        if dni_paciente:
            cursor.execute(
                """SELECT DISTINCT FechaRegistro::date AS Fecha
                FROM DiarioSintoma WHERE DNIPaciente = %s
                ORDER BY Fecha DESC""",
                (dni_paciente,)
            )
            fechas = [f[0] for f in cursor.fetchall()]
            if fechas:
                racha = 1
                for i in range(1, len(fechas)):
                    if (fechas[i-1] - fechas[i]).days == 1:
                        racha += 1
                    else:
                        break

        conn.close()

        return jsonify({
            "nombre": nombre,
            "apellidos": apellidos or "",
            "correo": correo,
            "etapa": etapa or "No definida",
            "miembroDesde": fecha_registro.strftime("%B %Y") if fecha_registro else "",
            "racha": racha,
            "telefono": telefono,
            "direccion": direccion
        }), 200

    except Exception:
        print("ERROR EN /api/perfil-datos:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500


# ===========================================================
# ACTUALIZAR PERFIL (nombre, apellidos, teléfono, dirección)
# ===========================================================

@app.route("/api/actualizar-perfil", methods=["POST"])
def actualizar_perfil():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No has iniciado sesión"}), 401

        datos = request.get_json()
        nombre = datos.get("nombre")
        apellidos = datos.get("apellidos", "")
        telefono = datos.get("telefono", "")
        direccion = datos.get("direccion", "")

        if not nombre:
            return jsonify({"error": "El nombre es obligatorio"}), 400

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE Usuario SET Nombre = %s, Apellidos = %s WHERE IdUsuario = %s",
            (nombre, apellidos, session['user_id'])
        )

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        p = cursor.fetchone()
        if p:
            cursor.execute(
                "UPDATE Paciente SET Nombre = %s, Apellidos = %s, Telefono = %s, Direccion = %s WHERE IdUsuario = %s",
                (nombre, apellidos, telefono, direccion, session['user_id'])
            )

        conn.commit()
        conn.close()

        session['nombre'] = nombre

        return jsonify({"mensaje": "Perfil actualizado correctamente"}), 200

    except Exception:
        print("ERROR EN /api/actualizar-perfil:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500

# ===========================================================
# ESPECIALIDADES
# ===========================================================

@app.route("/api/especialidades", methods=["GET"])
def especialidades():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT IdEspecialidad, Nombre FROM EspecialidadMedica")
    filas = cursor.fetchall()
    conn.close()
    return jsonify([{"id": f[0], "nombre": f[1]} for f in filas]), 200


# ===========================================================
# LISTA DE ESPECIALISTAS (opcional filtro por especialidad)
# ===========================================================

@app.route("/api/especialistas", methods=["GET"])
def especialistas():
    id_especialidad = request.args.get("especialidad")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT d.DNIDoctor, d.Nombre, d.Apellidos, e.Nombre AS Especialidad, d.CentroAfiliado
        FROM Doctor d
        JOIN DoctorEspecialidad de ON de.DNIDoctor = d.DNIDoctor
        JOIN EspecialidadMedica e ON e.IdEspecialidad = de.IdEspecialidad
    """
    params = ()
    if id_especialidad:
        query += " WHERE de.IdEspecialidad = %s"
        params = (id_especialidad,)

    cursor.execute(query, params)
    filas = cursor.fetchall()
    conn.close()

    doctores = [{
        "dni": f[0],
        "nombre": f"Dra. {f[1]} {f[2]}",
        "especialidad": f[3],
        "centroAfiliado": f[4]
    } for f in filas]

    return jsonify(doctores), 200

# ===========================================================
# SEDES DISPONIBLES
# ===========================================================

@app.route("/api/sedes", methods=["GET"])
def sedes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT IdSede, NombreSede, Direccion FROM Sede")
    filas = cursor.fetchall()
    conn.close()
    return jsonify([{"id": f[0], "nombre": f[1], "direccion": f[2]} for f in filas]), 200


# ===========================================================
# AGENDAR CITA
# ===========================================================

@app.route("/api/agendar-cita", methods=["POST"])
def agendar_cita():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No has iniciado sesión"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        paciente_row = cursor.fetchone()
        if not paciente_row:
            conn.close()
            return jsonify({"error": "Debes completar tu perfil (DNI) antes de agendar una cita"}), 400
        dni_paciente = paciente_row[0]

        datos = request.get_json()
        dni_doctor = datos.get("dniDoctor")
        modalidad = datos.get("modalidad")  # "Presencial" | "Virtual"
        id_sede = datos.get("idSede")  # puede ser None si es Virtual
        fecha_hora = datos.get("fechaHora")  # ISO string, ej "2026-08-29T09:30:00"


        from datetime import datetime as dt
        try:
            fecha_hora_dt = dt.fromisoformat(fecha_hora.replace('Z', '+00:00'))
        except ValueError:
            conn.close()
            return jsonify({"error": "Formato de fecha inválido"}), 400

        if fecha_hora_dt.replace(tzinfo=None) <= dt.utcnow():
            conn.close()
            return jsonify({"error": "No puedes agendar una cita en el pasado"}), 400





        cursor.execute(
            """INSERT INTO Cita (DNIPaciente, DNIDoctor, IdSede, FechaHoraCita, TipoCita, Estado)
            VALUES (%s, %s, %s, %s, %s, 'Programada')""",
            (dni_paciente, dni_doctor, id_sede if modalidad == "Presencial" else None, fecha_hora, modalidad)
        )
        conn.commit()
        conn.close()

        return jsonify({"mensaje": "Cita agendada correctamente"}), 201

    except Exception:
        print("ERROR EN /api/agendar-cita:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500

# ===========================================================
# RESUMEN PARA EL DASHBOARD (Inicio)
# ===========================================================

@app.route("/api/resumen-inicio", methods=["GET"])
def resumen_inicio():
    try:
        if 'user_id' not in session:
            return jsonify({"error": "No hay sesión activa"}), 401

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DNIPaciente FROM Paciente WHERE IdUsuario = %s", (session['user_id'],))
        p = cursor.fetchone()

        if not p:
            conn.close()
            return jsonify({"racha": 0, "sintomaFrecuente": "--"}), 200

        dni_paciente = p[0]

        # Racha (días consecutivos)
        cursor.execute(
            """SELECT DISTINCT FechaRegistro::date AS Fecha
            FROM DiarioSintoma WHERE DNIPaciente = %s
            ORDER BY Fecha DESC""",
            (dni_paciente,)
        )
        fechas = [f[0] for f in cursor.fetchall()]
        racha = 0
        if fechas:
            racha = 1
            for i in range(1, len(fechas)):
                if (fechas[i-1] - fechas[i]).days == 1:
                    racha += 1
                else:
                    break

        # Síntoma más frecuente (histórico, no solo la semana)
        cursor.execute(
            """
            SELECT c.NombreSintoma, COUNT(*) AS Cantidad
            FROM DetalleDiarioSintoma dd
            JOIN CatlogoSintoma c ON c.IdCatSintoma = dd.IdCatSintoma
            JOIN DiarioSintoma d ON d.IdDiario = dd.IdDiario
            WHERE d.DNIPaciente = %s
            GROUP BY c.NombreSintoma
            ORDER BY Cantidad DESC
            LIMIT 1
            """,
            (dni_paciente,)
        )
        fila_sintoma = cursor.fetchone()
        sintoma_frecuente = fila_sintoma[0] if fila_sintoma else "Sin datos"

        conn.close()

        return jsonify({
            "racha": racha,
            "sintomaFrecuente": sintoma_frecuente
        }), 200

    except Exception:
        print("ERROR EN /api/resumen-inicio:")
        print(traceback.format_exc())
        return jsonify({"error": "Error interno del servidor"}), 500






    
@app.route("/")
def home():
    return "Backend funcionando"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)