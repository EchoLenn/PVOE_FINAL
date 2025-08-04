# 📘 Sistema de Gestión UAMITOS

Aplicación de escritorio diseñada y programada en Python para la materia: *Programación Visual Orientada a Eventos*. Este sistema integral permite la gestión de alumnos, calificaciones, inscripciones y usuarios para la secundaria "UAMITOS High School".

---

**Entorno de desarrollo**: `Visual Studio Code`

**Lenguaje de programación**: `Python`

**Dependencias utilizadas**: `PySide6`

---

## ✅ Funcionalidades Implementadas

* **Sistema de Autenticación y Roles**
    * Login de usuarios validado contra la base de datos.
    * Creación de un usuario `admin` por defecto (`1234`) en el primer arranque.
    * Sistema de roles que restringe el acceso a funciones administrativas.

* **Módulo de Alumnos**
    * Formulario para registrar nuevos alumnos con datos personales y de tutor.
    * Asignación automática de un ID único a cada alumno al ser registrado.
    * Almacenamiento seguro de la información en una base de datos SQLite.

* **Módulo de Calificaciones**
    * Búsqueda de alumnos por ID para gestionar sus calificaciones.
    * Tabla para registrar y modificar las calificaciones de las materias.
    * Consulta de Kardex con el historial completo de calificaciones de un alumno.
    * Cálculo y visualización del promedio general del alumno.

* **Módulo de Inscripciones**
    * Formulario para generar nuevas inscripciones, asociando un alumno a un grupo.
    * Generación de un recibo de inscripción con los detalles de la transacción.
    * Pantalla para visualizar el historial completo de todas las inscripciones realizadas en el sistema.

* **Módulo de Administración (Solo para Admins)**
    * Creación de nuevos grupos escolares, asignando un profesor y materias.
    * Consulta de la lista de alumnos inscritos en cada grupo.
    * Gestión de horarios por grupo, permitiendo asignar materias a bloques de hora específicos.
    * Panel de gestión de usuarios para crear nuevos perfiles (profesor, asistente) con autorización del administrador.

* **Interfaz y Experiencia de Usuario**
    * Interfaz gráfica moderna y consistente, diseñada con un archivo `estilos.qss` externo.
    * Barra de menú y barra de herramientas con iconos del sistema para un acceso rápido a todas las funciones.
    * Manejo robusto de errores y validaciones con diálogos informativos para el usuario.

---

## 📂 Estructura del Proyecto


```css
PVOE_FINAL/
├── Main.py                             → Orquestador principal de la aplicación. Construye la ventana y gestiona las vistas.
├── database_manager.py                 → Gestor central que maneja toda la comunicación con la base de datos SQLite.
├── estilos.qss                         → Archivo de estilos (similar a CSS) que define la apariencia de la aplicación.
├── helpers.py                          → Contiene funciones de ayuda, como la que permite encontrar recursos para el ejecutable.
├── vista_calificaciones.py             → Define la interfaz y lógica para registrar y modificar calificaciones.
├── vista_consulta_grupos.py            → Define la interfaz para ver la lista de alumnos inscritos en un grupo.
├── vista_gestion_usuarios.py           → Define el panel de administración para crear nuevos usuarios.
├── vista_grupos.py                     → Define la interfaz y lógica para la creación de nuevos grupos escolares.
├── vista_historial_inscripciones.py    → Define la tabla para visualizar el historial de todas las inscripciones.
├── vista_horario.py                    → Define la interfaz para consultar y gestionar el horario de un grupo.
├── vista_inicio.py                     → Define la pantalla de bienvenida que aparece después del login.
├── vista_inscripcion.py                → Define el formulario para generar una nueva inscripción de un alumno.
├── vista_kardex.py                     → Define la interfaz para consultar el historial de calificaciones y promedio.
├── vista_login.py                      → Define la pantalla de inicio de sesión y la lógica de autenticación.
└── vista_registro_alumno.py            → Define el formulario para registrar nuevos alumnos y sus tutores.
```
---

## 🚀 Cómo Empezar

Sigue estos pasos para poner en marcha el proyecto en tu propio entorno.

### **Prerrequisitos**

Asegúrate de tener instalado Python 3 en tu sistema. Luego, instala la única dependencia necesaria:

```bash
pip install PySide6

```

## **Ejecución**

1. Clona o descarga este repositorio en tu máquina local.

2. Navega hasta la carpeta del proyecto en tu terminal

3. Ejecuta el archivo principal:

```bash
python Main.py

```

La primera vez que ejecutes la aplicación, se creará automáticamente el archivo de base de datos `escuela.db` y un usuario administrador por defecto.


## **Credenciales de Administrador**

* Usuario: `admin`

* Contraseña: `1234`

---


