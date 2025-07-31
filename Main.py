import sys
import os
from PySide6.QtCore import Slot, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QMessageBox, QStackedWidget
)

from vista_login import VistaLogin
from vista_registro_alumno import VistaRegistroAlumno
from vista_calificaciones import VistaCalificaciones
from vista_kardex import VistaKardex

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión UAMITOS High School")
        self.setGeometry(100, 100, 800, 600)

        menu = self.menuBar()
        self.menu_archivo = menu.addMenu("&Archivo")
        self.menu_alumnos = menu.addMenu("&Alumnos")
        self.menu_ayuda = menu.addMenu("A&yuda")

        self.accion_ir_inicio = QAction(QIcon("iconos/home.png"), "Ir a Inicio", self)
        accion_salir = QAction(QIcon("iconos/log-out.png"), "Salir", self)
        self.accion_registrar_alumno = QAction(QIcon("iconos/user-plus.png"), "Registrar Nuevo Alumno", self)
        self.accion_gestionar_calificaciones = QAction(QIcon("iconos/edit.png"), "Gestionar Calificaciones", self)
        self.accion_consultar_kardex = QAction(QIcon("iconos/file-text.png"), "Consultar Kardex", self)
        accion_acerca_de = QAction("Acerca de...", self)

        self.menu_archivo.addAction(self.accion_ir_inicio)
        self.menu_archivo.addSeparator() 
        self.menu_archivo.addAction(accion_salir)
        self.menu_alumnos.addAction(self.accion_registrar_alumno)
        self.menu_alumnos.addAction(self.accion_gestionar_calificaciones)
        self.menu_alumnos.addAction(self.accion_consultar_kardex)
        self.menu_ayuda.addAction(accion_acerca_de)

        self.toolbar = self.addToolBar("Barra de Herramientas Principal")
        self.toolbar.setIconSize(QSize(24, 24))
        self.toolbar.addAction(self.accion_ir_inicio)
        self.toolbar.addAction(self.accion_registrar_alumno)
        self.toolbar.addAction(self.accion_gestionar_calificaciones)
        self.toolbar.addAction(self.accion_consultar_kardex)
        self.toolbar.addAction(accion_salir)

        self.vistas = QStackedWidget()
        self.setCentralWidget(self.vistas)
        
        self.vista_login = VistaLogin()
        self.vista_inicio = QWidget()
        self.vista_inicio.setLayout(QVBoxLayout())
        self.vista_inicio.layout().addWidget(QLabel("<h1>Pantalla de Inicio</h1><p>Seleccione una opción del menú o la barra de herramientas.</p>"))
        self.vista_registro = VistaRegistroAlumno()
        self.vista_calificaciones = VistaCalificaciones()
        self.vista_kardex = VistaKardex()

        self.vistas.addWidget(self.vista_login)
        self.vistas.addWidget(self.vista_inicio)
        self.vistas.addWidget(self.vista_registro)
        self.vistas.addWidget(self.vista_calificaciones)
        self.vistas.addWidget(self.vista_kardex)

        self.statusBar().showMessage("Por favor, inicie sesión para continuar.")

        accion_salir.triggered.connect(self.close)
        accion_acerca_de.triggered.connect(self.mostrar_acerca_de)
        self.accion_ir_inicio.triggered.connect(self.mostrar_vista_inicio)
        self.accion_registrar_alumno.triggered.connect(self.mostrar_vista_registro)
        self.accion_gestionar_calificaciones.triggered.connect(self.mostrar_vista_calificaciones)
        self.accion_consultar_kardex.triggered.connect(self.mostrar_vista_kardex)
        
        self.vista_login.login_exitoso.connect(self.desbloquear_aplicacion)
        
        self.vistas.setCurrentWidget(self.vista_login)
        self.menu_alumnos.setEnabled(False)
        self.toolbar.setVisible(False)
        self.accion_ir_inicio.setEnabled(False)

    @Slot()
    def desbloquear_aplicacion(self):
        self.menu_alumnos.setEnabled(True)
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
    def mostrar_acerca_de(self):
        QMessageBox.about(
            self,
            "Acerca de UAMITOS High School",
            "<p><b>Sistema de Gestión de Calificaciones e Inscripción</b></p>"
            "<p>Desarrollado para el proyecto final de Programación Visual Orientada a Eventos.</p>"
            "<p><b>Cliente:</b> Secundaria UAMITOS</p>"
            "<p><b>Equipo de Desarrollo:</b><br>"
            "[Aquí irían los nombres de los integrantes]</p>"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        qss_file = os.path.join(script_dir, "estilos.qss")

        if os.path.exists(qss_file):
            with open(qss_file, "r") as f:
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