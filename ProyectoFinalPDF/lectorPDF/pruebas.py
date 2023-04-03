import aspose.words as aw
import os
from tkinter import filedialog
from logging import root

listWord=[]
class Docx:
    def __init__(self,nombre,ruta):
        self.nombre=nombre
        self.ruta=ruta
def ExtraerDatosWord():

    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        head, tail = os.path.split(route+documento)
        word=Docx(tail,route+documento)
        listWord.append(word)
        doc = aw.Document(route+documento)
        saveOptions = aw.saving.PdfSaveOptions()
        saveOptions.compliance = aw.saving.PdfCompliance.PDF17 
        doc.save(tail+".pdf", saveOptions)

def Mostrar():
    for i in range (len(listWord)):
        print(listWord[i].nombre)
        print(listWord[i].ruta)

ExtraerDatosWord()
Mostrar()