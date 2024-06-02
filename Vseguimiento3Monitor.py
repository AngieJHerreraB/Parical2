# se importan las librerias de PyQt5 y Sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QLineEdit, QPushButton, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from Cseguimiento3Monitor import ControladorU, Controlador

import sys

class Login(QMainWindow): # se crea una clase de la ventana principal
    def __init__(self): 
        super().__init__() # quien hereda atributos de QMainWindow
        loadUi(r"C:\Users\juand\Downloads\Info\Info\Info\ventanaMain.ui", self) # se carga la ruta de la ventana principal
        self.ControladorU = ControladorU() # se llama al controlador del usuario desde la vista
        self.Controlador = Controlador()  # se llama el controlador del sistema
        self.setWindowFlags(Qt.FramelessWindowHint) # permite eliminar los bordes
        self.setAttribute(Qt.WA_TranslucentBackground) # fondo transparente
        self.setupV() # se llaman los botones de la ventana
        
             
    def setupV(self): # botones con sus respectivas funciones
        self.boton_cerrar.clicked.connect(self.cerrarV)  
        self.boton_minimizar.clicked.connect(self.minimizar)
        self.ingresarUsuario.clicked.connect(self.loginV)
        self.agregarUsuario.clicked.connect(self.agregarV)   
        self.pw.setEchoMode(QLineEdit.Password) # permite ocultar los valores de la contraseña

        #subventana
        self.ingreso.clicked.connect(self.nuevoU)
        self.buscar_usuario.clicked.connect(self.buscarU)

        validator = QtGui.QIntValidator(1, 9999999, self) # se asegura de que el numero ingresado este entre ese valor
        self.tableView.verticalHeader().setVisible(False) # oculta el encabezado de la tabla
        self.id.setValidator(validator) # validaciones de id, busqueda, edad
        self.buscar.setValidator(validator)
        self.edad.setValidator(validator)
        self.leerU() # llama la funcion leer usuario
        self.tabla() # llama la funcion de crear tabla

        
    def loginV(self):
        self.stackedWidget_3.setCurrentIndex(1) #le digo a mi boton que se dirija a la ventana 2 que en este caso es la 1
        usuario = self.usuarioE.text() # toma los valores ingresados en los recuadros de texto
        password = self.pw.text()
        archivosJ = self.ControladorU.loginC(usuario, password) # llama al login del controlador y le entrega 2 argumentos
        if isinstance(archivosJ, tuple): # se verifica si devuelve una tupla de elementos
            self.Login = Login() # inicializa la calse login
            self.Login.show() # la muestra
            self.close() # y la cierra para dar paso a otra vista
            
        elif archivosJ == 0:  # si no cumple
            msgBox = QMessageBox() # lanza un MessageBox
            msgBox.setIcon(QMessageBox.Warning) # se llama el icono de precaucion
            msgBox.setText("El usuario no existe") # inicando que el usuario no existe
            msgBox.setWindowTitle('Vuelva a intentar') # ingrese nuevamente
            msgBox.setStandardButtons(QMessageBox.Ok) # conecta el boton de MessageBox
            msgBox.exec()  # cierra la ventana al dar en equis
        
    def oprimirBoton(self, event): # indica que el arrastre de la ventana ha iniciado
        if event.buttons() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def moverV(self, event): # mueve la ventana dada la elección del usuario
        try:
            if self.dragging:
                self.move(self.mapToGlobal(event.pos() - self.offset))
        except:
            pass

    def presionarV(self, event): # determina que el arraste ha terminado
        if event.button() == Qt.LeftButton:
            self.dragging = False
            
    def cerrarV(self): # permite cerrar una ventana
        sys.exit(app.exec_())   
        
    def minimizar(self): # permite minimizar el recuadro
        self.showMinimized()

    def agregarV(self): # permite apilar la informacion
        self.stackedWidget_3.setCurrentIndex(1)

    def leerU(self): # conecta la funcion mostrar usuario del controlador y lo retorna
        self.listaUsuarios = self.Controlador.mostrarU()

    def buscarU(self):   
        buscar = self.id_4.text()  # toma el texto del recuadro y busca el usuario
        self.listaUsuarios = self.Controlador.mostrarU(buscar)
        self.tabla() # enseña la info en forma de tabla

#Nombre, apellido, edad e identificación
    def nuevoU(self): # toma los valores para un nuevo usuario
        id = self.id.text()
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        edad = self.edad.text()

        if not id or not nombre or not apellido or not edad:  # verifica que toda la información esté completa
            mb = QMessageBox() # si no esta muestra un MesssageBox
            mb.setIcon(QMessageBox.warning)
            mb.setText("Por favor rellena las casillas faltantes")
            mb.setWindowTitle("Falta información")
            mb.setStandardButtons(QMessageBox.ok)
            mb.exec()
        else:
            usuario = {'id':id, 'nombre':nombre, 'apellido': apellido, 'edad': edad}  # si están todos los valores los toma
            unicoU = self.Controlador.nuevoU(usuario) # crea un nuevo usuario, llama la funcion del controlador
            if not unicoU:  # se verifica si ya exsite alguien la misma información
                mb = QMessageBox()
                mb.setIcon(QMessageBox.warning)
                mb.setText("Intentalo de nuevo")
                mb.setWindowTitle("ID ya existente")
                mb.setStandardButtons(QMessageBox.ok)
                mb.exec()
            else:  # si no, se crea la tabla
                self.leerU()
                self.tabla()
                self.id.setText("")
                self.nombre.setText("")
                self.apellido.setText("")
                self.edad.setText("")

    def tabla(self):
        self.tableView.setRowCount(len(self.listaUsuarios))  # establece el numero de columnas
        self.tableView.setColumnCount(5) # numero de columnas
        columnas = ["ID", "Nombre", "Apellido", "Edad", "Eliminar"]
        columnLayout = [ 'id','nombre','apellido','edad']
        self.tableView.setHorizontalHeaderLabels(columnas)  # usa la informaion como encabezado
        for row, usuario in enumerate(self.listaUsuarios):  # pasa por todos los usuarios obteniendo su indice
            for column in range(4):  # pasa los primero 4 numeros
                item = QTableWidgetItem(usuario[columnLayout[column]])  # se crea la tabla con la info de la lista Columnas
                self.tableView.setItem(row, column, item)  # coloca la información en la celda correspondiente

            boton = QPushButton('Borrar', self)  # conecta  el boton eliminar y lo posiciona al final
            boton.clicked.connect(lambda ch, r=row: self.eliminar(r))
            self.tableView.setCellWidget(row, 4, boton)
                
        self.tableView.setColumnWidth(0, 80)  # ajusta las dim de acuerdo a la celda
        self.tableView.setColumnWidth(1, 110)  
        self.tableView.setColumnWidth(2, 60)  
        self.tableView.setColumnWidth(3, 60)  
        self.tableView.setColumnWidth(4, 60)  

    def eliminar(self, row):
        
        id = self.tableView.item(row, 0).text()  # obtiene el id del paciente de la primera columna de la fila especificada
        deleted = self.Controlador.eliminarU(id) # se llama la funcion eliminar usuario del controlador
        if not deleted:  # si no fue borrado, aparece un MessageBox
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Sistem error")
            msgBox.setWindowTitle('ERROR')
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()
        self.leerU()  # se lee la informacion del usuario
        self.tabla()  # se actualiza la tabla

if __name__ == "__main__":  # inicializa la operación y se visualiza el programa
    app = QApplication(sys.argv)
    my_app = Login()
    my_app.show()
    sys.exit(app.exec_())