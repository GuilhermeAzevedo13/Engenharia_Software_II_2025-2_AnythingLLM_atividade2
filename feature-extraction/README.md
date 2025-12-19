# Análise de Padrões via Embeddings Semânticos

## Visão Geral

Este documento apresenta uma análise técnica detalhada do código Python fornecido, cujo objetivo é realizar **Feature Extraction (Extração de Características)** sobre um texto técnico de projeto de software, identificando:

1. O **modelo de fluxo de trabalho de branching** utilizado no repositório
2. A **estratégia de releases** adotada pelo projeto

A solução emprega um **Small Language Model (SLM)** especializado em **Embeddings**, utilizando a biblioteca **Sentence Transformers**, para cálculo de similaridade semântica vetorial.

---

## O Conceito: Feature Extraction e Similaridade

A abordagem de Feature Extraction consiste em transformar textos em **vetores numéricos densos (embeddings)** de alta dimensão, onde o posicionamento do vetor representa o significado semântico do conteúdo. O processo se baseia em:

- **Gerar o vetor** do texto de entrada (input)
- **Gerar os vetores** das descrições dos padrões arquiteturais (dicionário)

Nesse paradigma, o problema de classificação é reformulado como um problema de **proximidade geométrica**:

> *"Qual vetor de padrão arquitetural está angularmente mais próximo do vetor do texto de entrada?"*

Essa abordagem permite comparar descrições complexas de forma matemática usando o cálculo de **Cosseno**, sendo extremamente eficiente computacionalmente.

---

## O Modelo Utilizado

O modelo utilizado é: **Qwen/Qwen3-Embedding-0.6B**

Trata-se de um modelo moderno da família **Qwen**, otimizado especificamente para tarefas de representação semântica e recuperação de informação.

### Principais Características

- Arquitetura baseada em **Transformer** (Encoder-only)
- Tamanho compacto (**0.6 Bilhões de parâmetros**), ideal para CPU
- Janela de contexto estendida (suporta textos técnicos longos)
- Treinado em **corpora multilíngue** massivos
- Estado da arte em benchmarks de MTEB (Massive Text Embedding Benchmark) para seu tamanho

### Por que este modelo?

Este modelo é especialmente indicado porque:

- A tarefa exige **compreensão profunda** de nuances técnicas
- Ele gera embeddings de alta qualidade sem a latência de modelos maiores
- Funciona nativamente com a biblioteca **sentence-transformers**
- Não exige GPU dedicada para inferência rápida

Na prática, cada padrão é convertido em uma **coordenada no espaço semântico**.

---

## Bibliotecas Utilizadas

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
```

- **sentence_transformers**: framework para carregar o modelo e gerar vetores
- **sklearn.metrics.pairwise**: utilizado para calcular a similaridade de cosseno
- **numpy**: manipulação eficiente de arrays numéricos

---

## Carregamento do Modelo

```python
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def get_embedding(text):
    return model.encode(text)
```

Este método:

- Baixa e inicializa o modelo Qwen
- Define a função auxiliar para conversão texto-vetor
- Prepara o ambiente para inferência local (offline após download)

---

## Função de Análise

```python
def analisar_categoria(nome_categoria, dicionario_padroes, embedding_input):
    # ... loop de cálculo de similaridade ...
    sim = cosine_similarity([embedding_input], [emb])[0][0]
```

Esta é a lógica central do sistema.

### Funcionamento

Recebe:
- O embedding do texto técnico (input)
- Um dicionário de padrões com suas descrições

Processa:
1. Gera os embeddings para cada descrição do dicionário
2. Calcula o Cosseno entre o vetor do input e cada vetor do dicionário
3. Retorna os padrões ordenados por score de similaridade (0 a 1)

**Interpretação do Score**: Quanto mais próximo de 1.0, mais o texto de entrada "fala sobre a mesma coisa" que a descrição do padrão.

---

## Definição dos Padrões

Cada padrão não é apenas um nome, mas uma descrição técnica completa, por exemplo:

> "GitHub Flow, caracterizado por uma única branch principal (main) e branches curtas de feature, com integração contínua via pull requests..."

Isso é crucial porque:

- O modelo compara significado, não palavras-chave exatas
- Descrições detalhadas refinam o posicionamento vetorial
- Permite diferenciar conceitos próximos (ex: Gitflow vs GitHub Flow)

---

## Resultados

### Resultado – Modelo de Branching

**Rótulos analisados:**
- GitHub Flow
- Trunk-Based Development
- Gitflow
- GitLab Flow

**Scores de Similaridade:**

```
- GitHub Flow                : 0.6881
- GitLab Flow                : 0.6808
- Gitflow                    : 0.6574
- Trunk-Based Development    : 0.6162
```

**Interpretação:**

- GitHub Flow obteve a maior similaridade vetorial (0.6881)
- A proximidade com GitLab Flow (0.6808) indica que o fluxo descrito possui características híbridas (features + releases), mas a simplicidade pendeu para o GitHub Flow
- O modelo detectou semanticamente que a ausência de develop afasta o projeto do Gitflow

### Resultado – Estratégia de Release

**Rótulos analisados:**
- Semantic Versioning
- Release Train
- Rolling Release
- Ad-hoc Release

**Top 4 estratégias mais prováveis:**

```
- Semantic Versioning : 0.5204
- Ad-hoc Release      : 0.4814
- Rolling Release     : 0.4755
- Release Train       : 0.4498
```

**Interpretação:**

- A presença de tags como v1.9.0 gerou a maior correlação com Semantic Versioning
- O score geral mais baixo (0.52) comparado ao branching sugere que o texto de entrada mistura conceitos de deploy (Docker) com versionamento, dispersando a atenção vetorial
- A baixa similaridade com Release Train indica ausência de padrões temporais fixos no texto

---

## Conclusão

A análise via embeddings semânticos demonstra ser uma abordagem robusta e eficiente para classificação de padrões arquiteturais em projetos de software, permitindo identificação automática de práticas de desenvolvimento através de similaridade vetorial, sem necessidade de regras explícitas ou keywords hardcoded.