import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import database_manager

class VistaHistorialInscripciones(QWidget):
    def __init__(self):
        super().__init__()
        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(5)
        self.tabla_historial.setHorizontalHeaderLabels(["ID Alumno", "Nombre Alumno", "Grupo", "Fecha", "Costo"])
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabla_historial.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.boton_cargar = QPushButton("Cargar / Actualizar Historial")
        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(QLabel("<h2>Historial de Inscripciones</h2>"))
        layout_principal.addWidget(self.boton_cargar)
        layout_principal.addWidget(self.tabla_historial)
        self.boton_cargar.clicked.connect(self.cargar_historial)

    @Slot()
    def cargar_historial(self):
        try:
            historial = database_manager.obtener_historial_inscripciones()
            self.tabla_historial.setRowCount(len(historial))
            for fila, registro in enumerate(historial):
                id_alumno, nombre, apellido, grupo, fecha, costo = registro
                nombre_completo = f"{nombre} {apellido}".strip()
                self.tabla_historial.setItem(fila, 0, QTableWidgetItem(str(id_alumno)))
                self.tabla_historial.setItem(fila, 1, QTableWidgetItem(nombre_completo))
                self.tabla_historial.setItem(fila, 2, QTableWidgetItem(grupo))
                self.tabla_historial.setItem(fila, 3, QTableWidgetItem(fecha))
                self.tabla_historial.setItem(fila, 4, QTableWidgetItem(f"{costo:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar", f"No se pudo leer el historial: {e}")