from datetime import datetime
from datetime import timedelta

listPrestamos=[]  
listLibros=[]
listAutores=[]
listMultas=[]
listClientes=[]

class Biblioteca:
    def __init__(self,nombre,direccion,id):
        self.nombre = nombre
        self.direccion=direccion
        self.id = id


class Libro:
    def __init__(self, nombre,clasi, edit, año, autores, isbn,numPag, formato, estado):
        self.nombre = nombre
        self.clasi = clasi
        self.edit = edit
        self.año = año
        self.autores = autores
        self.isbn = isbn
        self.numPag = numPag
        self.formato = formato
        self.estado = estado
    
def IngresarLibro(cantLibros):

    for i in range(0,cantLibros,1):
        print ("\nIngrese los datos del Libro",i+1,"\n")
        nombre=input("Nombre: ")
        clasi=input("Clasificación: ")
        edit=input("Editorial: ")
        año=input("Año: ")
        isbn=input("ISBN: ")
        numPag=input("Número de páginas: ")
        formato=input("Formato: ")
        autores=input("Autor(es) (Separados por ','): ")
        IngresarAutor(autores)
        libro=Libro(nombre,clasi, edit, año, autores, isbn,numPag, formato,"Disponible")
        listLibros.append(libro)
    for c in range(0,len(listLibros),1):
         print("Libros registrados: ",listLibros[c].nombre)

libro=Libro("Casa","Romance","Panini","2003","Pedro","542343","28", "pdf","Disponible")
listLibros.append(libro)

libro2=Libro("Cocina","Recetas","Norma","2005","Ramiro","2343543","12", "fisico","Disponible")
listLibros.append(libro2)

libro3=Libro("Firulais","Ficcion","Panamericana","2013","Carla","768743","115", "pdf","Prestado")
listLibros.append(libro3)

class Autor:
    def __init__(self, nombre,nacionalidad, vinculacion, nacimiento):
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.vinculacion = vinculacion
        self.nacimiento = nacimiento

autorL=Autor("Pedro","Colombiano","nose","10/02/1968")   
listAutores.append(autorL)

autorL2=Autor("Ramiro","Colombiano","nose","08/12/1965")   
listAutores.append(autorL2)

def IngresarAutor(autores):
    nombres=autores.split(",")
    valor=False
   
    for x in range (0,len(nombres),1):
        for y in range (0,len(listAutores),1):
            if(nombres[x]==listAutores[y].nombre):
                valor=True
                break
            else:
                valor=False

        if(valor==False):
            print("\nAutor:",nombres[x])
            nacion=input("Nacionalidad: ")
            vincu=input("Vinculación: ")
            naci=input("Nacimiento: ")
            autor=Autor(nombres[x],nacion,vincu,naci)
            listAutores.append(autor)
            print("\nAutor registrado")

                
class Prestamo:    
    def __init__(self,prestatario,fechaInicio,fechaFin,libro,cant):
        self.prestatario=prestatario
        self.fechaInicio = fechaInicio 
        self.fechaFin = fechaFin 
        self.libro=libro
        self.cant=cant

    def ChecarGenerarMulta(self,fechaAct):
        multa=False
        
        fechaSep=fechaAct.split("/")
        fechaActual = datetime(int(fechaSep[2]), int(fechaSep[1]), int(fechaSep[0]), 00, 00, 00, 00000)
      
        diasMulta= fechaActual-self.fechaFin
        if(diasMulta.days>0):
            valor=5000*diasMulta.days
            multa=Multa(self.prestatario,valor,self.libro)
            print("Libro con multa: ",self.libro.nombre)
            print("Dias de multa:",diasMulta.days)
            print("El cliente",self.prestatario.nombre,"tiene una multa de: ",valor)
            listMultas.append(multa)
            multa=True
            for x in range(0,len(listClientes),1):
                if(listClientes[x].nombre==self.prestatario.nombre):
                    listClientes[x].ChecarEstado()
            self.libro.estado="Prestado con multa"
        else:
            print("Al cliente",self.prestatario.nombre,"aún le quedan",-1*diasMulta.days,"dias")
        return multa

    def ReportesLibros(self):
        if(self.libro.estado=="Prestado con multa"):
            print(self.libro.nombre," - ",self.libro.estado)

        if(self.libro.estado=="Prestado"):
            print(self.libro.nombre," - ",self.libro.estado," - ",self.fechaFin)
        
def PrestarLibro():
    cantLibros=0
    dias=0
    print("Escoja el tipo de persona a prestar.\n")
    prestatario=int(input("1. Estudiante\n2. Profesor\n3. Trabajador\n"))
    fechaI=input("Fecha (dd/mm/aa):")
    fechaSep=fechaI.split("/")
    fechaInicio = datetime(int(fechaSep[2]), int(fechaSep[1]), int(fechaSep[0]), 00, 00, 00, 00000)
    
    if(prestatario==1):
        cantLibros=int(input("Cantidad de libros: "))
        if (cantLibros>5):
            print("Solo puedes pedir prestado máximo 5 libros")
            cantLibros=int(input("Cantidad de libros: "))
        dias=30
        nom=input("Nombre persona: ")
        cod=input("Código: ")
        presta=Prestatario(nom,cod,"Estudiante","Con libro(s)",dias)

    if(prestatario==2):
        cantLibros=int(input("Cantidad de libros: "))
        if (cantLibros>10):
            print("Solo puedes pedir prestado máximo 10 libros")
            cantLibros=int(input("Cantidad de libros: "))
        dias=15
        nom=input("Nombre persona: ")
        cod=input("Cédula: ")
        presta=Prestatario(nom,cod,"Profesor","Con libro(s)",dias)

    if(prestatario==3):
        cantLibros=int(input("Cantidad de libros: "))
        if (cantLibros>8):
            print("Solo puedes pedir prestado máximo 8 libros")
            cantLibros=int(input("Cantidad de libros: "))
        dias=15
        nom=input("Nombre persona: ")
        cod=input("Cédula: ")
        presta=Prestatario(nom,cod,"Trabajador","Con libro(s)",dias)

    listClientes.append(presta)
    fechaFin=fechaInicio + timedelta(days=dias)
    for w in range(0,cantLibros,1):   
        libro=input("Libro: ")  
        for y in range(0,len(listLibros),1):
            if(listLibros[y].nombre==libro):
                prestar=Prestamo(presta,fechaInicio,fechaFin,listLibros[y],cantLibros)
                listLibros[y].estado="Prestado"
                listPrestamos.append(prestar)
    print("\nLista de libros:")
    for j in range(0,len(listLibros),1):
        print(listLibros[j].nombre," - ",listLibros[j].estado)
        
    print("\nLista de Prestamos:")
    for g in range(0,len(listPrestamos),1):
        print(listPrestamos[g].prestatario.nombre," - ",listPrestamos[g].libro.nombre)

def DevolverLibro():
    fechaAct=input("Fecha actual (dd/mm/aa):")
    nombre=input("Escriba el nombre del usuario: ")
    libroDev=input("Escriba el libro que desea devolver: ")

    for z in range (0,len(listPrestamos),1):
        if(listPrestamos[z].prestatario.nombre==nombre and listPrestamos[z].libro.nombre==libroDev):
            if(listPrestamos[z].ChecarGenerarMulta(fechaAct)==True):
                print("Debe pagar la multa")
                for x in range (0,len(listMultas),1):
                    if(listMultas[x].persona.nombre==nombre and listMultas[x].libro.nombre==libroDev):
                        listMultas[x].PagarMulta()
            else:
                for y in range (0,len(listPrestamos),1):
                    if(listPrestamos[y].prestatario.nombre==nombre):
                        print("Gracias por devolver el libro.")  
                        
            for j in range(0,len(listLibros),1):
                if(listLibros[j].nombre==libroDev):
                    listLibros[j].estado="Disponible"
            listPrestamos.pop(z)            
        
    for w in range (0,len(listClientes),1):
        listClientes[w].ChecarEstado()
                
    print("\nLista de libros:")
    for j in range(0,len(listLibros),1):
        print(listLibros[j].nombre," - ",listLibros[j].estado)

    
def is_empty(data_structure):
    if data_structure:
        return False
    else:
        return True

class Prestatario:
    def __init__(self,nombre,cedula,cargo,estado,dias):
        self.nombre = nombre
        self.cedula=cedula  
        self.cargo=cargo   
        self.estado=estado
        self.dias=dias
    
    def ChecarEstado(self):
        prestado=False
        multaConj=set(listMultas) & set(listPrestamos)
        
        for i in range (0,len(listPrestamos),1):
            if(listPrestamos[i].prestatario.nombre==self.nombre):
                prestado=True
            else:
                prestado=False


        if(is_empty(multaConj)==True and prestado==False):
            self.estado="Sin libro(s) prestado(s)"
            print("Estado cambiado. Cliente a paz y salvo.")

        if(is_empty(multaConj)==False):
            self.estado="Con libro(s) prestado(s) y multa"

        if(is_empty(multaConj)==True and prestado==True):
            self.estado="Con libro(s) prestado(s)"
            

        for s in range (0,len(listClientes),1):
            print(listClientes[s].nombre," - ",listClientes[s].estado)



class Multa:
    def __init__(self,persona,valor,libro):
        self.valor = valor
        self.persona=persona
        self.libro=libro

    def PagarMulta(self):
        for i in range (0, len(listMultas),1):
            if(listMultas[i].persona.nombre==self.persona.nombre and listMultas[i].libro.nombre==self.libro.nombre):
                print("Multa por el monto de",self.valor,"pesos. Pagada.")
                print("Gracias por devolver el libro.")
                listMultas.pop(i)

seguir=1
while (seguir==1):
    print("\n------------------BIBLIOTECA------------------\n")
    opcion=int(input("1. Registrar libro\n2. Prestar libro\n3. Registrar devolución\n4. Reportes \n"))
    if(opcion==1):
        numLibros=int( input("Escriba la cantidad de libros que desea registrar: "))
        IngresarLibro(numLibros)
    if(opcion==2):
        PrestarLibro()

    if(opcion==3):
        DevolverLibro()

    if(opcion==4):
        print("\nReporte clientes con multa\n")
        fechaAct=input("Fecha actual (dd/mm/aa):")
        for o in range(0,len(listPrestamos),1):
            listPrestamos[o].ChecarGenerarMulta(fechaAct)
        print("\nReporte libros\n")
        for o in range(0,len(listPrestamos),1):
            listPrestamos[o].ReportesLibros()
        

    seguir=int(input("\n¿Desea volver al menu?\n1. Si 2. No\n"))