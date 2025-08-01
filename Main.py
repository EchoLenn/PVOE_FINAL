import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import database_manager
from vista_inicio import VistaInicio
from vista_login import VistaLogin
from vista_registro_alumno import VistaRegistroAlumno
from vista_calificaciones import VistaCalificaciones
from vista_kardex import VistaKardex
from vista_inscripcion import VistaInscripcion
from vista_historial_inscripciones import VistaHistorialInscripciones
from vista_grupos import VistaGrupos
from vista_horario import VistaHorario

try:
    with open("estilos.qss", "x") as f:
        f.write("/* Archivo de Estilos QSS para UAMITOS High School */")
except FileExistsError:
    pass

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión UAMITOS High School")
        self.setGeometry(100, 100, 800, 600)

        menu = self.menuBar()
        self.menu_archivo = menu.addMenu("&Archivo")
        self.menu_alumnos = menu.addMenu("&Alumnos")
        self.menu_inscripciones = menu.addMenu("&Inscripciones")
        self.menu_admin = menu.addMenu("Administración")
        self.menu_ayuda = menu.addMenu("A&yuda")

        self.accion_ir_inicio = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon), "Ir a Inicio", self)
        accion_salir = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton), "Salir", self)
        self.accion_registrar_alumno = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon), "Registrar Nuevo Alumno", self)
        self.accion_gestionar_calificaciones = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView), "Gestionar Calificaciones", self)
        self.accion_consultar_kardex = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView), "Consultar Kardex", self)
        self.accion_solicitar_inscripcion = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogApplyButton), "Solicitar Inscripción", self)
        self.accion_historial_inscripciones = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload), "Consultar Historial", self)
        self.accion_generar_grupo = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogNewFolder), "Generar Grupo", self)
        self.accion_consultar_horario = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView), "Consultar Horario", self)
        accion_acerca_de = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation), "Acerca de...", self)

        self.menu_archivo.addAction(self.accion_ir_inicio)
        self.menu_archivo.addSeparator() 
        self.menu_archivo.addAction(accion_salir)
        self.menu_alumnos.addAction(self.accion_registrar_alumno)
        self.menu_alumnos.addAction(self.accion_gestionar_calificaciones)
        self.menu_alumnos.addAction(self.accion_consultar_kardex)
        self.menu_inscripciones.addAction(self.accion_solicitar_inscripcion)
        self.menu_inscripciones.addAction(self.accion_historial_inscripciones)
        self.menu_admin.addAction(self.accion_generar_grupo)
        self.menu_admin.addAction(self.accion_consultar_horario)
        self.menu_ayuda.addAction(accion_acerca_de)

        self.toolbar = self.addToolBar("Barra de Herramientas Principal")
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.addAction(self.accion_ir_inicio)
        self.toolbar.addAction(self.accion_registrar_alumno)
        self.toolbar.addAction(self.accion_gestionar_calificaciones)
        self.toolbar.addAction(self.accion_consultar_kardex)
        self.toolbar.addAction(self.accion_solicitar_inscripcion)
        self.toolbar.addAction(self.accion_historial_inscripciones)
        self.toolbar.addAction(self.accion_generar_grupo)
        self.toolbar.addAction(self.accion_consultar_horario)
        self.toolbar.addSeparator()
        self.toolbar.addAction(accion_salir)

        self.vistas = QStackedWidget()
        self.setCentralWidget(self.vistas)
        
        self.vista_login = VistaLogin()
        self.vista_inicio = VistaInicio()
        self.vista_registro = VistaRegistroAlumno()
        self.vista_calificaciones = VistaCalificaciones()
        self.vista_kardex = VistaKardex()
        self.vista_inscripcion = VistaInscripcion()
        self.vista_historial_ins = VistaHistorialInscripciones()
        self.vista_grupos = VistaGrupos()
        self.vista_horario = VistaHorario()

        self.vistas.addWidget(self.vista_login)
        self.vistas.addWidget(self.vista_inicio)
        self.vistas.addWidget(self.vista_registro)
        self.vistas.addWidget(self.vista_calificaciones)
        self.vistas.addWidget(self.vista_kardex)
        self.vistas.addWidget(self.vista_inscripcion)
        self.vistas.addWidget(self.vista_historial_ins)
        self.vistas.addWidget(self.vista_grupos)
        self.vistas.addWidget(self.vista_horario)

        self.statusBar().showMessage("Por favor, inicie sesión para continuar.")

        accion_salir.triggered.connect(self.close)
        accion_acerca_de.triggered.connect(self.mostrar_acerca_de)
        self.accion_ir_inicio.triggered.connect(self.mostrar_vista_inicio)
        self.accion_registrar_alumno.triggered.connect(self.mostrar_vista_registro)
        self.accion_gestionar_calificaciones.triggered.connect(self.mostrar_vista_calificaciones)
        self.accion_consultar_kardex.triggered.connect(self.mostrar_vista_kardex)
        self.accion_solicitar_inscripcion.triggered.connect(self.mostrar_vista_inscripcion)
        self.accion_historial_inscripciones.triggered.connect(self.mostrar_vista_historial)
        self.accion_generar_grupo.triggered.connect(self.mostrar_vista_grupos)
        self.accion_consultar_horario.triggered.connect(self.mostrar_vista_horario)
        
        self.vista_login.login_exitoso.connect(self.desbloquear_aplicacion)
        
        self.vistas.setCurrentWidget(self.vista_login)
        self.menu_alumnos.setEnabled(False)
        self.menu_inscripciones.setEnabled(False)
        self.menu_admin.setEnabled(False)
        self.toolbar.setVisible(False)
        self.accion_ir_inicio.setEnabled(False)

    @Slot()
    def desbloquear_aplicacion(self):
        self.menu_alumnos.setEnabled(True)
        self.menu_inscripciones.setEnabled(True)
        self.menu_admin.setEnabled(True)
        self.toolbar.setVisible(True)
        self.accion_ir_inicio.setEnabled(True)
        self.statusBar().showMessage("Sesión iniciada correctamente.")
        self.mostrar_vista_inicio()
    
    @Slot()
    def mostrar_vista_inicio(self):
        self.vistas.setCurrentWidget(self.vista_inicio)
    @Slot()
    def mostrar_vista_registro(self):
        self.vistas.setCurrentWidget(self.vista_registro)
    @Slot()
    def mostrar_vista_calificaciones(self):
        self.vistas.setCurrentWidget(self.vista_calificaciones)
    @Slot()
    def mostrar_vista_kardex(self):
        self.vistas.setCurrentWidget(self.vista_kardex)
    @Slot()
    def mostrar_vista_inscripcion(self):
        self.vistas.setCurrentWidget(self.vista_inscripcion)
    @Slot()
    def mostrar_vista_historial(self):
        self.vistas.setCurrentWidget(self.vista_historial_ins)
        self.vista_historial_ins.cargar_historial()
    @Slot()
    def mostrar_vista_grupos(self):
        self.vistas.setCurrentWidget(self.vista_grupos)
    @Slot()
    def mostrar_vista_horario(self):
        self.vistas.setCurrentWidget(self.vista_horario)
        self.vista_horario.refrescar_grupos()

    @Slot()
    def mostrar_acerca_de(self):
        QMessageBox.about(
            self,
            "Acerca de UAMITOS High School",
            "<p><b>Sistema de Gestión de Calificaciones e Inscripción</b></p>"
            "<p>Desarrollado para el proyecto final de Programación Visual Orientada a Eventos.</p>"
            "<p><b>Cliente:</b> Secundaria UAMITOS</p>"
            "<p><b>Equipo de Desarrollo:</b><br>"
            "Echo Lengrit Muñoz Sanchez</p>"
        )

if __name__ == "__main__":
    database_manager.init_db()
    
    app = QApplication(sys.argv)
    
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        qss_file = os.path.join(script_dir, "estilos.qss")

        if os.path.exists(qss_file):
            with open(qss_file, "r", encoding="utf-8") as f:
                stylesheet = f.read()
                app.setStyleSheet(stylesheet)
                print("Estilos QSS cargados correctamente.")
        else:
            error_msg = f"Error: No se encontró el archivo 'estilos.qss' en la ruta esperada:\n{qss_file}"
            print(error_msg)
            QMessageBox.warning(None, "Error de Carga", error_msg)

    except Exception as e:
        print(f"Ocurrió un error inesperado al cargar 'estilos.qss': {e}")
        QMessageBox.critical(None, "Error Crítico", f"Ocurrió un error al cargar los estilos:\n{e}")

    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())