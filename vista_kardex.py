import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaKardex(QWidget):
    def __init__(self):
        super().__init__()

        layout_busqueda = QHBoxLayout()
        label_id = QLabel("No. Alumno:")
        self.entry_id = QLineEdit()
        self.entry_id.setPlaceholderText("Ingrese ID del alumno")
        self.boton_buscar = QPushButton("Buscar Kardex")
        
        layout_busqueda.addWidget(label_id)
        layout_busqueda.addWidget(self.entry_id)
        layout_busqueda.addWidget(self.boton_buscar)

        label_titulo = QLabel("<h2>Kardex del Alumno</h2>")
        label_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tabla_kardex = QTableWidget()
        self.tabla_kardex.setColumnCount(2)
        self.tabla_kardex.setHorizontalHeaderLabels(["Materia", "Calificación Final"])
        
        header = self.tabla_kardex.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

        self.label_promedio = QLabel("<h3>Promedio actual: N/A</h3>")
        self.label_promedio.setAlignment(Qt.AlignmentFlag.AlignRight)

        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_busqueda)
        layout_principal.addWidget(label_titulo)
        layout_principal.addWidget(self.tabla_kardex)
        layout_principal.addWidget(self.label_promedio)

        self.boton_buscar.clicked.connect(self.buscar_kardex)
        self.entry_id.returnPressed.connect(self.buscar_kardex)

    @Slot()
    def buscar_kardex(self):
        student_id = self.entry_id.text().strip()
        if not student_id:
            QMessageBox.warning(self, "ID Vacío", "Por favor, ingrese un número de alumno.")
            return
        
        filename = f"{student_id}.txt"

        self.tabla_kardex.setRowCount(0)
        self.label_promedio.setText("<h3>Promedio actual: N/A</h3>")

        if not os.path.exists(filename):
            QMessageBox.critical(self, "Error", f"No se encontró un historial de calificaciones para el alumno con ID: {student_id}.")
            return

        try:
            with open(filename, 'r') as f:
                lineas = [line.strip() for line in f.readlines()]
            
            self.tabla_kardex.setRowCount(len(lineas))
            calificaciones_validas = []
            
            for fila, linea in enumerate(lineas):
                if ',' in linea:
                    materia, calificacion_str = linea.split(',', 1)
                else:
                    materia, calificacion_str = linea, ""

                try:
                    if calificacion_str:
                        calificaciones_validas.append(float(calificacion_str))
                except ValueError:
                    pass

                item_materia = QTableWidgetItem(materia)
                item_calificacion = QTableWidgetItem(calificacion_str)
                item_materia.setFlags(item_materia.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item_calificacion.setFlags(item_calificacion.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.tabla_kardex.setItem(fila, 0, item_materia)
                self.tabla_kardex.setItem(fila, 1, item_calificacion)

            if calificaciones_validas:
                promedio = sum(calificaciones_validas) / len(calificaciones_validas)
                self.label_promedio.setText(f"<h3>Promedio actual: {promedio:.2f}</h3>")
            else:
                self.label_promedio.setText("<h3>Promedio actual: No calculable</h3>")

        except Exception as e:
            QMessageBox.critical(self, "Error al Cargar", f"No se pudo leer el archivo de calificaciones:\n{e}")