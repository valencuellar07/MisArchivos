import PyPDF2
from logging import root
import os
from tkinter import filedialog
from PIL import Image
import fitz
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import aspose.words as aw

listPdf=[]
listPdfImag=[]
listPalabras=[]
listWord=[]
listTxt=[]

class Pdf:
    def __init__(self,nombre,numPag,encrip,ruta):
        self.nombre=nombre
        self.numPag=int(numPag)
        self.encrip=encrip
        self.ruta=ruta

    def MostrarLista(self):
        print("Nombre:",self.nombre)
        print("Número de páginas:",self.numPag)
        print("¿Está encriptado?:",self.encrip)
    
    def CambiarDatos(self):
        root.directory = filedialog. askopenfilename()
        route = root.directory
        pdfObj= open (route,'rb')
        pdfLector= PyPDF2.PdfFileReader(pdfObj)
        nombre_pdf =os.path.splitext(os.path.basename(route))[0]
        self.nombre=nombre_pdf
        self.numPag=pdfLector.numPages
        self.encrip=pdfLector.isEncrypted
        self.ruta=str(route)

        print ("\nDatos del PDF cambiados")
        print("\nNombre del archivo:",nombre_pdf)
        print("Cantidad de hojas del PDF:",pdfLector.numPages)
        print("¿Está encriptado?", pdfLector.isEncrypted)
        pdfObj.close()

class Imagenes:
    def __init__(self,pdf,numImg):
        self.pdf=pdf
        self.numImg=int(numImg)

    def MostrarListaImage(self):
        print("\nNombre:",self.pdf.nombre)
        print("Número de páginas:",self.pdf.numPag)
        print("Número de imagenes:",self.numImg)
        
    def ExtraerImagenesList(self):
        pdfObj= open (self.pdf.ruta,'rb')
        pdfLector= PyPDF2.PdfFileReader(pdfObj)

        fullPages= self.pdf.numPag

        for numPages in range (fullPages):

            page= pdfLector.pages[numPages]

            count=0
            for image_file_obj in page.images:
                with open (str(count)+image_file_obj.name,"wb") as img:
                    img.write(image_file_obj.data)
                    count+=1      
            
        pdfObj.close()

class Palabras:
    def __init__(self,pdfNom,palabras,veces):
        self.pdfNom=pdfNom
        self.palabras=palabras
        self.veces=veces

    def MostrarListPalabras (self):
        print("\nPalabra:",self.palabras)
        print("No Veces:",self.veces)
        print("Nombre PDF:",self.pdfNom)

class Docx:
    def __init__(self,nombre,ruta):
        self.nombre=nombre
        self.ruta=ruta

    def MostrarWords(self):
        print("Nombre archivo:",self.nombre)
        print("Ruta:",self.ruta)
    
    def ConvertiraPdf(self):
        doc = aw.Document(self.ruta)
        saveOptions = aw.saving.PdfSaveOptions()
        saveOptions.compliance = aw.saving.PdfCompliance.PDF17 
        doc.save(self.nombre+".pdf", saveOptions)

class ArchivoTxt():
    def __init__(self,nombre,ruta):
        self.nombre=nombre
        self.ruta=ruta

    def MostrarTxts(self):
        print("Nombre archivo:",self.nombre)
        print("Ruta:",self.ruta)
    
    def ConvertirTXTaPdf(self):
        doc = aw.Document(self.ruta)
        doc.save(self.nombre+".pdf")

def ExtraerDatosTXT():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    #print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        head, tail = os.path.split(route+documento)
        txt=ArchivoTxt(tail,route+documento)
        listTxt.append(txt)

def TxtaPdf():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        head, tail = os.path.split(route+documento)
        doc = aw.Document(route+documento)
        doc.save(tail+".pdf")

def ExtraerDatosWord():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    #print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        head, tail = os.path.split(route+documento)
        word=Docx(tail,route+documento)
        listWord.append(word)

def WordaPdf():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        head, tail = os.path.split(route+documento)
        doc = aw.Document(route+documento)
        saveOptions = aw.saving.PdfSaveOptions()
        saveOptions.compliance = aw.saving.PdfCompliance.PDF17 
        doc.save(tail+".pdf", saveOptions)


def GraficaPalabras():
    y=[]
    nomPdf=input("Escriba el nombre del pdf (que esté en la lista): ")
    for i in range (len(listPalabras)):
        if(listPalabras[i].pdfNom==nomPdf):
            for j in range(int(listPalabras[i].veces)):
                y.append(listPalabras[i].palabras)

    plt.hist(y)
    plt.title("Histograma palabras")
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.show()

def AnalizarPdfImage():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        pdfObj= open(route+documento,'rb')
        pdfLector= PyPDF2.PdfFileReader(pdfObj)
        nombre_pdf =os.path.splitext(os.path.basename(route+documento))[0]
        numePaginas=pdfLector.numPages
        encriptado=pdfLector.isEncrypted

        for numPages in range (numePaginas):

            page= pdfLector.pages[numPages]

            count=0
            for image_file_obj in page.images:
                count+=1      
                
        if(count>0):
            print("El archivo",nombre_pdf,"tiene",count,"imagenes")
            pdf=Pdf(nombre_pdf,numePaginas,encriptado,route+documento)
            pdfImg=Imagenes(pdf,count)
            listPdfImag.append(pdfImg)

        pdfObj.close()    

def Renombrar ():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)

    documentos=os.listdir(route)

    for documento in documentos:
        
        nombre_pdf =os.path.splitext(os.path.basename(route+documento))[0]
        print("Nombre actual:",nombre_pdf)
        nombreNuevo=input("Nombre nuevo: ")
        os.rename(route+documento,route+nombreNuevo+'.pdf')

def CambiarDatosLista():

    for i in range(len(listPdf)):
        print("\nPDF #",i+1)
        listPdf[i].MostrarLista()
    
    nombre=input("Escriba el nombre del pdf que desea renovar datos: ")

    for j in range(len(listPdf)):
        if(listPdf[j].nombre==nombre):
            listPdf[j].CambiarDatos()
        
def ExtraerImagenes():
    root.directory = filedialog. askopenfilename()
    route = root.directory
    #print (route)
    pdfObj= open (route,'rb')
    pdfLector= PyPDF2.PdfFileReader(pdfObj)

    fullPages= len(pdfLector.pages)

    for numPages in range (fullPages):

        page= pdfLector.pages[numPages]

        count=0
        for image_file_obj in page.images:
            with open (str(count)+image_file_obj.name,"wb") as img:
                img.write(image_file_obj.data)
                count+=1      
          
    pdfObj.close()

def IngresarDatosPDF():
    root.directory = filedialog.askdirectory()
    route = root.directory + '/'
    print (route)
    documentos=os.listdir(route)
    for documento in documentos:
        pdfObj= open(route+documento,'rb')
        pdfLector= PyPDF2.PdfFileReader(pdfObj)
        nombre_pdf =os.path.splitext(os.path.basename(route+documento))[0]
        numePaginas=pdfLector.numPages
        encriptado=pdfLector.isEncrypted
        print("\nNombre del archivo:",nombre_pdf)
        print("Cantidad de hojas del PDF:",numePaginas)
        print("¿Está encriptado?", encriptado)  
        pdf=Pdf(nombre_pdf,numePaginas,encriptado,str(route+documento))
        listPdf.append(pdf)
        pdfObj.close()    

def CuentaPalabras (palabra):
    root.directory = filedialog. askopenfilename()
    route = root.directory
    #print (route)
    pdfObj= open(route,'rb')
    pdfLector= PyPDF2.PdfFileReader(pdfObj)
    numePaginas=pdfLector.numPages
    nombre_pdf =os.path.splitext(os.path.basename(route))[0]
    print("Nombre del archivo:",nombre_pdf)
    veces=0
    for i in range(numePaginas):
        pagina=pdfLector.getPage(i)
        text=pagina.extractText()
        veces += text.count(palabra)
        #print(text)
     
    print("La palabra",palabra,"se repite",veces,"veces")
    word=Palabras(nombre_pdf,palabra,veces)
    listPalabras.append(word)
    pdfObj.close()

def TablasListaPDF():
    fig, ax =plt.subplots(1,1)
    data=[]
    datosInd=[]
    for i in range (len(listPdf)):
        datosInd=[]
        datosInd.append(listPdf[i].nombre)
        datosInd.append(listPdf[i].numPag)
        datosInd.append(listPdf[i].encrip)
        data.append(datosInd)
    print(data)
    column_labels=["Nombre", "Num Pág.", "Encriptado"]
    df=pd.DataFrame(data,columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values,
            colLabels=df.columns,
            loc="center")
    
    plt.show()

def TablasListaPDFImg():
    fig, ax =plt.subplots(1,1)
    data=[]
    datosInd=[]
    for i in range (len(listPdfImag)):
        datosInd=[]
        datosInd.append(listPdfImag[i].pdf.nombre)
        datosInd.append(listPdfImag[i].pdf.numPag)
        datosInd.append(listPdfImag[i].pdf.encrip)
        datosInd.append(listPdfImag[i].numImg)
        data.append(datosInd)
    print(data)
    column_labels=["Nombre", "Num Pág.", "Encriptado","Num Img"]
    df=pd.DataFrame(data,columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values,
            colLabels=df.columns,
            loc="center")
    plt.show()

seguir=1
while(seguir==1): 
    print("------------------MANIPULADOR DE PDF'S------------------")
    print("Escoge la opción que deseas realizar:\n1. Mostrar datos de los PDF e insertarlos a la lista de PDF's\n2. Renombrar archivos de una carpeta\n3. Renovar datos de un pdf en la lista de PDF's\n4. Extraer las imagenes de un archivo\n5. Analizar cada pdf de una carpeta y decir si tiene imagenes. Guardar en lista PDF's con imágenes\n6. Extraer imagenes de un archivo de la lista PDF's con imágenes\n7. Contar frecuencia de una palabra en un archivo. Guardar en lista de palabras\n8. Graficas y tablas\n9. Guardar en lista archivos word\n10. Convertir archivos docx a pdf\n11. Convertir a pdf archivo docx en la lista\n12. Guardar en lista archivos txt\n13. Convertir archivos txt a pdf\n14. Convertir a pdf archivo txt en la lista")
    opcion=int(input())
    if(opcion==1):
        IngresarDatosPDF()
    if(opcion==2):
        Renombrar()
    if(opcion==3):
        CambiarDatosLista()
    if(opcion==4):
        ExtraerImagenes()
    if(opcion==5):
        AnalizarPdfImage()
    if(opcion==6):
        for i in range (len(listPdfImag)):
            print("\nArchivo",i+1)
            listPdfImag[i].MostrarListaImage()

        nombre=input("\nEscriba el nombre del archivo que desea extraer imagenes: ")
        for j in range (len(listPdfImag)):
            if(listPdfImag[j].pdf.nombre==nombre):
                listPdfImag[j].ExtraerImagenesList()
    if(opcion==7):
        palabra=input("Escriba la palabra que desea contar: ")
        CuentaPalabras(palabra)
    if(opcion==8):
        print("1. Grafica de frecuencia de palabras de un pdf\n2. Tabla de lista PDF's\n3. Tabla de lista PDF's con imágenes")
        opcion2=int(input())
        if(opcion2==1):
            for i in range (len(listPalabras)):
                listPalabras[i].MostrarListPalabras()
            GraficaPalabras()
        if(opcion2==2):
            TablasListaPDF()
        if(opcion2==3):
            TablasListaPDFImg()
    if(opcion==9):
        ExtraerDatosWord()
    if(opcion==10):
        WordaPdf()
    if(opcion==11):

        for i in range(len(listWord)):
            print("\nArchivo #",i+1)
            listWord[i].MostrarWords()
        archivo=input("Escriba el nombre del archivo: ")

        for x in range(len(listWord)):
            if(listWord[i].nombre==archivo):
                listWord[i].ConvertiraPdf()
    if(opcion==12):
        ExtraerDatosTXT()
    if(opcion==13):
        TxtaPdf()
    if(opcion==14):

        for i in range(len(listTxt)):
            print("\nArchivo #",i+1)
            listTxt[i].MostrarTxts()
        archivo=input("Escriba el nombre del archivo: ")

        for x in range(len(listTxt)):
            if(listTxt[i].nombre==archivo):
                listTxt[i].ConvertirTXTaPdf()

    print("¿Desea volver al menú?")
    seguir=int(input("1. SI\n2. NO "))

