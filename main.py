# LIBRERIAS
import csv
import datetime

# BASE DE DATOS 
ARCHIVO_PACIENTES = "pacientes.csv"
ARCHIVO_ESPECIALIDADES = "especialidades.csv"
ARCHIVO_TURNOS = "agenda_turnos.csv"
ARCHIVO_AUDITORIA = "auditoria.csv"

# ESTRUCTURAS
CAMPOS_PACIENTES = ["dni", "nombre", "apellido", "telefono"]
CAMPOS_TURNOS = ["id_turno", "id_especialidad", "medico", "fecha_hora", "estado", "dni_paciente"]
CAMPOS_AUDITORIA = ["fecha_hora", "dni", "estado", "mensaje"]

# MÁQUINA DE ESTADOS
ESTADO_INICIO = "ESTADO_INICIO"
ESTADO_ESPERANDO_DNI = "ESTADO_ESPERANDO_DNI"
ESTADO_REGISTRANDO_PACIENTE = "ESTADO_REGISTRANDO_PACIENTE"
ESTADO_ESPERANDO_ESPECIALIDAD = "ESTADO_ESPERANDO_ESPECIALIDAD"
ESTADO_ESPERANDO_HORARIO = "ESTADO_ESPERANDO_HORARIO"
ESTADO_ESPERANDO_CONFIRMACION = "ESTADO_ESPERANDO_CONFIRMACION"
ESTADO_FIN = "ESTADO_FIN"

# DECLARACION DE FUNCIONES
def leer_csv(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {nombre_archivo}")
        return []

def guardar_csv(nombre_archivo, datos, campos):
    with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(datos)

def registrar_auditoria(dni, estado, mensaje):
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(ARCHIVO_AUDITORIA, "a", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_AUDITORIA)

            if archivo.tell() == 0:
                escritor.writeheader()

            escritor.writerow({
                "fecha_hora": fecha_hora,
                "dni": dni,
                "estado": estado,
                "mensaje": mensaje
            })
    except Exception as error:
        print(f"[ERROR] No se pudo registrar auditoría: {error}")

def cargar_pacientes():
    pacientes = {}
    filas = leer_csv(ARCHIVO_PACIENTES)

    for fila in filas:
        dni = int(fila["dni"])
        pacientes[dni] = {
            "nombre": fila["nombre"],
            "apellido": fila["apellido"],
            "telefono": fila["telefono"]
        }

    return pacientes

def guardar_pacientes(tabla_pacientes):
    filas = []

    for dni, datos in tabla_pacientes.items():
        filas.append({
            "dni": dni,
            "nombre": datos["nombre"],
            "apellido": datos["apellido"],
            "telefono": datos["telefono"]
        })

    guardar_csv(ARCHIVO_PACIENTES, filas, CAMPOS_PACIENTES)

def cargar_especialidades():
    especialidades = {}
    filas = leer_csv(ARCHIVO_ESPECIALIDADES)

    for fila in filas:
        especialidades[int(fila["id_especialidad"])] = fila["nombre"]

    return especialidades

def cargar_turnos():
    turnos = leer_csv(ARCHIVO_TURNOS)

    for turno in turnos:
        turno["id_turno"] = int(turno["id_turno"])
        turno["id_especialidad"] = int(turno["id_especialidad"])

    return turnos

def guardar_turnos(tabla_agenda_turnos):
    guardar_csv(ARCHIVO_TURNOS, tabla_agenda_turnos, CAMPOS_TURNOS)

def cambiar_estado(nuevo_estado, contexto_usuario, mensaje):
    dni = contexto_usuario.get("dni", "")
    registrar_auditoria(dni, nuevo_estado, mensaje)
    return nuevo_estado

def iniciar_auditoria():
    with open(ARCHIVO_AUDITORIA, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(
            archivo,
            fieldnames=CAMPOS_AUDITORIA
        )

        escritor.writeheader()

def simular_bot():
    iniciar_auditoria()
    estado_actual = ESTADO_INICIO
    contexto_usuario = {}

    tabla_pacientes = cargar_pacientes()
    tabla_especialidades = cargar_especialidades()
    tabla_agenda_turnos = cargar_turnos()

    print("\n////////// ASISTENTE VIRTUAL DE TURNOS MÉDICOS INICIADO //////////\n")

    while estado_actual != ESTADO_FIN:

        # --- ESTADO INICIO ---
        if estado_actual == ESTADO_INICIO:
            print("Turni: ¡Hola! Bienvenido al sistema de autogestión de turnos médicos.")
            print("Turni: Soy Turni, el Bot que te ayudará a gestionar tus turnos médicos.")
            print("Turni: Por favor, ingresá tu número de DNI (solo números, sin puntos):")

            estado_actual = cambiar_estado(
                ESTADO_ESPERANDO_DNI,
                contexto_usuario,
                "Inicio de conversación y solicitud de DNI"
            )
        # --- ESTADO ESPERANDO DNI (Validación y Compuerta 1) ---
        elif estado_actual == ESTADO_ESPERANDO_DNI:
            entrada = input("Usuario: ").strip()

            # Camino Infeliz: Entrada no numérica
            if not entrada.isdigit():
                print("-------------------------------------------------------------------------------------------")
                print("Turni: [!] El DNI debe contener solo números y sin puntos. Por favor, ingresalo nuevamente.")

                registrar_auditoria(
                    "",
                    ESTADO_ESPERANDO_DNI,
                    f"DNI inválido ingresado: {entrada}"
                )
                continue

            dni = int(entrada)
            contexto_usuario["dni"] = dni

            print(f"Turni: [Verificando DNI {dni} en Base de Datos...]")
            if dni in tabla_pacientes:
                # Camino SÍ: Paciente Registrado
                paciente = tabla_pacientes[dni]
                print("-------------------------------------------------------------------------------------------")
                print(f"Turni: ¡Bienvenido, me alegra verte de nuevo, {paciente['nombre']} {paciente['apellido']}!")

                estado_actual = cambiar_estado(
                    ESTADO_ESPERANDO_ESPECIALIDAD,
                    contexto_usuario,
                    "Paciente registrado encontrado en la base de datos"
                )
            else:
                # Camino NO: Paciente Nuevo
                print("-------------------------------------------------------------------------------------------")
                print("Turni: No te encontré en nuestro sistema. Vamos a realizar tu registro rápido.")

                estado_actual = cambiar_estado(
                    ESTADO_REGISTRANDO_PACIENTE,
                    contexto_usuario,
                    "Paciente no registrado. Se inicia alta"
                )
        
        # --- ESTADO REGISTRANDO PACIENTE (Camino NO del BPMN) ---
        elif estado_actual == ESTADO_REGISTRANDO_PACIENTE:
            nombre = input("Turni: Ingresá tu Nombre: ").strip()
            apellido = input("Turni: Ingresá tu Apellido: ").strip()
            telefono = input("Turni: Ingresá un número de contacto: ").strip()
            
            # Guardado tabla auxiliar
            tabla_pacientes[contexto_usuario["dni"]] = {
                "nombre": nombre,
                "apellido": apellido,
                "telefono": telefono
            }
            # Guardado persistente en CSV
            guardar_pacientes(tabla_pacientes)

            print("Turni: ¡Registro completado con éxito!")

            estado_actual = cambiar_estado(
                ESTADO_ESPERANDO_ESPECIALIDAD,
                contexto_usuario,
                "Paciente registrado correctamente en pacientes.csv"
            )
        
        # --- ESTADO ESPERANDO ESPECIALIDAD ---
        elif estado_actual == ESTADO_ESPERANDO_ESPECIALIDAD:
            print("-------------------------------------------------------------------------------------------")
            print("Turni: Estas son nuestras especialidades disponibles:")

            for id_esp, nombre_esp in tabla_especialidades.items():
                print(f"       [{id_esp}] {nombre_esp}")

            entrada = input("Turni: Seleccioná el número de la especialidad: ").strip()
            # Camino Infeliz: Opción inválida o fuera de rango
            if not entrada.isdigit() or int(entrada) not in tabla_especialidades:
                print("Turni: [!] Opción no válida. Por favor, seleccioná un número correspondiente a la lista.")

                registrar_auditoria(
                    contexto_usuario.get("dni", ""),
                    ESTADO_ESPERANDO_ESPECIALIDAD,
                    f"Especialidad inválida ingresada: {entrada}"
                )
                continue

            id_seleccionado = int(entrada)
            contexto_usuario["id_especialidad"] = id_seleccionado

            print(f"Turni: Consultando agenda de turnos para {tabla_especialidades[id_seleccionado]}...")
            
            # Mostramos TODOS los turnos de la especialidad (tanto Disponibles como Ocupados)
            turnos_totales = [
                t for t in tabla_agenda_turnos
                if t["id_especialidad"] == id_seleccionado
            ]

            if not turnos_totales:
                print("Turni: [!] En este momento no hay turnos cargados para esta especialidad.")
                print("Turni: Proceso finalizado.")

                estado_actual = cambiar_estado(
                    ESTADO_FIN,
                    contexto_usuario,
                    "No existen turnos cargados para la especialidad seleccionada"
                )
            else:
                turnos_disponibles = [
                    turno for turno in turnos_totales
                    if turno["estado"] == "Disponible"
                ]

                if len(turnos_disponibles) == 0:
                    print("Turni: En este momento todos los turnos para esta especialidad están ocupados.")
                    print("Turni: Registraremos tu solicitud en lista de espera.")

                    estado_actual = cambiar_estado(
                        ESTADO_FIN,
                        contexto_usuario,
                        "Todos los turnos de la especialidad están ocupados. Usuario derivado a lista de espera"
                    )
                else:
                    contexto_usuario["turnos_opciones"] = turnos_totales

                    estado_actual = cambiar_estado(
                        ESTADO_ESPERANDO_HORARIO,
                        contexto_usuario,
                        "Turnos encontrados para la especialidad seleccionada"
                    )

        # --- ESTADO ESPERANDO HORARIO (Con validación de ocupado) ---
        elif estado_actual == ESTADO_ESPERANDO_HORARIO:
            print("-------------------------------------------------------------------------------------------")
            print("Turni: Agenda de turnos para la especialidad seleccionada:")
            opciones = contexto_usuario["turnos_opciones"]
            
            # Mostramos todos, pero aclaramos si está Disponible u Ocupado
            for indice, turno in enumerate(opciones):
                estado_visual = "Disponible" if turno["estado"] == "Disponible" else "OCUPADO"
                print(f"  [{indice + 1}] {turno['fecha_hora']} con el/la {turno['medico']} ({estado_visual})")

            entrada = input("Turni: Seleccioná el número del horario deseado o ingresá 0 para cancelar: ").strip()

            if entrada == "0":
                print("Turni: Operación cancelada por el usuario.")
                estado_actual = cambiar_estado(
                    ESTADO_FIN,
                    contexto_usuario,
                    "El usuario canceló la selección de horario"
                )
                continue
            
            # Camino Infeliz 1: Opción fuera de rango de la lista
            if not entrada.isdigit() or int(entrada) < 1 or int(entrada) > len(opciones):
                print("Turni: [!] Opción no válida. Elija un número de la lista mostrada.")

                registrar_auditoria(
                    contexto_usuario.get("dni", ""),
                    ESTADO_ESPERANDO_HORARIO,
                    f"Horario inválido ingresado: {entrada}"
                )
                continue

            turno_elegido = opciones[int(entrada) - 1]
            
            # Camino Infeliz 2: El usuario elige un turno que figura como OCUPADO
            if turno_elegido["estado"] == "Ocupado":
                print(f"Turni: [!] El turno del {turno_elegido['fecha_hora']} ya no se encuentra disponible.")
                print("Turni: Alguien reservó este cupo recientemente. Por favor, seleccioná otra opción que esté libre.")

                registrar_auditoria(
                    contexto_usuario.get("dni", ""),
                    ESTADO_ESPERANDO_HORARIO,
                    f"Intento de reservar turno ocupado ID {turno_elegido['id_turno']}"
                )
                # Al no cambiar el estado_actual, el bucle se repite y le vuelve a mostrar la lista para que elija bien.
                continue

            # Si pasa la validación (está Disponible), avanza al camino feliz
            contexto_usuario["turno_elegido"] = turno_elegido

            estado_actual = cambiar_estado(
                ESTADO_ESPERANDO_CONFIRMACION,
                contexto_usuario,
                f"Turno seleccionado ID {turno_elegido['id_turno']}"
            )
        
        # --- ESTADO ESPERANDO CONFIRMACIÓN (Compuerta Final) ---
        elif estado_actual == ESTADO_ESPERANDO_CONFIRMACION:
            t = contexto_usuario["turno_elegido"]
            esp_nombre = tabla_especialidades[contexto_usuario["id_especialidad"]]

            print("-------------------------------------------------------------------------------------------")
            print("Turni: --- RESUMEN DE TU RESERVA ---")
            print(f"Especialidad: {esp_nombre}")
            print(f"Médico: {t['medico']}")
            print(f"Fecha y Hora: {t['fecha_hora']}")

            respuesta = input("Turni: ¿Confirmás la reserva de este turno? (SI/NO): ").strip().upper()

            if respuesta == "SI":
                # Camino SÍ: Éxito
                # Cambiar el estado del turno en la BD
                for turno_bd in tabla_agenda_turnos:
                    if turno_bd["id_turno"] == t["id_turno"]:
                        turno_bd["estado"] = "Ocupado"
                        turno_bd["dni_paciente"] = str(contexto_usuario["dni"])
                # Guardamos en CSV
                guardar_turnos(tabla_agenda_turnos)
                print("Turni: ¡Turno asignado exitosamente!")
                print(f"Turni: Se generó tu comprobante nro #{t['id_turno']}. ¡Te esperamos!")

                estado_actual = cambiar_estado(
                    ESTADO_FIN,
                    contexto_usuario,
                    f"Turno asignado correctamente. ID turno {t['id_turno']}"
                )

            elif respuesta == "NO":
                # Camino NO: Cancelación
                print("Turni: El turno no ha sido reservado.")
                print("Turni: Proceso finalizado - Turno cancelado por el usuario.")

                estado_actual = cambiar_estado(
                    ESTADO_FIN,
                    contexto_usuario,
                    "El usuario no confirmó la reserva"
                )

            else:
                # Camino Infeliz: Respuesta ambigua
                print("Turni: [!] No entendí tu respuesta. Por favor, respondé escribiendo SI o NO.")

                registrar_auditoria(
                    contexto_usuario.get("dni", ""),
                    ESTADO_ESPERANDO_CONFIRMACION,
                    f"Respuesta inválida en confirmación: {respuesta}"
                )
                continue

    print("\n////////// ASISTENTE VIRTUAL DE TURNOS MÉDICOS FINALIZADO //////////\n")

# Ejecución de la simulación
if __name__ == "__main__":
    simular_bot()
    
