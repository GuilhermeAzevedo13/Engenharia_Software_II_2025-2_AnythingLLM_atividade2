O código está organizado de forma sequencial e didática, seguindo cinco grandes etapas:

1. Importação de bibliotecas  
2. Definição do texto de análise  
3. Configuração do modelo de classificação Zero-Shot  
4. Definição das hipóteses (rótulos)  
5. Execução da inferência e apresentação dos resultados

Essa separação torna o código legível, extensível e adequado para análises acadêmicas ou experimentos exploratórios em Engenharia de Software e IA Aplicada.

## 

## **Bibliotecas Utilizadas**

###  **Pandas**

A biblioteca **pandas** é utilizada exclusivamente para:

* Organizar os resultados da classificação;  
* Criar tabelas estruturadas (DataFrames);  
* Facilitar a apresentação final dos scores em formato percentual.

Não há uso de pandas para análise estatística pesada, apenas para **formatação e visualização dos resultados**.

### **Transformers (Hugging Face)**

A biblioteca **transformers** fornece a abstração de alto nível chamada `pipeline`, que encapsula:

* Tokenização do texto;  
* Inferência com o modelo pré-treinado;  
* Pós-processamento dos scores de classificação.

Isso reduz drasticamente a complexidade do código e permite focar no problema conceitual em vez de detalhes de baixo nível.

O texto armazenado em `texto_analise` funciona como um **artefato documental rico**, contendo:

* Informações arquiteturais do projeto;  
* Dados sobre branches, pull requests e CI;  
* Informações históricas de releases e versionamento.

Esse texto é propositalmente não estruturado, simulando documentação real (README, relatórios técnicos ou auditorias de repositório). A escolha desse formato é essencial para demonstrar o poder da classificação Zero-Shot, que opera diretamente sobre linguagem natural.

### 

O modelo utilizado é:

**MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7**

Esse modelo pertence à família **DeBERTa v3** e foi treinado especificamente para tarefas de:

* *Natural Language Inference (NLI)*;  
* Classificação textual multilíngue;  
* Inferência semântica entre premissas e hipóteses.

Em tarefas de **NLI**, o modelo aprende a responder se uma hipótese é:

* Entailment (implicada pelo texto);  
* Contradiction (contradita pelo texto);  
* Neutral (não inferível).

A **Classificação Zero-Shot** é uma aplicação direta desse conceito: cada rótulo fornecido é tratado como uma *hipótese*, e o texto como a *premissa*.

Isso permite avaliar se o conteúdo do texto **sustenta semanticamente** cada rótulo candidato.

###  **Por que o mDeBERTa-v3 é uma excelente escolha?**

Este modelo é particularmente adequado por vários motivos:

* **Inferência lógica superior**: o DeBERTa separa explicitamente embeddings de posição e conteúdo, melhorando o raciocínio contextual.  
* **Robustez semântica**: consegue inferir conceitos implícitos, como práticas de Git, mesmo sem termos explícitos.  
* **Multilíngue**: funciona bem com textos em português e inglês, algo essencial neste código.  
* **Treinamento em larga escala (XNLI)**: foi ajustado com milhões de exemplos de inferência textual.

Em comparação, modelos puramente classificatórios falhariam sem fine-tuning específico.

### 

Na **Classificação Zero-Shot**, o modelo:

* Não recebe exemplos rotulados do problema;  
* Não é treinado novamente;  
* Trabalha apenas com descrições textuais dos rótulos.

O conhecimento vem inteiramente do pré-treinamento da LLM.

### 

O código define dois conjuntos distintos de hipóteses:

#### **Modelos de Branching**

* GitHub Flow  
* Gitflow  
* Trunk-Based Development  
* GitLab Flow

#### 

#### **Estratégias de Release**

* Semantic Versioning  
* Release Train  
* Rolling Release  
* Ad-hoc Release

Esses rótulos são propositalmente descritivos e semanticamente ricos, o que melhora a capacidade do modelo de realizar inferência correta.

Para cada rótulo, o modelo avalia:

“O texto implica que este rótulo é verdadeiro?”

O resultado é um **score de confiança**, normalizado entre 0 e 1, que representa a probabilidade relativa daquela hipótese ser suportada pelo texto.

O pipeline é chamado duas vezes:

* Uma para classificar o **modelo de branching**;  
* Outra para classificar a **estratégia de release**.

Cada chamada retorna:

* Lista ordenada de rótulos (do mais provável ao menos provável);  
* Scores associados.

A função `criar_tabela` converte os resultados brutos em um DataFrame legível, aplicando:

* Conversão de score para porcentagem;  
* Organização tabular clara;  
* Separação por categoria.

Isso torna os resultados adequados para:

* Relatórios técnicos;  
* Trabalhos acadêmicos;  
* Documentação de decisão arquitetural.

O rótulo com maior score é tratado como o **vencedor**, representando a inferência mais forte da LLM a partir do texto.

É importante destacar que:

* Os resultados são probabilísticos;  
* Pequenas diferenças de score podem indicar sobreposição conceitual;  
* A análise não substitui auditoria humana, mas fornece **forte evidência automatizada**.

  \=== MODELO DE BRANCHING \===

                 		Categoria Confiança (%)  
0              GitHub Flow        41.80%  
1  Trunk-Based Development        30.17%  
2                  Gitflow        15.99%  
3              GitLab Flow        12.04%

✅ Vencedor: GitHub Flow

\=== ESTRATÉGIA DE RELEASE \===  
             		Categoria Confiança (%)  
0        Release Train        52.39%  
1  Semantic Versioning        30.56%  
2      Rolling Release        13.56%  
3       Ad-hoc Release         3.49%

✅ Vencedor: Release Train  
