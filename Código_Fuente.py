import datetime

# ==========================================
# 1. PERSISTENCIA DE DATOS 
# ==========================================
tabla_pacientes = {
    35444888: {"nombre": "Juan", "apellido": "Perez", "telefono": "1123456789"},
    40123456: {"nombre": "Maria", "apellido": "Gomez", "telefono": "1198765432"}
}

# Modificado con las nuevas especialidades solicitadas
tabla_especialidades = {
    1: "Cardiologia",
    2: "Dermatologia",
    3: "Traumatologia",
    4: "Medico Clinico",
    5: "Oftalmologia"
}

# Agenda actualizada que distribuye turnos para las nuevas especialidades
tabla_agenda_turnos = [
    # ---- CARDIOLOGÍA (ID: 1) ----
    {"id_turno": 101, "id_especialidad": 1, "medico": "Dra. Martinez", "fecha_hora": "2026-06-22 09:00", "estado": "Disponible"},
    {"id_turno": 102, "id_especialidad": 1, "medico": "Dra. Martinez", "fecha_hora": "2026-06-22 11:30", "estado": "Ocupado"},
    {"id_turno": 103, "id_especialidad": 1, "medico": "Dr. Rossi", "fecha_hora": "2026-06-23 16:00", "estado": "Disponible"},

    # ---- DERMATOLOGÍA (ID: 2) ----
    {"id_turno": 104, "id_especialidad": 2, "medico": "Dr. Facchini", "fecha_hora": "2026-06-22 10:00", "estado": "Disponible"},
    {"id_turno": 105, "id_especialidad": 2, "medico": "Dr. Facchini", "fecha_hora": "2026-06-22 10:30", "estado": "Disponible"},
    {"id_turno": 106, "id_especialidad": 2, "medico": "Dra. Sola", "fecha_hora": "2026-06-25 18:15", "estado": "Ocupado"},

    # ---- TRAUMATOLOGÍA (ID: 3) ----
    {"id_turno": 107, "id_especialidad": 3, "medico": "Dr. Casares", "fecha_hora": "2026-06-23 14:00", "estado": "Ocupado"},
    {"id_turno": 108, "id_especialidad": 3, "medico": "Dr. Casares", "fecha_hora": "2026-06-23 14:45", "estado": "Disponible"},
    {"id_turno": 109, "id_especialidad": 3, "medico": "Dra. Lopez", "fecha_hora": "2026-06-26 08:30", "estado": "Disponible"},

    # ---- MÉDICO CLÍNICO (ID: 4) ----
    {"id_turno": 110, "id_especialidad": 4, "medico": "Dra. Rossi", "fecha_hora": "2026-06-24 09:15", "estado": "Disponible"},
    {"id_turno": 111, "id_especialidad": 4, "medico": "Dr. Alvarez", "fecha_hora": "2026-06-24 11:00", "estado": "Disponible"},
    {"id_turno": 112, "id_especialidad": 4, "medico": "Dr. Alvarez", "fecha_hora": "2026-06-24 12:30", "estado": "Ocupado"},

    # ---- OFTALMOLOGÍA (ID: 5) - Todo Ocupado para simular el Camino Infeliz ----
    {"id_turno": 113, "id_especialidad": 5, "medico": "Dr. Peralta", "fecha_hora": "2026-06-25 15:30", "estado": "Ocupado"},
    {"id_turno": 114, "id_especialidad": 5, "medico": "Dr. Peralta", "fecha_hora": "2026-06-25 16:00", "estado": "Ocupado"},
    {"id_turno": 115, "id_especialidad": 5, "medico": "Dra. Vega", "fecha_hora": "2026-06-27 10:15", "estado": "Ocupado"}
]

# ==========================================
# 2. MÁQUINA DE ESTADOS
# ==========================================
ESTADO_INICIO = "ESTADO_INICIO"
ESTADO_ESPERANDO_DNI = "ESTADO_ESPERANDO_DNI"
ESTADO_REGISTRANDO_PACIENTE = "ESTADO_REGISTRANDO_PACIENTE"
ESTADO_ESPERANDO_ESPECIALIDAD = "ESTADO_ESPERANDO_ESPECIALIDAD"
ESTADO_ESPERANDO_HORARIO = "ESTADO_ESPERANDO_HORARIO"
ESTADO_ESPERANDO_CONFIRMACION = "ESTADO_ESPERANDO_CONFIRMACION"
ESTADO_FIN = "ESTADO_FIN"

def simular_bot():
    estado_actual = ESTADO_INICIO
    contexto_usuario = {}
    
    print("////////// ASISTENTE VIRTUAL DE TURNOS MÉDICOS INICIADO //////////")
    
    while estado_actual != ESTADO_FIN:
        
        # --- ESTADO INICIO ---
        if estado_actual == ESTADO_INICIO:
            print("Turni: ¡Hola! Bienvenido al sistema de autogestión de turnos médicos.")
            print("Turni: Soy Turni, el Bot que te ayudará a gestionar tus turnos médicos")
            print("Turni: Por favor, ingresá tu número de DNI (solo números, sin puntos):")
            estado_actual = ESTADO_ESPERANDO_DNI
            
        # --- ESTADO ESPERANDO DNI (Validación y Compuerta 1) ---
        elif estado_actual == ESTADO_ESPERANDO_DNI:
            entrada = input("Usuario: ").strip()
            
            # Camino Infeliz: Entrada no numérica
            if not entrada.isdigit():
                print("-------------------------------------------------------------------------------------------")
                print("Turni: [!] El DNI debe contener solo números y sin puntos. Por favor, ingresalo nuevamente.")
                continue
                
            dni = int(entrada)
            contexto_usuario["dni"] = dni
            
            print(f"Turni: [Verificando DNI {dni} en Base de Datos...]")
            if dni in tabla_pacientes:
                # Camino SÍ: Paciente Registrado
                paciente = tabla_pacientes[dni]
                print("-------------------------------------------------------------------------------------------")
                print(f"Turni: ¡Bienvenido, me alegra verte de nuevo, {paciente['nombre']} {paciente['apellido']}!")
                estado_actual = ESTADO_ESPERANDO_ESPECIALIDAD
            else:
                # Camino NO: Paciente Nuevo
                print("-------------------------------------------------------------------------------------------")
                print("Turni: No te encontré en nuestro sistema. Vamos a realizar tu registro rápido.")
                estado_actual = ESTADO_REGISTRANDO_PACIENTE

        # --- ESTADO REGISTRANDO PACIENTE (Camino NO del BPMN) ---
        elif estado_actual == ESTADO_REGISTRANDO_PACIENTE:
            nombre = input("Turni: Ingresá tu Nombre: ").strip()
            apellido = input("Turni: Ingresá tu Apellido: ").strip()
            telefono = input("Turni: Ingresá un número de contacto: ").strip()
            
            # Guardado automático en persistencia simulada
            tabla_pacientes[contexto_usuario["dni"]] = {
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono
            }
            print("Turni: ¡Registro completado con éxito!")
            estado_actual = ESTADO_ESPERANDO_ESPECIALIDAD

        # --- ESTADO ESPERANDO ESPECIALIDAD ---
        elif estado_actual == ESTADO_ESPERANDO_ESPECIALIDAD:
            print("Turni: Estas son nuestras especialidades disponibles:")
            for id_esp, nombre_esp in tabla_especialidades.items():
                print(f"  [{id_esp}] {nombre_esp}")
                
            entrada = input("Turni: Seleccioná el número de la especialidad: ").strip()
            
            # Camino Infeliz: Opción inválida o fuera de rango
            if not entrada.isdigit() or int(entrada) not in tabla_especialidades:
                print("Turni: [!] Opción no válida. Por favor, selecciona un número correspondiente a la lista.")
                continue
                
            id_seleccionado = int(entrada)
            contexto_usuario["id_especialidad"] = id_seleccionado
            print(f"Turni: Consultando agenda de turnos para {tabla_especialidades[id_seleccionado]}...")
            
            # CAMBIO AQUÍ: Ahora traemos TODOS los turnos de la especialidad (tanto Disponibles como Ocupados)
            turnos_totales = [t for t in tabla_agenda_turnos if t["id_especialidad"] == id_seleccionado]
            
            if not turnos_totales:
                print("Turni: [!] En este momento no hay turnos cargados para esta especialidad.")
                print("Turni: Proceso finalizado.")
                estado_actual = ESTADO_FIN
            else:
                contexto_usuario["turnos_opciones"] = turnos_totales
                estado_actual = ESTADO_ESPERANDO_HORARIO

        # --- ESTADO ESPERANDO HORARIO (Con validación de ocupado) ---
        elif estado_actual == ESTADO_ESPERANDO_HORARIO:
            print("-------------------------------------------------------------------------------------------")
            print("Turni: Agenda de turnos para la especialidad seleccionada:")
            opciones = contexto_usuario["turnos_opciones"]
            
            # Mostramos todos, pero aclaramos si está Disponible u Ocupado
            for indice, turno in enumerate(opciones):
                estado_visual = "Disponible" if turno['estado'] == "Disponible" else "OCUPADO"
                print(f"  [{indice + 1}] {turno['fecha_hora']} con el/la {turno['medico']} ({estado_visual})")
                
            entrada = input("Turni: Seleccioná el número del horario deseado: ").strip()
            
            # Camino Infeliz 1: Opción fuera de rango de la lista
            if not entrada.isdigit() or int(entrada) < 1 or int(entrada) > len(opciones):
                print("Turni: [!] Opción no válida. Elija un número de la lista mostrada.")
                continue
                
            turno_elegido = opciones[int(entrada) - 1]
            
            # NUEVO CAMINO INFELIZ 2: El usuario elige un turno que figura como OCUPADO
            if turno_elegido["estado"] == "Ocupado":
                print(f"Turni: [!] El turno del {turno_elegido['fecha_hora']} ya no se encuentra disponible.")
                print("Turni: Alguien reservó este cupo recientemente. Por favor, selecciona otra opción que esté libre.")
                # Al no cambiar el estado_actual, el bucle se repite y le vuelve a mostrar la lista para que elija bien.
                continue
                
            # Si pasa la validación (está Disponible), avanza al camino feliz
            contexto_usuario["turno_elegido"] = turno_elegido
            estado_actual = ESTADO_ESPERANDO_CONFIRMACION

        # --- ESTADO ESPERANDO CONFIRMACIÓN (Compuerta Final) ---
        elif estado_actual == ESTADO_ESPERANDO_CONFIRMACION:
            t = contexto_usuario["turno_elegido"]
            esp_nombre = tabla_especialidades[contexto_usuario["id_especialidad"]]
            print("-------------------------------------------------------------------------------------------")
            print(f"Turni: --- RESUMEN DE TU RESERVA ---")
            print(f"Especialidad: {esp_nombre}")
            print(f"Médico: {t['medico']}")
            print(f"Fecha y Hora: {t['fecha_hora']}")
            
            respuesta = input("Turni: ¿Confirmás la reserva de este turno? (SI/NO): ").strip().upper()
            
            if respuesta == "SI":
                # Camino SÍ: Éxito
                # Cambiar el estado del turno en la BD simulada
                for turno_bd in tabla_agenda_turnos:
                    if turno_bd["id_turno"] == t["id_turno"]:
                        turno_bd["estado"] = "Ocupado"
                
                print("Turni: ¡Turno asignado exitosamente!")
                print(f"Turni: Se generó tu comprobante nro #{t['id_turno']}. ¡Te esperamos!")
                estado_actual = ESTADO_FIN
            elif respuesta == "NO":
                # Camino NO: Cancelación
                print("Turni: El turno no ha sido reservado.")
                print("Turni: Proceso finalizado - Turno cancelado por el usuario.")
                estado_actual = ESTADO_FIN
            else:
                # Camino Infeliz: Respuesta ambigua
                print("Turni: [!] No entendí tu respuesta. Por favor, responde escribiendo SI o NO.")
                continue

    print("////////// ASISTENTE VIRTUAL DE TURNOS MÉDICOS FINALIZADO //////////")

# Ejecución de la simulación
if __name__ == "__main__":
    simular_bot()