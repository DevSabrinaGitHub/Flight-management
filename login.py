from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from conexion_db import ejecutar_consulta

class LoginWindow(QtWidgets.QMainWindow):
    login_exitoso = pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        # Conectar botones a las funciones
        self.boton_aceptar.clicked.connect(self.iniciar_sesion)
        self.boton_cancelar.clicked.connect(self.cerrar_ventana)
        
        # Ocultar el mensaje de error al iniciar
        self.label_error.setVisible(False)

    def iniciar_sesion(self):
        usuario = self.input_usuario.text()
        contraseña = self.input_contrasena.text()

        # Consulta para verificar las credenciales
        query = "SELECT * FROM usuarios WHERE correo = ? AND contraseña = ?"
        resultado = ejecutar_consulta(query, (usuario, contraseña))
        
        if resultado:
            QtWidgets.QMessageBox.information(self, "Login", "Acceso exitoso")
            self.login_exitoso.emit()  # Emitir señal de login exitoso
        else:
            # Mostrar mensaje de error si las credenciales son incorrectas
            self.label_error.setText("Credenciales incorrectas")
            self.label_error.setVisible(True)

    def cerrar_ventana(self):
        self.close()
