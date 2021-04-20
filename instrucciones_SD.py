import sys
import re
import string

def countingWords(texto):
    contador=0
    palabras=texto.split()
    contador=len(palabras)
    return contador




def wordCount(texto):
        eliminar = ",;:.!¡¿?#"
        #texto=texto.replace("\n"," ")
        texto = texto.translate({ord(c): " " for c in "\n"})
        texto = texto.translate({ord(c): None for c in eliminar})
        #for caracter in eliminar:
        #   texto=texto.replace(caracter,"")
        texto=texto.lower()
        palabras = texto.split(" ")
        #print(texto)
        diccionario_frecuencias = {}

        for palabra in palabras:
            if palabra in diccionario_frecuencias:
               diccionario_frecuencias[palabra] += 1
            else:
                diccionario_frecuencias[palabra] = 1

        diccionario_frecuencias.pop('', None)
        return diccionario_frecuencias

