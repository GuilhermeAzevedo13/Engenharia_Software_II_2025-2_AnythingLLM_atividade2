from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Inicialização do modelo
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def get_embedding(text):
    return model.encode(text)

# --- Dicionários de Padrões ---

BRANCHING_DESCRIPTIONS = {
    "GitHub Flow": (
         "GitHub Flow, caracterizado por uma única branch principal (main) e branches curtas de feature, "
         "com integração contínua via pull requests"
    ),

    "Gitflow": (
         "Gitflow, caracterizado pelo uso de branches fixas como develop, master, release e hotfix, "
         "com ciclos de desenvolvimento bem definidos"
    ),

    "Trunk-Based Development": (
        "Trunk-Based Development, caracterizado por commits frequentes diretamente na branch principal "
        "ou em branches de vida muito curta, com forte uso de CI"
    ),

    "GitLab Flow": (
        "GitLab Flow, caracterizado pela combinação de branches de feature com branches específicas "
        "por ambiente ou versão"
    ),
}

RELEASE_STRATEGY_DESCRIPTIONS = {
    "Semantic Versioning": (
        "Semantic Versioning, caracterizado pelo uso de versões no formato MAJOR.MINOR.PATCH, "
        "indicando compatibilidade e tipo de mudança"
    ),

    "Release Train": (
        "Release Train, caracterizado por releases em datas fixas e previsíveis, "
        "independentemente do volume de mudanças"
    ),

    "Rolling Release": (
        "Rolling Release, caracterizado por entregas contínuas sem versões bem definidas, "
        "onde o software está sempre sendo atualizado"
    ),

    "Ad-hoc Release": (
        "Ad-hoc Release, caracterizado por releases manuais e pontuais, "
        "sem periodicidade fixa ou estratégia formal"
    ),
}

# --- Entrada de Texto para Análise ---
entrada = """
Com base nos dados técnicos e estatísticos abaixo sobre o projeto open source "AnythingLLM", identifique e justifique:
1. Qual é o Modelo de Fluxo de Trabalho (Branching Model) utilizado (ex: Gitflow, GitHub Flow, Trunk-Based Development)?
2. Qual é a Estratégia de Releases utilizada (ex: Versionamento Semântico, Release Train, Rolling Release)?

# Visão Geral do Projeto

• Nome: Mintplex-Labs/anything-llm.  
• Descrição: Aplicação "all-in-one" de IA para Desktop e Docker, focada em RAG (Retrieval Augmented Generation).  
• Arquitetura: Monorepo contendo Frontend (ViteJS/React), Server (NodeJS), Collector e configurações de Docker.  
• Linguagem Dominante: JavaScript (98%).

# Dados sobre Branches e Fluxo de Trabalho (Branching)

• Estrutura de Branches: O repositório possui cerca de 67 branches, sendo 24 ativas. A maioria segue o
padrão de nomenclatura convencional: feat/...,bug/...,refactor/....  
• Ausência de Branch "Develop": Não foi identificada uma branch intermediária fixa chamada develop.
As alterações ocorrem em branches temporárias e são mescladas diretamente na branch principal (master).  
• Integração e Code Review:  
    ◦ O uso de Pull Requests (PRs) é mandatório e intenso: houve 58 PRs mesclados em um período de 30 dias (15/nov a 15/dez).  
    ◦ Existem templates de contribuição (pull_request_template.md e CONTRIBUTING.md).  
    ◦ A integração na branch principal é controlada: apenas 5 autores realizaram commits diretos na main, enquanto 58 commits ocorreram via merge de branches auxiliares.  
• Automação (CI): Todas as branches analisadas passam por verificações automáticas de testes (CI via
GitHub Actions), garantindo integridade antes do merge.

# Dados sobre Releases e Entrega

• Versionamento: O projeto utiliza tags no formato de Versionamento Semântico (ex: v1.9.0, v1.9.1),.  
• Artefatos de Entrega: O software não é apenas um serviço web, mas gera binários instaláveis para Desktop (Windows, Mac, Linux) e Imagens Docker,.  
• Histórico: O projeto contabiliza mais de 21 releases registradas no GitHub.  
• Gestão de Mudanças: As releases parecem ser isoladas pontualmente em branches específicas ou tags para garantir estabilidade sem travar o desenvolvimento paralelo na branch principal.
"""

print("Gerando embeddings da entrada...\n")
emb_entrada = get_embedding(entrada)

# --- Função de Análise Genérica ---
def analisar_categoria(nome_categoria, dicionario_padroes, embedding_input):
    print(f"--- Analisando: {nome_categoria} ---")
    
    # Gera embeddings para o dicionário atual
    emb_padroes = {k: get_embedding(v) for k, v in dicionario_padroes.items()}
    
    resultados = []
    for nome, emb in emb_padroes.items():
        # Calcula similaridade
        sim = cosine_similarity([embedding_input], [emb])[0][0]
        resultados.append((nome, sim))
    
    # Ordena e exibe
    resultados.sort(key=lambda x: x[1], reverse=True)
    
    for nome, score in resultados:
        print(f"{nome:25s} -> Similaridade: {score:.4f}")
    
    print(f"\n>> Padrão mais provável para {nome_categoria}: {resultados[0][0]}\n")
    return resultados[0][0]

# --- Execução das Análises ---

# 1. Análise de Branching
analisar_categoria("Modelos de Branching", BRANCHING_DESCRIPTIONS, emb_entrada)

# 2. Análise de Release
analisar_categoria("Estratégias de Release", RELEASE_STRATEGY_DESCRIPTIONS, emb_entrada)