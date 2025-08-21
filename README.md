# NLI_with_LLMs_ConcepNet
Semantic Abstraction for Natural Language Inference: a Methodological Framework for Discovering and Compensating Semantic
Knowledge and Reasoning Gaps in Large Language Models

Evaluation of LLMs on the NLI task (RTEGLUE, SNLI, SciTail, SICK, Diagnostic corpora)

Meta
llama3.1:latest                	91ab477bec9d	4.7 GB	
    Model                                          
        arch            	llama 	                         
        parameters      	8.0B  	                         
        quantization    	Q4_0  	                         
        context length  	131072	                         
        embedding length	4096 
llama3.2:latest                	a80c4f17acd5	2.0 GB	
    Model                                               
        arch            	llama 	                              
        parameters      	3.2B  	                              
        quantization    	Q4_K_M	                              
        context length  	131072	                              
        embedding length	3072 
Google
gemma2:latest                  	ff02c3702f32	5.4 GB	
    Model                             
        arch            	gemma2	            
        parameters      	9.2B  	            
        quantization    	Q4_0  	            
        context length  	8192  	            
        embedding length	3584
gemma2:2b                       8ccf136fdd52    1.6 GB
    Model                             
        arch                gemma2              
        parameters          2.6B                
        quantization        Q4_0                
        context length      8192                
        embedding length    2304

Miscrosoft
phi3:medium                    	cf611a26b048	7.9 GB	
    Model                                 
        arch            	phi3  	                
        parameters      	14.0B 	                
        quantization    	Q4_0  	                
        context length  	131072	                
        embedding length	5120
phi3:latest                    	4f2222927938	2.2 GB	
    Model                                 
        arch            	phi3  	                
        parameters      	3.8B  	                
        quantization    	Q4_0  	                
        context length  	131072	                
        embedding length	3072  


Identification of relationships

First, the semantic relationships of the P-H pairs in each corpus are retrieved to reduce processing times with ConceptNet.

relationships/
    comandosRelaciones
    getRelaciones.py

Dictionaries are created for each process and corpus and then integrated into a single database
Once processed, the dictionaries are backed up
At the end, there will be two global dictionaries in 

data/
    General: wt -> wh
    Specific: wt <- wh

Random sampling of the corpora:
In order to obtain the relationships between the examples of T and H, a script must be run:
The list of commands is in commands, the reading files must be in pickle with the following columns: sentence1, sentence2, and gold_label.
The commands file contains the execution lines for processing.

Relationships_TH

This script generates pickle with the corresponding relationships: G1, G2, G3, G4, and ST.


Calls to LLMs
prompt:
The commands file contains the instructions
callsLLM.py

that generates the responses in a pickle format of the label prediction and explanation

###
In this process, it is first necessary to validate that they have all the answers from the T, H examples
because LLMs generate text that is irrelevant, or the template omits it.
Because of this, it is necessary to validate the samples and their answers so that, if any are missing, the missing answers can be requested.

In another case, the votes are generated.
Votes_groups.ipynb


##


To process this information,

processResp.ipynb

is used, which allows the performance per sample and group to be structured in dataframes.

After this, the data from the group that contributes the most is used.

# Process for validating weights for WVM, VM, RNN, Decision Tree
validation folder containing 3 samples for the final decision-making mechanism
1) validacion_respuestas_completas.ipynb
2) validacionPesos.ipynb
2) Votos_grupos.ipynb
3) RNN.ipynb



######
We conducted an experiment with direct relationships to test how well LLMs perform
when we provide them with this list without any definitions.

We are also conducting DTs with 4 groups and 3 groups. This is to measure other reasoning values.
We will add values such as entropy obtained from the tree to identify the importance of each one.
