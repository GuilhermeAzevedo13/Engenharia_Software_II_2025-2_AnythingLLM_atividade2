## 

Este documento apresenta uma análise técnica detalhada do código Python fornecido, cujo objetivo é realizar **classificação Zero-Shot** sobre um texto técnico de projeto de software, identificando:

1. O **modelo de fluxo de trabalho de branching** utilizado no repositório;  
2. A **estratégia de releases** adotada pelo projeto.

A solução emprega um **Large Language Model (LLM)** especializado em **Natural Language Inference (NLI)**, utilizando a biblioteca **Hugging Face Transformers**, sem necessidade de treinamento supervisionado adicional.

### 

A classificação Zero-Shot é uma técnica em que um modelo é capaz de classificar textos em **rótulos nunca vistos durante o treinamento específico da tarefa**, baseando-se apenas:

* No **significado semântico do texto de entrada**;  
* Na **descrição textual dos rótulos candidatos**.

Nesse paradigma, o problema de classificação é reformulado como um problema de **inferência lógica**:

*“O texto implica semanticamente a hipótese representada por este rótulo?”*

Essa abordagem elimina a necessidade de datasets rotulados, tornando-a extremamente valiosa em cenários acadêmicos, análise de documentação e engenharia de software.

### 

O modelo utilizado é:

**MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7**

Trata-se de uma versão avançada do **DeBERTa v3**, treinada extensivamente para tarefas de **Natural Language Inference (NLI)** em múltiplos idiomas.

#### **Principais características:**

* Arquitetura baseada em **Transformer**;  
* Atenção **disentangled**, separando conteúdo e posição;  
* Treinamento com **mais de 2 milhões de exemplos NLI**;  
* Suporte multilíngue (incluindo português);  
* Excelente desempenho em tarefas Zero-Shot.


  ### 

Este modelo é especialmente indicado porque:

* A tarefa de classificação Zero-Shot **é essencialmente NLI**;  
* Ele foi treinado para decidir se uma hipótese é:  
  * *entailment* (implicada),  
  * *neutral*,  
  * *contradiction*;  
* Consegue lidar com **textos longos e técnicos**, como descrições de arquitetura de software;  
* Mantém boa estabilidade de scores mesmo com múltiplos rótulos semanticamente próximos.

Na prática, cada rótulo é interpretado como uma **hipótese semântica**.

### 

import pandas as pd  
from transformers import pipeline  
from typing import Dict, Any

* pandas: utilizado apenas para organização tabular dos resultados;  
* pipeline: abstração de alto nível da Hugging Face;  
* typing: tipagem explícita para melhor legibilidade e manutenção.


  ### 

  def load\_zero\_shot\_classifier(model\_name: str \= "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"):  
      return pipeline("zero-shot-classification", model=model\_name)


Este método:

* Cria um pipeline especializado em zero-shot-classification;  
* Carrega o modelo NLI;  
* Elimina a necessidade de fine-tuning;  
* Permite reutilização em múltiplas tarefas.


  ### 

    
  def classify(description, descriptions, model\_name, multi\_label):


Esta é a função central do sistema.

#### **Funcionamento:**

1. Recebe:  
   * Um texto técnico (description);  
   * Um conjunto de rótulos com descrições (descriptions);  
2. Extrai os nomes dos rótulos como candidate\_labels;  
3. Executa o pipeline Zero-Shot;  
4. Retorna os rótulos ordenados por probabilidade.  
 


   multi\_label=True

Isso permite que:

* Mais de um rótulo seja semanticamente compatível;  
* Os scores não precisem somar 1;  
* O modelo avalie cada hipótese de forma independente.

Esse comportamento é fundamental quando conceitos são **semanticamente sobrepostos**, como:

* GitHub Flow vs Trunk-Based Development;  
* Release Train vs Semantic Versioning.

A função pretty\_print:

* Exibe o texto analisado;  
* Mostra os **Top-K rótulos mais prováveis**;  
* Estrutura os dados em um DataFrame;  
* Facilita exportação para CSV.

### 

Cada rótulo não é apenas um nome, mas uma **descrição textual clara**, por exemplo:

“GitHub Flow, caracterizado por uma única branch principal (main) e branches curtas de feature...”

Isso é crucial porque:

* O modelo compara **significado**, não palavras-chave;  
* Hipóteses bem descritas aumentam precisão;  
* Reduz ambiguidades semânticas.

Rótulos analisados:

* GitHub Flow  
* Trunk-Based Development  
* Gitflow  
* GitLab Flow

Todos são conceitos próximos, o que torna a tarefa um excelente exemplo de classificação semântica complexa.

### 

Rótulos analisados:

* Semantic Versioning  
* Release Train  
* Rolling Release  
* Ad-hoc Release

Essas estratégias frequentemente coexistem, justificando novamente o uso de **multi-label**.

                         \- GitHub Flow                    : 0.5341  
 		 \- Trunk-Based Development        : 0.2828  
  		\- Gitflow                        : 0.1507  
 \- GitLab Flow                    : 0.0867

**Interpretação**:

* Forte evidência de **GitHub Flow**;  
* Ausência de branch develop reduz probabilidade de Gitflow;  
* CI intenso e branches curtas justificam proximidade com Trunk-Based Development.


  ### 

  ### 

  ### 

  ### 

  ### 

  ### **6.2 Resultado – Estratégia de Release**

  ### Top 4 estratégias mais prováveis (label : score):

  ### 

  ###   \- Release Train                  : 0.7988

  ###   \- Semantic Versioning            : 0.5834

  ###   \- Rolling Release                : 0.1941

  ###   \- Ad-hoc Release                 : 0.0168

  ### 

  ### 

* Releases frequentes e organizadas sugerem Release Train;  
* Uso explícito de tags SemVer reforça Semantic Versioning;  
* Baixa evidência de Rolling ou Ad-hoc releases.


  

