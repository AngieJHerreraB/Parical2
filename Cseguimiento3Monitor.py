# se importa el modelo
from Mseguimiento3Monitor import *

class ControladorU: # se crea un controlador para el login
    def __init__(self, usuarioM:object = UsuarioM()):
            self.usuarioM = usuarioM

    def loginC(self, username:str, password:str):  # cuyo datos de entrada son el usuario y contraseña
         result = self.usuarioM.archivosJ(username, password)
         return result

class Controlador:  # se crea un controlador para comunicar las funciones de vista con el modulo
    def __init__(self, cargar = Cargar()):
          self.cargar = cargar
    def nuevoU(self, data: dict):
         return self.cargar.agregarU(data)  # se pasa la informacion al modelo en forma de diccionario
    
    def mostrarU(self, initName:str = ""):
         return self.cargar.buscarUsuario(initName)  # llama la funcion buscar del modelo
    
    def eliminarU(self, id:str):
         return self.cargar.eliminarU(id)  # llama la funcion eliminar del modelo
