import requests
import json
import random
import time
import pickle
import pandas as pd
import sys

ruta="salida/finales/"+str(sys.argv[3])
corpus=["1","2","3","4","5","6","7","8","9","10"]

definitions=["Group 1 (G1): These relations usually correspond to Entailment.",
            "Group 2 (G2): These relations often indicate Contradiction.",
            "Group 3 (G3): These relations typically correspond to Neutral.",
            "Group 4 (G4): These relations are not identified."]

definitionsE=["Group 1 (G1): Triplets of Generality. These relations usually correspond to Entailment. triplets: (ti,rel,hj) where ti is in Text, hj is in Hypothesis and rel is the relation between ti an hj. e.g., (dog,is_a,animal) dog is in T, animal is in H and relation is general between dog - animal.",
        "Group 2 (G2): Triplets of Contradictory. These often indicate Contradiction. triplets: (ti,rel,hj) where ti is in Text, hj is in Hypothesis and rel is the relation between ti an hj. e.g., (dog,distinct_from,cat) dog is in T, cat is in H and relation is distinct_from between dog - cat.",
        "Group 3 (G3): Triplets of Contextuality. These typically correspond to Neutral. triplets: (ti,rel,hj) where ti is in Text, hj is in Hypothesis and rel is the relation between ti an hj. e.g., (human,relate_to,dog) animal is in T, dog is in H and relation is contextual between human - dog.",
        "Group 4 (G4): Relations not identified or categorized."]

gs=["G1","G2","G3","G4"]

grupos=["ConteosG1","ConteosG2","ConteosG3","ConteosG4"]

# modelo y donde se almacena los resultados
model1 = sys.argv[1]
muestreos=int(sys.argv[2])
salida="LLMs/"+str(sys.argv[1])+"/"+str(sys.argv[3])

####

print("INICIA TODAS LAS RELACIONES")

inicio = time.time()

lista_respuestasOllama=[]
for c in range(muestreos):
    df_t=pd.read_pickle(ruta+str(c+1)+".pickle")
    lista_respuestasOllama=[]
    for index,strings in df_t.iterrows():
        #print(strings["sentence1"],strings["sentence2"],strings['gold_label'])
        prompt = '''
        You are an expert in Recognition of Textual Entailment over pairs of Text and Hypothesis.
        Based on the information provided below, classify the relationship between the given Text and Hypothesis as one of the following: "Entailment", "Neutral", or "Contradiction" and give an explanation. Respond only using the template:
        {
            "Answer": "",
            "Explanation":""
        }
        Do not modify the template.

        Text and Hypothesis to Classify:
            Text: '''+strings["Texto"]+'''
            Hypothesis: '''+ strings["Hipotesis"]+'''
            
        Relations:
            '''+str(strings["ConteosR"])+'''

        Use the information provided to classify the relationship and give an explanation.'''
    
        # print(prompt)
        # break
        data = {
            "prompt": prompt,
            "model": model1,
            "format": "json",
            "stream": False,
            "options": {"temperature": 0},
        }
        try:
            response = requests.post("http://localhost:11434/api/generate", json=data, stream=False,timeout=90)        
            json_data = json.loads(response.text)
            lista_respuestasOllama.append(json.dumps(json.loads(json_data["response"]), indent=2))
            print(index)
        except:
            print("Saltó",index,c)
            lista_respuestasOllama.append("NA")
        
    with open(salida+"ritST_"+str(c+1)+".pickle", "wb") as f:
        pickle.dump(lista_respuestasOllama, f)
    #time.sleep(300)

fin = time.time()
print("Tiempo que se llevo:",round(fin-inicio,2)," segundos")

inicio = time.time()

lista_respuestasOllama=[]
for c in range(muestreos):
    df_t=pd.read_pickle(ruta+str(c+1)+".pickle")
    for f_ in range(len(definitions)):
        lista_respuestasOllama=[]
        for index,strings in df_t.iterrows():
            #print(strings["sentence1"],strings["sentence2"],strings['gold_label'])
            prompt = '''
            You are an expert in Recognition of Textual Entailment over pairs of Text and Hypothesis.
            Based on the information provided below, classify the relationship between the given Text and Hypothesis as one of the following: "Entailment", "Neutral", or "Contradiction" and give an explanation. Respond only using the template:
            {
                "Answer": "",
                "Explanation":""
            }
            Do not modify the template.

            Background Information:
            
                Word Relationship Groups:
                    '''+str(definitionsE[f_])+'''

            Text and Hypothesis to Classify:
                Text: '''+strings["Texto"]+'''
                Hypothesis: '''+ strings["Hipotesis"]+'''
                
            Relations:
                '''+str(gs[f_])+''' : '''+str(strings[grupos[f_]])+'''                    

            Use the information provided to classify the relationship and give an explanation.'''
        
            #print(prompt)
            data = {
                "prompt": prompt,
                "model": model1,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0},
            }
            try:
                response = requests.post("http://localhost:11434/api/generate", json=data, stream=False,timeout=90)        
                json_data = json.loads(response.text)
                lista_respuestasOllama.append(json.dumps(json.loads(json_data["response"]), indent=2))
                print(index)
            except:
                print("Saltó",index,c)
                lista_respuestasOllama.append("NA")
            
        with open(salida+"rit_"+str(c+1)+"_"+str(gs[f_])+".pickle", "wb") as f:
            pickle.dump(lista_respuestasOllama, f)
        time.sleep(300)
    
fin = time.time()
print("Tiempo que se llevo:",round(fin-inicio,2)," segundos")
