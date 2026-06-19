# TPI_OE_Asistente-de-Turnos-Medicos
# Trabajo Práctico Integrador: Asistente Virtual para Asignación de Turnos Médicos
# Materia: Organización Empresarial | 1° Cuatrimestre 2026
 
---

## Integrantes del Grupo
* **Leila Magalí Bruno** - Comisión: 14
* **Sofía Antonella Gai Rejan** - Comisión: 14

---

## Descripción del Proyecto
Este proyecto consiste en el diseño y prototipado de un Chatbot Automatizado orientado a la gestión y reserva de turnos en instituciones de salud de mediana complejidad. El objetivo principal es descentralizar las tareas repetitivas del personal administrativo, eliminar los cuellos de botella telefónicos y ofrecer una solución asincrónica 24/7 para los pacientes, mediante la plataforma WhatsApp.

El sistema simula un flujo conversacional inteligente que interactúa en tiempo real con una capa de persistencia de datos relacionales y toma decisiones lógicas basadas en un modelo estandarizado BPMN, diseñado en Camunda 8.9.

---

## Funcionalidades
* Validación de DNI del paciente.
* Registro automático de pacientes no existentes.
* Oferta de especialidades médicas.
* Visualización de turnos disponibles y ocupados.
* Reserva de turnos médicos.
* Registro de estados en archivo de auditoría.

---

## Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Modelado de Procesos:** BPMN 2.0, Camunda Web Modeler
* **Control de Versiones:** Git & GitHub

---

## Estructura del proyecto
gestor_turnos_medicos/

├── main.py

├── pacientes.csv

├── especialidades.csv

├── agenda_turnos.csv

├── auditoria.csv

└── README.md

---

## Archivos utilizados
* **pacientes.csv**
Contiene los datos de los pacientes registrados.
Campos:
dni,nombre,apellido,telefono

* **especialidades.csv**
Contiene las especialidades disponibles.
Campos:
id_especialidad,nombre

* **agenda_turnos.csv**
Contiene la agenda de turnos médicos.
Campos:
id_turno,id_especialidad,medico,fecha_hora,estado,dni_paciente

* **auditoria.csv**
Se genera o sobrescribe automáticamente al iniciar una nueva ejecución del programa. Registra los estados recorridos por el chatbot y permite auditar el flujo realizado.
Campos:
fecha_hora,dni,estado,mensaje

---
## Máquina de Estados Finitos
El chatbot está construido bajo una arquitectura de Máquina de Estados Finitos (FSM) para mantener el contexto de la conversación con el paciente:

* `ESTADO_INICIO`: Saludo inicial y limpieza de variables.
* `ESTADO_ESPERANDO_DNI`: Validación del documento en la tabla de Pacientes.
* `ESTADO_REGISTRANDO_PACIENTE`: Captura de datos para nuevos usuarios (Camino Infeliz / Excepción).
* `ESTADO_ESPERANDO_ESPECIALIDAD`: Despliegue de menú dinámico de ramas médicas.
* `ESTADO_ESPERANDO_HORARIO`: Consulta de disponibilidad en la Agenda Médica.
* `ESTADO_ESPERANDO_CONFIRMACION`: Resumen de reserva y confirmación final (SI/NO).

---
## Cómo ejecutar el proyecto
1- Descargar o clonar el repositorio.

2- Verificar que los siguientes archivos se encuentren en la misma carpeta:
   
   * main.py
   * pacientes.csv
   * especialidades.csv
   * agenda_turnos.csv

3- Abrir una terminal en la carpeta del proyecto.

4- Ejecutar el programa con el siguiente comando:
   python main.py

5- En algunos sistemas puede ser necesario usar:
   python3 main.py

## Auditoria
Cada vez que se ejecuta el programa, el archivo auditoria.csv se reinicia automáticamente. 
Durante la ejecución se registran los estados recorridos por el chatbot, junto con el DNI del usuario y un mensaje descriptivo.
Esto permite revisar el recorrido del proceso, detectar errores de entrada y analizar en qué punto finalizó la interacción.
