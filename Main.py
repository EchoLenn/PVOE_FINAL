import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from vista_registro_alumno import VistaRegistroAlumno
from vista_calificaciones import VistaCalificaciones
from vista_kardex import VistaKardex

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
        menu_archivo = menu.addMenu("&Archivo")
        menu_alumnos = menu.addMenu("&Alumnos")
        menu_ayuda = menu.addMenu("A&yuda")

        accion_ir_inicio = QAction("Ir a Inicio", self)
        accion_salir = QAction("Salir", self)
        accion_registrar_alumno = QAction("Registrar Nuevo Alumno", self)
        accion_gestionar_calificaciones = QAction("Gestionar Calificaciones", self)
        accion_consultar_kardex = QAction("Consultar Kardex", self)
        accion_acerca_de = QAction("Acerca de...", self)

        menu_archivo.addAction(accion_ir_inicio)
        menu_archivo.addSeparator() 
        menu_archivo.addAction(accion_salir)
        menu_alumnos.addAction(accion_registrar_alumno)
        menu_alumnos.addAction(accion_gestionar_calificaciones)
        menu_alumnos.addAction(accion_consultar_kardex)
        menu_ayuda.addAction(accion_acerca_de)

        toolbar = self.addToolBar("Barra de Herramientas Principal")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.addAction(accion_ir_inicio)
        toolbar.addAction(accion_registrar_alumno)
        toolbar.addAction(accion_gestionar_calificaciones)
        toolbar.addAction(accion_consultar_kardex)

        self.vistas = QStackedWidget()
        self.setCentralWidget(self.vistas)
        
        self.vista_inicio = QWidget()
        self.vista_inicio.setLayout(QVBoxLayout())
        self.vista_inicio.layout().addWidget(QLabel("<h1>Pantalla de Inicio</h1><p>Seleccione una opción del menú o la barra de herramientas.</p>"))
        
        self.vista_registro = VistaRegistroAlumno()
        self.vista_calificaciones = VistaCalificaciones()
        self.vista_kardex = VistaKardex()

        self.vistas.addWidget(self.vista_inicio)
        self.vistas.addWidget(self.vista_registro)
        self.vistas.addWidget(self.vista_calificaciones)
        self.vistas.addWidget(self.vista_kardex)

        self.statusBar().showMessage("Bienvenido al Sistema de Gestión UAMITOS.")

        accion_salir.triggered.connect(self.close)
        accion_acerca_de.triggered.connect(self.mostrar_acerca_de)
        accion_ir_inicio.triggered.connect(self.mostrar_vista_inicio)
        accion_registrar_alumno.triggered.connect(self.mostrar_vista_registro)
        accion_gestionar_calificaciones.triggered.connect(self.mostrar_vista_calificaciones)
        accion_consultar_kardex.triggered.connect(self.mostrar_vista_kardex)
        
        self.vistas.setCurrentWidget(self.vista_inicio)

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
    
    with open("estilos.qss", "r") as f:
        app.setStyleSheet(f.read())

    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())