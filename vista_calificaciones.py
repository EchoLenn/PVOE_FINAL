import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import Qt
import database_manager

class VistaCalificaciones(QWidget):
    def __init__(self):
        super().__init__()
        layout_busqueda = QHBoxLayout()
        label_id = QLabel("No. de Estudiante:")
        self.entry_id = QLineEdit()
        self.entry_id.setPlaceholderText("Ingrese ID y presione Buscar")
        self.boton_buscar = QPushButton("Buscar")
        layout_busqueda.addWidget(label_id)
        layout_busqueda.addWidget(self.entry_id)
        layout_busqueda.addWidget(self.boton_buscar)
        self.tabla_calificaciones = QTableWidget()
        self.tabla_calificaciones.setColumnCount(2)
        self.tabla_calificaciones.setHorizontalHeaderLabels(["Materia", "Calificación"])
        header = self.tabla_calificaciones.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.boton_guardar = QPushButton("Guardar Calificaciones")
        self.boton_guardar.setEnabled(False)
        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_busqueda)
        layout_principal.addWidget(self.tabla_calificaciones)
        layout_principal.addWidget(self.boton_guardar)
        self.boton_buscar.clicked.connect(self.buscar_alumno)
        self.entry_id.returnPressed.connect(self.buscar_alumno)
        self.boton_guardar.clicked.connect(self.guardar_calificaciones)

    def _cargar_materias_defecto(self):
        materias = ["Matemáticas", "Ciencias", "Historia", "Español", "Programación Visual"]
        self.tabla_calificaciones.setRowCount(len(materias))
        for fila, materia in enumerate(materias):
            item_materia = QTableWidgetItem(materia)
            item_materia.setFlags(item_materia.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_calificacion = QTableWidgetItem("")
            self.tabla_calificaciones.setItem(fila, 0, item_materia)
            self.tabla_calificaciones.setItem(fila, 1, item_calificacion)

    @Slot()
    def buscar_alumno(self):
        student_id = self.entry_id.text().strip()
        if not student_id:
            QMessageBox.warning(self, "ID Vacío", "Por favor, ingrese un número de estudiante.")
            return
        
        if not database_manager.verificar_alumno_existente(student_id):
            QMessageBox.critical(self, "Alumno No Encontrado", f"No se encontró un registro para el alumno con ID: {student_id}.")
            self.tabla_calificaciones.setRowCount(0)
            self.boton_guardar.setEnabled(False)
            return

        self.current_student_id = student_id
        calificaciones = database_manager.obtener_calificaciones(student_id)

        if not calificaciones:
            self._cargar_materias_defecto()
        else:
            self.tabla_calificaciones.setRowCount(len(calificaciones))
            for fila, (materia, calificacion) in enumerate(calificaciones):
                item_materia = QTableWidgetItem(materia)
                item_materia.setFlags(item_materia.flags() & ~Qt.ItemFlag.ItemIsEditable)
                calif_str = str(calificacion) if calificacion is not None else ""
                item_calificacion = QTableWidgetItem(calif_str)
                self.tabla_calificaciones.setItem(fila, 0, item_materia)
                self.tabla_calificaciones.setItem(fila, 1, item_calificacion)
        
        self.boton_guardar.setEnabled(True)

    @Slot()
    def guardar_calificaciones(self):
        if not hasattr(self, 'current_student_id') or not self.current_student_id:
            QMessageBox.warning(self, "Error", "No se ha seleccionado un alumno válido.")
            return
        
        lista_calificaciones = []
        calificaciones_invalidas = []
        
        for fila in range(self.tabla_calificaciones.rowCount()):
            materia_item = self.tabla_calificaciones.item(fila, 0)
            calificacion_item = self.tabla_calificaciones.item(fila, 1)
            
            if not materia_item or not calificacion_item:
                continue
                
            materia = materia_item.text()
            calificacion_texto = calificacion_item.text().strip()
            
            try:
                if calificacion_texto:
                    calificacion = float(calificacion_texto)
                    if calificacion < 0 or calificacion > 10:
                        calificaciones_invalidas.append(materia)
                        continue
                else:
                    calificacion = None
            except ValueError:
                calificaciones_invalidas.append(materia)
                continue
                
            lista_calificaciones.append((materia, calificacion))
        
        if calificaciones_invalidas:
            QMessageBox.warning(
                self, 
                "Calificaciones Inválidas", 
                f"Las siguientes materias tienen calificaciones inválidas (deben ser entre 0 y 10):\n"
                f"{', '.join(calificaciones_invalidas)}"
            )
            return
        
        if database_manager.guardar_calificaciones(self.current_student_id, lista_calificaciones):
            QMessageBox.information(self, "Éxito", f"Calificaciones del alumno {self.current_student_id} guardadas.")
            self.entry_id.clear()
            self.tabla_calificaciones.setRowCount(0)
            self.boton_guardar.setEnabled(False)
            delattr(self, 'current_student_id')
        else:
            QMessageBox.critical(self, "Error de Base de Datos", "No se pudieron guardar las calificaciones.")