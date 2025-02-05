import pandas as pd
import numpy as np
import utils as ut # esta librería tiene funciones para poder obtener un procesamiento del <T,H>
import spacy
import mutual_info as mi
import time
import sys
import string

import conceptnet_lite
conceptnet_lite.connect("../OPENAI/data/conceptnet.db")
from conceptnet_lite import Label, edges_for, edges_between

nlp = spacy.load("en_core_web_md") # modelo de nlp

prueba=pd.read_csv("../OPENAI/data/"+sys.argv[1])

textos = prueba["sentence1"].to_list()       # almacenamiento en listas
hipotesis = prueba["sentence2"].to_list()

#vamos a crear un diccionario que contenga todas la relaciones de las palabras que se usan
# y las vamos a almacenar en un diccionario
rel_concept=['related_to', 
             'form_of', 
             'is_a', 
             'part_of', 
             'has_a', 
             'used_for', 
             'capable_of', 
             'at_location', 
             'entails', 
             'causes' , 
             'has_subevent', 
             'has_first_subevent', 
             'has_last_subevent', 
             'has_prerequisite', 
             'has_property', 
             'motivated_by_goal', 
             'desires', 
             'synonym', 
             'antonym', 
             'distinct_from', 
             'derived_from',
             'defined_as', 
             'manner_of', 
             'located_near', 
             'has_context', 
             'similar_to', 
             'etymologically_related_to', 
             'causes_desire',
             'made_of',
             'receives_action',
             'created_by']
rel_all_gen = dict()
rel_all_esp = dict()


inicio = time.time()
punct = string.punctuation
for i in range(len(textos)):
#for i in range(4):
    print(i)
    print(textos[i])
    print(hipotesis[i])
    lemmas_t=list(set(ut.get_lemmas_(textos[i],nlp)))
    lemmas_h=list(set(ut.get_lemmas_(hipotesis[i],nlp)))

    s1=str(textos[i]).lower()
    for c in punct:
        s1 = s1.lower().replace(c, " ")
    t_lem=s1.split()
    t_lem.extend(lemmas_t)

    s2=str(hipotesis[i]).lower()
    for c in punct:
        s2 = s2.lower().replace(c, " ")
    h_lem=s2.split()
    h_lem.extend(lemmas_h)

    print(t_lem)
    for t in t_lem:
        if t not in rel_all_gen:
            p=t
            new_i = { 'related_to': set(), 'form_of': set(), 'is_a': set(), 'part_of': set(), 'has_a': set(), 'used_for': set(), 'capable_of': set(),
                    'at_location': set(), 'entails': set(), 'causes': set() , 'has_subevent': set(), 'has_first_subevent': set(), 
                    'has_last_subevent': set(), 'has_prerequisite': set(), 'has_property': set(), 'motivated_by_goal': set(), 'desires': set(), 
                    'synonym': set(), 'antonym': set(), 'distinct_from': set(), 'derived_from': set(),'defined_as': set(), 'manner_of': set(), 'located_near': set(),
                    'has_context': set(), 'similar_to': set(), 'etymologically_related_to': set(), 'causes_desire': set(),'made_of': set(),'receives_action': set(),'created_by': set()}        
            new_d = { 'related_to': set(), 'form_of': set(), 'is_a': set(), 'part_of': set(), 'has_a': set(), 'used_for': set(), 'capable_of': set(),
                    'at_location': set(), 'entails': set(), 'causes': set() , 'has_subevent': set(), 'has_first_subevent': set(), 
                    'has_last_subevent': set(), 'has_prerequisite': set(), 'has_property': set(), 'motivated_by_goal': set(), 'desires': set(), 
                    'synonym': set(), 'antonym': set(), 'distinct_from': set(), 'derived_from': set(),'defined_as': set(), 'manner_of': set(), 'located_near': set(),
                    'has_context': set(), 'similar_to': set(), 'etymologically_related_to': set(), 'causes_desire': set(),'made_of': set(),'receives_action': set(),'created_by': set()}
            try:
                for e in edges_for(Label.get(text=p, language='en').concepts, same_language=True):
                    if e.relation.name in rel_concept:
                        if p == e.start.text:
                            new_i[e.relation.name].add(e.end.text)
                        elif p == e.end.text:
                            new_d[e.relation.name].add(e.start.text)
            except:
                pass
            rel_all_gen[p]=new_i
            rel_all_esp[p]=new_d
    print(h_lem)
    for t in h_lem:
        if t not in rel_all_gen:
            p=t
            new_i = { 'related_to': set(), 'form_of': set(), 'is_a': set(), 'part_of': set(), 'has_a': set(), 'used_for': set(), 'capable_of': set(),
                    'at_location': set(), 'entails': set(), 'causes': set() , 'has_subevent': set(), 'has_first_subevent': set(), 
                    'has_last_subevent': set(), 'has_prerequisite': set(), 'has_property': set(), 'motivated_by_goal': set(), 'desires': set(), 
                    'synonym': set(), 'antonym': set(), 'distinct_from': set(), 'derived_from': set(),'defined_as': set(), 'manner_of': set(), 'located_near': set(),
                    'has_context': set(), 'similar_to': set(), 'etymologically_related_to': set(), 'causes_desire': set(),'made_of': set(),'receives_action': set(),'created_by': set()}        
            new_d = { 'related_to': set(), 'form_of': set(), 'is_a': set(), 'part_of': set(), 'has_a': set(), 'used_for': set(), 'capable_of': set(),
                    'at_location': set(), 'entails': set(), 'causes': set() , 'has_subevent': set(), 'has_first_subevent': set(), 
                    'has_last_subevent': set(), 'has_prerequisite': set(), 'has_property': set(), 'motivated_by_goal': set(), 'desires': set(), 
                    'synonym': set(), 'antonym': set(), 'distinct_from': set(), 'derived_from': set(),'defined_as': set(), 'manner_of': set(), 'located_near': set(),
                    'has_context': set(), 'similar_to': set(), 'etymologically_related_to': set(), 'causes_desire': set(),'made_of': set(),'receives_action': set(),'created_by': set()}
            try:
                for e in edges_for(Label.get(text=p, language='en').concepts, same_language=True):
                    if e.relation.name in rel_concept:
                        if p == e.start.text:
                            new_i[e.relation.name].add(e.end.text)
                        elif p == e.end.text:
                            new_d[e.relation.name].add(e.start.text)
            except:
                pass
            rel_all_gen[p]=new_i
            rel_all_esp[p]=new_d

fin = time.time()
print("Tiempo que se llevo:",round(fin-inicio,2)," segundos")
df_diccionario = pd.DataFrame(rel_all_gen)
df_diccionario.to_pickle("salida/relaciones/"+sys.argv[1]+"Relaciones_generalesN.pickle")
df_diccionario = pd.DataFrame(rel_all_esp)
df_diccionario.to_pickle("salida/relaciones/"+sys.argv[1]+"Relaciones_especificasN.pickle")