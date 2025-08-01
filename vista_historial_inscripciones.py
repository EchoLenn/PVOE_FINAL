import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaHistorialInscripciones(QWidget):
    def __init__(self):
        super().__init__()

        self.tabla_historial = QTableWidget()
        self.tabla_historial.setColumnCount(4)
        self.tabla_historial.setHorizontalHeaderLabels(["ID Alumno", "Fecha", "Grupo", "Costo"])
        
        header = self.tabla_historial.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
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
            filename = "inscripciones.txt"
            if not os.path.exists(filename):
                QMessageBox.information(self, "Historial Vacío", "Aún no se ha realizado ninguna inscripción.")
                self.tabla_historial.setRowCount(0)
                return
            
            with open(filename, "r", encoding="utf-8") as archivo:
                lineas = [line.strip() for line in archivo.readlines() if line.strip()]

            self.tabla_historial.setRowCount(len(lineas))

            for fila, linea in enumerate(lineas):
                partes = linea.split(',')
                datos = {}
                for parte in partes:
                    clave, valor = parte.split(':', 1)
                    datos[clave] = valor
                
                self.tabla_historial.setItem(fila, 0, QTableWidgetItem(datos.get("ID", "")))
                self.tabla_historial.setItem(fila, 1, QTableWidgetItem(datos.get("Fecha", "")))
                self.tabla_historial.setItem(fila, 2, QTableWidgetItem(datos.get("Grupo", "")))
                self.tabla_historial.setItem(fila, 3, QTableWidgetItem(datos.get("Costo", "")))
        
        except FileNotFoundError:
             QMessageBox.information(self, "Historial Vacío", "Aún no se ha realizado ninguna inscripción.")
             self.tabla_historial.setRowCount(0)
        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar", f"No se pudo leer el archivo de inscripciones:\n{e}")