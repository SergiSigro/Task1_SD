import sys
import re
import string

def countingWords(nombreFichero):
    contador=0
    try:
        with open(nombreFichero) as file_t:
            texto=file_t.read()
            #print(texto)

    except FileNotFoundError:
        mensaje="No existe el archivo " ,nombreFichero
        print(mensaje)
    else:
        palabras=texto.split()
        contador=len(palabras)

    finally:
        file_t.close()
    return contador




def wordCount(nombreFichero):
    try:
        eliminar = ",;:.!¡¿?#"
        with open(nombreFichero) as file_t:
            texto=file_t.read()
            texto=texto.replace("\n"," ")

            for caracter in eliminar:
                texto=texto.replace(caracter,"")
            texto=texto.lower()
            palabras = texto.split(" ")

            print(palabras)
            
            diccionario_frecuencias = {}

            for palabra in palabras:
                if palabra in diccionario_frecuencias:
                    diccionario_frecuencias[palabra] += 1
                else:
                    diccionario_frecuencias[palabra] = 1

            for palabra in diccionario_frecuencias:
                frecuencia = diccionario_frecuencias[palabra]
                print("'"+palabra+"'," , frecuencia,";")

    except FileNotFoundError:
        mensaje="No existe el archivo ", nombreFichero
        print(mensaje)

    finally:
        file_t.close()

print("COUNTING WORDS:")
nombre=sys.argv[1]
nPalabras=countingWords(nombre)
print("En el fichero hay ",nPalabras," palabras")
print("WORD COUNT:")
wordCount(nombre)
