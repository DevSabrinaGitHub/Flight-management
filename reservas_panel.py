from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3

class ReservasPanelWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('reservas_panel.ui', self)

        # Conectar botones
        self.btn_ver_reservas.clicked.connect(self.ver_reservas)
        self.btn_agregar_reserva.clicked.connect(self.agregar_reserva)
        self.btn_modificar_reserva.clicked.connect(self.modificar_reserva)
        self.btn_eliminar_reserva.clicked.connect(self.eliminar_reserva)
        self.btn_volver_menu.clicked.connect(self.volver_menu_principal)

        # Cargar reservas al iniciar
        self.ver_reservas()

    def ejecutar_consulta(self, query, params=()):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(query, params)
        resultado = cursor.fetchall()
        conn.commit()
        conn.close()
        return resultado

    def ver_reservas(self):
        self.tabla_reservas.setRowCount(0)
        query = """
        SELECT r.id, p.nombre || ' ' || p.apellido AS pasajero, r.vuelo_id, 
               r.fecha_creacion, r.estado, r.asiento_clase, r.precio 
        FROM reservas r
        JOIN pasajeros p ON r.pasajero_id = p.id
        """
        reservas = self.ejecutar_consulta(query)

        for row_number, reserva in enumerate(reservas):
            self.tabla_reservas.insertRow(row_number)
            for column_number, data in enumerate(reserva):
                self.tabla_reservas.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.actualizar_estadisticas()

    def agregar_reserva(self):
        pasajero_dni = self.input_dni_pasajero.text()
        vuelo_id = self.input_vuelo_id.text()
        fecha_creacion = self.input_fecha_creacion.date().toString("yyyy-MM-dd")
        estado = self.input_estado_reserva.currentText()
        asiento_clase = self.input_asiento_clase.currentText()
        precio = self.calcular_precio(asiento_clase)

        # Verificar que los campos no estén vacíos
        if not pasajero_dni or not vuelo_id or not fecha_creacion:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos.")
            return

        # Obtener el ID del pasajero por su DNI
        pasajero_id_query = "SELECT id FROM pasajeros WHERE dni = ?"
        pasajero = self.ejecutar_consulta(pasajero_id_query, (pasajero_dni,))

        if not pasajero:
            # Si no existe el pasajero, preguntar si se desea agregar
            nombre = self.input_nombre_pasajero.text()  # Campo de nombre
            apellido = self.input_apellido_pasajero.text()  # Campo de apellido

            if not nombre or not apellido:
                QMessageBox.warning(self, "Error", "Por favor, complete el nombre y apellido del pasajero.")
                return

            # Insertar nuevo pasajero
            insert_query = "INSERT INTO pasajeros (dni, nombre, apellido) VALUES (?, ?, ?)"
            self.ejecutar_consulta(insert_query, (pasajero_dni, nombre, apellido))
            QMessageBox.information(self, "Éxito", "Pasajero agregado correctamente.")

            # Ahora obtener el ID del nuevo pasajero
            pasajero = self.ejecutar_consulta(pasajero_id_query, (pasajero_dni,))

        pasajero_id = pasajero[0][0]

        # Verificar la franja horaria para el mismo pasajero (1 hora)
        overlap_query = '''
        SELECT COUNT(*) FROM reservas 
        WHERE pasajero_id = ? AND vuelo_id = ? AND 
              ABS(strftime('%s', fecha_creacion) - strftime('%s', ?)) < 3600
        '''
        resultado = self.ejecutar_consulta(overlap_query, (pasajero_id, vuelo_id, fecha_creacion))
        
        if resultado[0][0] > 0:
            QMessageBox.warning(self, "Error", "El pasajero tiene una reserva cercana a la misma hora.")
            return

        # Insertar la nueva reserva
        query = '''
        INSERT INTO reservas (pasajero_id, vuelo_id, fecha_creacion, estado, asiento_clase, precio)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (pasajero_id, vuelo_id, fecha_creacion, estado, asiento_clase, precio)
        self.ejecutar_consulta(query, params)
        QMessageBox.information(self, "Éxito", "Reserva agregada exitosamente.")
        self.ver_reservas()

    def calcular_precio(self, asiento_clase):
        # Definir precios según clase
        precios = {"normal": 100, "turista": 200, "premium": 300}
        return precios.get(asiento_clase, 100)

    def modificar_reserva(self):
        selected_row = self.tabla_reservas.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una reserva para modificar.")
            return

        reserva_id = self.tabla_reservas.item(selected_row, 0).text()
        nuevo_estado = self.input_estado_reserva.currentText()
        nueva_clase_asiento = self.input_asiento_clase.currentText()
        nuevo_precio = self.calcular_precio(nueva_clase_asiento)

        query = '''
        UPDATE reservas SET estado = ?, asiento_clase = ?, precio = ?
        WHERE id = ?
        '''
        params = (nuevo_estado, nueva_clase_asiento, nuevo_precio, reserva_id)
        self.ejecutar_consulta(query, params)
        QMessageBox.information(self, "Éxito", "Reserva modificada correctamente.")
        self.ver_reservas()

    def eliminar_reserva(self):
        selected_row = self.tabla_reservas.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Seleccione una reserva para eliminar.")
            return

        reserva_id = self.tabla_reservas.item(selected_row, 0).text()
        query = "DELETE FROM reservas WHERE id = ?"
        self.ejecutar_consulta(query, (reserva_id,))
        QMessageBox.information(self, "Éxito", "Reserva eliminada correctamente.")
        self.ver_reservas()

    def actualizar_estadisticas(self):
        total_query = "SELECT COUNT(*) FROM reservas"
        futuras_query = "SELECT COUNT(*) FROM reservas WHERE fecha_creacion >= DATE('now')"

        total_reservas = self.ejecutar_consulta(total_query)[0][0]
        reservas_futuras = self.ejecutar_consulta(futuras_query)[0][0]

        self.label_estadisticas.setText(f"Estadísticas: Total de Reservas Actuales: {total_reservas}, Futuras: {reservas_futuras}")

    def volver_menu_principal(self):
        self.close()  # Cierra el panel de reservas y vuelve al menú principal
