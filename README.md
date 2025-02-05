# NLI_with_LLMs_ConcepNet
Evaluación de LLMs con corpus de NLI e información externa de ConcepNet

Primero se recuperan las relaciones de las palabras del vocabulario de los diferentes corpus
para reducir tiempos en procesamiento de identificación de relaciones entre la premisa y la hipótesis.

getRelaciones.py
comandosRelaciones

Para obtener las palabras multiterminos se ocuparon:

getRelacionesMultiterminos.py
comandosRelacionesMultiterminos

Se crean diccionarios para cada proceso y corpus para después integrarlos en una sola base de datos
Una vez procesado se respaldan los diccionarios
Al final se tendrán dos diccionarios globales en data/
Generales: wt -> wh
Contextuales: wh -> wt

Una vez obtenida la base de datos, se procede a realizar un proceso de ngrams
Los cuales serviran para identificar las primeras relaciones de sinonimia sobre el texto directo.
Por ejemplo, "wmd" tiene el sinonimo "weapons of massive destruction"


Para poder obtener las relaciones de los ejemplos de T y H, se requiere ejecutar un script:
La lista de comandos esta en comandos, los archivos de lectura deben de estar en pickle con las siguientes columnas: sentence1, sentence2 y gold_label
En el archivo comandos vienen las lineas de ejecución para su procesamiento

Relaciones_TH

Este script genera pickle con las relaciones correspondientes: G1, G2, G3, G4 y ST.

Llamadas a los LLMs
prompt:
En el archivo comandos se encuentra las instrucciones
callsLLM.py
