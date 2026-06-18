import csv

ARCHIVO_PACIENTES = "pacientes.csv"
ARCHIVO_ESPECIALIDADES = "especialidades.csv"
ARCHIVO_MEDICOS = "medicos.csv"
ARCHIVO_TURNOS = "turnos.csv"

CAMPOS_PACIENTES = ["dni", "nombre", "telefono"]
CAMPOS_TURNOS = ["id_turno", "dni_paciente", "id_medico", "id_especialidad", "fecha", "hora", "estado"]


def leer_csv(nombre_archivo):
    try:
        with open(nombre_archivo, "r", encoding="utf-8", newline="") as archivo:
            return list(csv.DictReader(archivo))
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {nombre_archivo}.")
        return []


def guardar_csv(nombre_archivo, datos, campos):
    try:
        with open(nombre_archivo, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(datos)
    except Exception as error:
        print(f"Error al guardar el archivo {nombre_archivo}: {error}")


def validar_dni(dni):
    return dni.isdigit() and len(dni) >= 7


def buscar_paciente(dni):
    pacientes = leer_csv(ARCHIVO_PACIENTES)

    for paciente in pacientes:
        if paciente["dni"] == dni:
            return paciente

    return None


def registrar_paciente(dni):
    print("\nPaciente no registrado. Se iniciará el alta.")

    nombre = input("Ingrese nombre y apellido: ").strip()
    telefono = input("Ingrese teléfono: ").strip()

    while nombre == "":
        nombre = input("El nombre no puede estar vacío. Ingrese nombre y apellido: ").strip()

    while telefono == "":
        telefono = input("El teléfono no puede estar vacío. Ingrese teléfono: ").strip()

    pacientes = leer_csv(ARCHIVO_PACIENTES)

    nuevo_paciente = {
        "dni": dni,
        "nombre": nombre,
        "telefono": telefono
    }

    pacientes.append(nuevo_paciente)
    guardar_csv(ARCHIVO_PACIENTES, pacientes, CAMPOS_PACIENTES)

    print("\nPaciente registrado correctamente.")
    return nuevo_paciente


def identificar_paciente():
    #print("\nEstado actual: SOLICITAR_DNI")

    while True:
        dni = input("Ingrese su DNI: ").strip()

        #print("Estado actual: VALIDAR_DNI")

        if validar_dni(dni):
            #print("Estado actual: VERIFICAR_PACIENTE")
            paciente = buscar_paciente(dni)

            if paciente:
                print(f"\nBienvenido/a, {paciente['nombre']}.")
                return paciente
            else:
                return registrar_paciente(dni)

        print("DNI inválido. Debe ingresar solo números y al menos 7 dígitos.")


def obtener_especialidad_por_id(id_especialidad):
    especialidades = leer_csv(ARCHIVO_ESPECIALIDADES)

    for especialidad in especialidades:
        if especialidad["id_especialidad"] == id_especialidad:
            return especialidad["nombre"]

    return "Especialidad no encontrada"


def obtener_medico_por_id(id_medico):
    medicos = leer_csv(ARCHIVO_MEDICOS)

    for medico in medicos:
        if medico["id_medico"] == id_medico:
            return medico["nombre"]

    return "Médico no encontrado"


def mostrar_especialidades():
    especialidades = leer_csv(ARCHIVO_ESPECIALIDADES)

    print("\nEspecialidades disponibles:")

    for especialidad in especialidades:
        print(f"{especialidad['id_especialidad']}. {especialidad['nombre']}")

    return especialidades


def solicitar_turno(paciente):
    #print("\nEstado actual: SOLICITAR_TURNO")

    especialidades = mostrar_especialidades()
    ids_validos = [especialidad["id_especialidad"] for especialidad in especialidades]

    while True:
        id_especialidad = input("\nSeleccione una especialidad: ").strip()

        #print("Estado actual: VALIDAR_ESPECIALIDAD")

        if id_especialidad in ids_validos:
            break

        print("\nERROR: La especialidad seleccionada no existe.")
        print("\nDebe ingresar uno de los siguientes números:")

        for especialidad in especialidades:
            print(f"{especialidad['id_especialidad']}. {especialidad['nombre']}")

    turnos = leer_csv(ARCHIVO_TURNOS)

    #print("Estado actual: CONSULTAR_DISPONIBILIDAD")

    disponibles = []

    for turno in turnos:
        if turno["id_especialidad"] == id_especialidad and turno["estado"] == "disponible":
            disponibles.append(turno)

    if not disponibles:
        print("\nNo hay turnos disponibles para la especialidad seleccionada.")
        #print("Estado actual: FIN_SIN_RESERVA")
        return

    print("\nTurnos disponibles:")

    for turno in disponibles:
        medico = obtener_medico_por_id(turno["id_medico"])
        print(f"{turno['id_turno']}. {medico} - {turno['fecha']} - {turno['hora']}")

    id_turno = input("\nSeleccione el ID del turno deseado o ingrese 0 para cancelar: ").strip()

    if id_turno == "0":
        print("Operación cancelada por el paciente.")
        #print("Estado actual: FIN_SIN_RESERVA")
        return

    turno_elegido = None

    for turno in disponibles:
        if turno["id_turno"] == id_turno:
            turno_elegido = turno

    if turno_elegido is None:
        print("Turno inválido. Operación cancelada.")
        #print("Estado actual: FIN_SIN_RESERVA")
        return

    #print("Estado actual: CONFIRMAR_RESERVA")
    confirmacion = input("¿Confirma la reserva? (S/N): ").strip().upper()

    if confirmacion != "S":
        print("Reserva cancelada por el paciente.")
        #print("Estado actual: FIN_SIN_RESERVA")
        return

    for turno in turnos:
        if turno["id_turno"] == id_turno:
            turno["dni_paciente"] = paciente["dni"]
            turno["estado"] = "reservado"

    guardar_csv(ARCHIVO_TURNOS, turnos, CAMPOS_TURNOS)

    #print("Estado actual: REGISTRAR_TURNO")

    especialidad = obtener_especialidad_por_id(turno_elegido["id_especialidad"])
    medico = obtener_medico_por_id(turno_elegido["id_medico"])

    print("\nTurno reservado correctamente.\n")
    print(f"Paciente: {paciente['nombre']}")
    print(f"Especialidad: {especialidad}")
    print(f"Médico: {medico}")
    print(f"Fecha: {turno_elegido['fecha']}")
    print(f"Hora: {turno_elegido['hora']}")
    #print("Estado actual: FIN_CON_RESERVA")


def consultar_turnos(paciente):
    turnos = leer_csv(ARCHIVO_TURNOS)

    turnos_paciente = []

    for turno in turnos:
        if turno["dni_paciente"] == paciente["dni"] and turno["estado"] == "reservado":
            turnos_paciente.append(turno)

    if not turnos_paciente:
        print("\nNo posee turnos reservados.")
        return

    print("\nTurnos reservados:")

    for turno in turnos_paciente:
        especialidad = obtener_especialidad_por_id(turno["id_especialidad"])
        medico = obtener_medico_por_id(turno["id_medico"])
        print(f"ID {turno['id_turno']} - {especialidad} - {medico} - {turno['fecha']} - {turno['hora']}")


def cancelar_turno(paciente):
    turnos = leer_csv(ARCHIVO_TURNOS)

    turnos_paciente = []

    for turno in turnos:
        if turno["dni_paciente"] == paciente["dni"] and turno["estado"] == "reservado":
            turnos_paciente.append(turno)

    if not turnos_paciente:
        print("\nNo posee turnos activos para cancelar.")
        return

    consultar_turnos(paciente)

    id_turno = input("\nIngrese el ID del turno a cancelar: ").strip()
    encontrado = False

    for turno in turnos:
        if turno["id_turno"] == id_turno and turno["dni_paciente"] == paciente["dni"]:
            turno["dni_paciente"] = ""
            turno["estado"] = "disponible"
            encontrado = True

    if encontrado:
        guardar_csv(ARCHIVO_TURNOS, turnos, CAMPOS_TURNOS)
        print("Turno cancelado correctamente.")
    else:
        print("No se encontró un turno válido con ese ID.")


def reprogramar_turno(paciente):
    turnos = leer_csv(ARCHIVO_TURNOS)

    turnos_paciente = []

    for turno in turnos:
        if turno["dni_paciente"] == paciente["dni"] and turno["estado"] == "reservado":
            turnos_paciente.append(turno)

    if not turnos_paciente:
        print("\nNo posee turnos activos para reprogramar.")
        return

    consultar_turnos(paciente)

    id_turno_actual = input("\nIngrese el ID del turno que desea reprogramar: ").strip()

    turno_actual = None

    for turno in turnos:
        if turno["id_turno"] == id_turno_actual and turno["dni_paciente"] == paciente["dni"]:
            turno_actual = turno

    if turno_actual is None:
        print("No se encontró un turno válido con ese ID.")
        return

    id_especialidad = turno_actual["id_especialidad"]

    disponibles = []

    for turno in turnos:
        if turno["id_especialidad"] == id_especialidad and turno["estado"] == "disponible":
            disponibles.append(turno)

    if not disponibles:
        print("No hay turnos disponibles para reprogramar.")
        return

    print("\nHorarios disponibles para reprogramar:")

    for turno in disponibles:
        medico = obtener_medico_por_id(turno["id_medico"])
        print(f"{turno['id_turno']}. {medico} - {turno['fecha']} - {turno['hora']}")

    id_nuevo_turno = input("\nSeleccione el nuevo ID de turno: ").strip()

    nuevo_turno = None

    for turno in disponibles:
        if turno["id_turno"] == id_nuevo_turno:
            nuevo_turno = turno

    if nuevo_turno is None:
        print("Turno inválido. Operación cancelada.")
        return

    turno_actual["dni_paciente"] = ""
    turno_actual["estado"] = "disponible"

    nuevo_turno["dni_paciente"] = paciente["dni"]
    nuevo_turno["estado"] = "reservado"

    guardar_csv(ARCHIVO_TURNOS, turnos, CAMPOS_TURNOS)

    print("Turno reprogramado correctamente.")


def mostrar_menu():
    print("\n===== CENTRO MÉDICO =====")
    print("1. Solicitar turno")
    print("2. Consultar turno")
    print("3. Cancelar turno")
    print("4. Reprogramar turno")
    print("5. Salir")


def main():
    print("\nBienvenido/a al Asistente Virtual de Turnos Médicos.\n")

    paciente = identificar_paciente()

    while True:
        #print("\nEstado actual: MENU_PRINCIPAL")
        mostrar_menu()

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            solicitar_turno(paciente)
        elif opcion == "2":
            consultar_turnos(paciente)
        elif opcion == "3":
            cancelar_turno(paciente)
        elif opcion == "4":
            reprogramar_turno(paciente)
        elif opcion == "5":
            print("\nGracias por utilizar el Asistente Virtual.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


main()

