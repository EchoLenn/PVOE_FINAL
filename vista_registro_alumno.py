import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *

class VistaRegistroAlumno(QWidget):
    def __init__(self):
        super().__init__()
        
        grupo_alumno = self._crear_grupo_alumno()
        grupo_tutor = self._crear_grupo_tutor()
        self.boton_registrar = QPushButton("Registrar Alumno")

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.boton_registrar)
        layout_botones.addStretch()

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(grupo_alumno)
        layout_principal.addWidget(grupo_tutor)
        layout_principal.addLayout(layout_botones)

        self.boton_registrar.clicked.connect(self.registrar_datos)

    def _crear_grupo_alumno(self):
        grupo_alumno = QGroupBox("Datos del Alumno")
        layout = QFormLayout()

        self.nombre_alum = QLineEdit()
        self.apellido_pa = QLineEdit()
        self.apellido_ma = QLineEdit()
        self.direccion = QLineEdit()
        self.fecha_nacimiento = QLineEdit()
        self.fecha_nacimiento.setPlaceholderText("dd/mm/aaaa")
        self.genero_m = QCheckBox("Masculino")
        self.genero_f = QCheckBox("Femenino")

        layout_genero = QHBoxLayout()
        layout_genero.addWidget(self.genero_m)
        layout_genero.addWidget(self.genero_f)

        layout.addRow("Nombre(s):", self.nombre_alum)
        layout.addRow("Apellido Paterno:", self.apellido_pa)
        layout.addRow("Apellido Materno:", self.apellido_ma)
        layout.addRow("Dirección:", self.direccion)
        layout.addRow("Fecha de Nacimiento:", self.fecha_nacimiento)
        layout.addRow("Género:", layout_genero)
        
        grupo_alumno.setLayout(layout)
        return grupo_alumno

    def _crear_grupo_tutor(self):
        grupo_tutor = QGroupBox("Datos del Padre o Tutor")
        layout = QFormLayout()

        self.nombre_pad = QLineEdit()
        self.telefono = QLineEdit()
        self.correo = QLineEdit()
        self.correo.setPlaceholderText("ejemplo@correo.com")

        layout.addRow("Nombre Completo:", self.nombre_pad)
        layout.addRow("Teléfono:", self.telefono)
        layout.addRow("Correo Electrónico:", self.correo)

        grupo_tutor.setLayout(layout)
        return grupo_tutor

    def _limpiar_formulario(self):
        for line_edit in self.findChildren(QLineEdit):
            line_edit.clear()
        self.genero_m.setChecked(False)
        self.genero_f.setChecked(False)
        
    def _generar_nuevo_id(self):
        id_file = "ultimo_id.txt"
        try:
            if os.path.exists(id_file):
                with open(id_file, 'r') as f:
                    ultimo_id = int(f.read().strip())
                    nuevo_id = ultimo_id + 1
            else:
                nuevo_id = 1000
            
            with open(id_file, 'w') as f:
                f.write(str(nuevo_id))
            
            return str(nuevo_id)
        except Exception as e:
            QMessageBox.critical(self, "Error Crítico", f"No se pudo generar un ID para el alumno:\n{e}")
            return None

    @Slot()
    def registrar_datos(self):
        nombre = self.nombre_alum.text().strip()
        ap_paterno = self.apellido_pa.text().strip()
        
        if not all([nombre, ap_paterno]):
            QMessageBox.warning(self, "Campos Incompletos", "El nombre y el apellido paterno son obligatorios.")
            return

        nuevo_id = self._generar_nuevo_id()
        if not nuevo_id:
            return

        datos = []
        datos.append("----- DATOS DEL ALUMNO -----")
        datos.append(f"ID de Alumno: {nuevo_id}")
        datos.append(f"Nombre: {nombre}")
        datos.append(f"Apellido Paterno: {ap_paterno}")
        datos.append(f"Apellido Materno: {self.apellido_ma.text().strip()}")
        datos.append(f"Dirección: {self.direccion.text().strip()}")
        datos.append(f"Fecha de Nacimiento: {self.fecha_nacimiento.text().strip()}")
    
        genero = "No especificado"
        if self.genero_m.isChecked():
            genero = "Masculino"
        elif self.genero_f.isChecked():
            genero = "Femenino"
        datos.append(f"Género: {genero}")

        datos.append("\n----- DATOS DEL TUTOR -----")
        datos.append(f"Nombre: {self.nombre_pad.text().strip()}")
        datos.append(f"Teléfono: {self.telefono.text().strip()}")
        datos.append(f"Correo: {self.correo.text().strip()}")
        datos.append("----------------------------")

        try:
            with open("registros_alumnos.txt", "a", encoding="utf-8") as archivo:
                archivo.write("\n".join(datos) + "\n\n")
            
            with open(f"{nuevo_id}.txt", "w") as f_calificaciones:
                pass
            
            QMessageBox.information(self, "Éxito", f"¡Alumno registrado correctamente!\n\nEl ID asignado es: {nuevo_id}")
            self._limpiar_formulario()
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar el archivo:\n{e}")