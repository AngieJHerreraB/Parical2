import json
import os

#Cree una clase login que luego inicialice con un constructor, definí que se utilizaría .json y dos atributos el data y el load de ingresar
class Cargar:
    def __init__(self, data= r"C:\Users\juand\Downloads\TrabajoUnidad3Monitor\Dseguimiento3Monitor.json"):
        self.data = data
        self.loadD()

    def loadD(self):
        if os.path.exists(self.data):  #Aquí verifico si el usuario existe
            with open(self.data, "r") as file: #si existe en self.data, con esta linea puedo abrir el .json
                self.usuario = json.load(file) #Aquí convierto los archivos .json en objetos python que se puedan leer

        else:
            self.usuario = [] #si no existe se guarda en un lista

    def guardarD(self):
        with open(self.data, "w") as file:
                print(self.usuario) #Con esta línea se puede abrir el archivo en modo escritura "w"
                json.dump(self.usuario, file, indent=4) #con el json.dump convierto esos objetos python ahora en unos .json con 3 argumentos

    
    def agregarU(self, usuario:dict):
        if not any(u["id"] == usuario["id"] for u in self.usuario): #verifico si ya hay un usuario en la lista mediante el id
            self.usuario.append(usuario) #agrego el usuario a la lista de usuarios
            self.guardarD() #guardo el cambio en la lista
            return True #cumple
        return False #no cumple

    def eliminarU(self, usuarioID:str): #el id del usuario debe ser un str
        initLen = len(self.usuario) #almaceno la información de la lista de usuarios a initlen
        self.usuario = [u for u in self.usuario if u["id"] != usuarioID] #verifico el usuario mediante el id y si coincide se elimina
        self.guardarD() #guardo los cambios en la lista de usuarios
        if initLen == len(self.usuario): #revisa si hubieron o no cambios
            return 0 #no hubieron
        else:
            return 1 #si hubieron

    def buscarUsuario(self, initName:str):
        initName = initName.lower().strip() #con el lower vemos que no importe si se escribe en mayus o en min, el strip elimina espacios en blanco
        return [usuario for usuario in self.usuario if usuario["id"].lower().strip().startswith(initName)] #me muestra los usuarios identificados por el id registrado
    

class UsuarioM:
    def __init__(self, dataU = "users.json"):
        self.dataU = dataU
        self.loadU()

    def loadU(self):
        try:
            with open (self.dataU, "r") as file:
                self.datas = json.load(file)
        except FileNotFoundError:
            self.datas = []
            print("No existe el archivo")

    def archivosJ(self, usuarioE: str, pw:str):  #archivos = existe
        try:
            for i in self.datas:
                if i["usuario"] == usuarioE and i["contrasena"] == pw:
                    return (1, f"{usuarioE} Bienvenido al sistema")
                return 0
        except TypeError:
            return 2