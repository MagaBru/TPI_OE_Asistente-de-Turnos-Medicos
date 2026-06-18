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

El sistema simula un flujo conversacional inteligente que interactúa en tiempo real con una capa de persistencia de datos relacionales simulada en memoria y toma decisiones lógicas basadas en un modelo estandarizado BPMN, diseñado en Camunda 8.9.

---

## Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Modelado de Procesos:** BPMN 2.0, Camunda Web Modeler
* **Control de Versiones:** Git & GitHub

---

## Esqueleto de Navegación / Máquina de Estados Finitos
El chatbot está construido bajo una arquitectura de Máquina de Estados Finitos (FSM) para mantener el contexto de la conversación con el paciente:

* `ESTADO_INICIO`: Saludo inicial y limpieza de variables.
* `ESTADO_ESPERANDO_DNI`: Validación del documento en la tabla de Pacientes.
* `ESTADO_REGISTRANDO_PACIENTE`: Captura de datos para nuevos usuarios (Camino Infeliz / Excepción).
* `ESTADO_ESPERANDO_ESPECIALIDAD`: Despliegue de menú dinámico de ramas médicas.
* `ESTADO_ESPERANDO_HORARIO`: Consulta de disponibilidad en la Agenda Médica.
* `ESTADO_ESPERANDO_CONFIRMACION`: Resumen de reserva y confirmación final (SI/NO).

---

## Persistencia Simulada / Modelo de Datos
El script manipula internamente tres estructuras de datos clave:
1. **`tabla_pacientes`**: Almacena `dni` (Clave Primaria), `nombre`, `apellido` y `telefono`.
2. **`tabla_especialidades`**: Almacena `id_especialidad` y `nombre_esp`.
3. **`tabla_agenda_turnos`**: Gestiona la disponibilidad de cupos (`id_turno`, `medico`, `fecha_hora`, `estado`).