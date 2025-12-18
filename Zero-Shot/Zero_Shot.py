import pandas as pd
from transformers import pipeline
from typing import Dict, Any

def load_zero_shot_classifier(model_name: str = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"):
    """
    Carrega o modelo zero-shot-classification (sem necessidade de treino).
    """
    return pipeline("zero-shot-classification", model=model_name)

# ===============================================================
# 🔹 Função de classificação por similaridade semântica
# ===============================================================
def classify_architecture(description: str,
                          architecture_descriptions: Dict[str, str],
                          model_name: str = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
                          multi_label: bool = True) -> Dict[str, Any]:
    """
    Usa zero-shot-classification para identificar qual arquitetura o texto mais descreve.
    """
    classifier = load_zero_shot_classifier(model_name)
    candidate_labels = list(architecture_descriptions.keys())

    result = classifier(description, candidate_labels, multi_label=multi_label)
    labels_scores = list(zip(result["labels"], result["scores"]))
    labels_scores = sorted(labels_scores, key=lambda x: x[1], reverse=True)

    return {
        "sequence": result.get("sequence", description),
        "labels_scores": labels_scores
    }
def pretty_print(result: Dict[str, Any], top_k: int = 6):
    print("\nTexto analisado:\n", result["sequence"][:600], "...\n")
    print(f"Top {top_k} estratégias mais prováveis (label : score):\n")
    lista = []
    for label, score in result["labels_scores"][:top_k]:
        print(f"  - {label:<30} : {score:.4f}")
        lista.append({
            "label": label,
            "score": score
        })
    df = pd.DataFrame(data=lista)
    #df.to_csv('Zero-Shot.csv', index=False)

# ==========================================
# PASSO 2: Configuração do Modelo e do Texto
# ==========================================

# O texto técnico do projeto AnythingLLM (Fornecido no prompt)
texto_analise = """
Com base nos dados técnicos e estatísticos abaixo sobre o projeto open source "AnythingLLM", 
identifique e justifique:
1. Qual é o Modelo de Fluxo de Trabalho (Branching Model) utilizado (ex: Gitflow, GitHub Flow, 
Trunk-Based Development)?
2. Qual é a Estratégia de Releases utilizada (ex: Versionamento Semântico, Release Train, Rolling 
Release)?
✷ Visão Geral do Projeto
• Nome: Mintplex-Labs/anything-llm.
• Descrição: Aplicação "all-in-one" de IA para Desktop e Docker, focada em RAG (Retrieval Augmented 
Generation).
• Arquitetura: Monorepo contendo Frontend (ViteJS/React), Server (NodeJS), Collector e configurações de 
Docker.
• Linguagem Dominante: JavaScript (98%).
✷ Dados sobre Branches e Fluxo de Trabalho (Branching)
• Estrutura de Branches: O repositório possui cerca de 67 branches, sendo 24 ativas. A maioria segue o 
padrão de nomenclatura convencional: feat/...,bug/...,refactor/....
• Ausência de Branch "Develop": Não foi identificada uma branch intermediária fixa chamada develop. 
As alterações ocorrem em branches temporárias e são mescladas diretamente na branch principal 
(master ou main).
• Integração e Code Review:
◦ O uso de Pull Requests (PRs) é mandatório e intenso: houve 58 PRs mesclados em um período de 30 
dias (15/nov a 15/dez).
◦ Existem templates de contribuição (pull_request_template.md e CONTRIBUTING.md).
◦ A integração na branch principal é controlada: apenas 5 autores realizaram commits diretos na main, 
enquanto 58 commits ocorreram via merge de branches auxiliares.
• Automação (CI): Todas as branches analisadas passam por verificações automáticas de testes (CI via 
GitHub Actions), garantindo integridade antes do merge.
✷ Dados sobre Releases e Entrega
• Versionamento: O projeto utiliza tags no formato de Versionamento Semântico (ex: v1.9.0, v1.9.1),.
• Artefatos de Entrega: O software não é apenas um serviço web, mas gera binários instaláveis para 
Desktop (Windows, Mac, Linux) e Imagens Docker,.
• Histórico: O projeto contabiliza mais de 21 releases registradas no GitHub.
• Gestão de Mudanças: As releases parecem ser isoladas pontualmente em branches específicas ou 
tags para garantir estabilidade sem travar o desenvolvimento paralelo na branch principal.
"""

# Carregando o pipeline de Zero-Shot Classification
# Usamos o 'facebook/bart-large-mnli' pois ele é excelente em inferência lógica (NLI)
print("Carregando modelo Zero-Shot (pode demorar alguns segundos)...")


# ==========================================
# PASSO 3: Definição das Hipóteses (Rótulos)
# ==========================================

# ==========================================
# PASSO 3: Definição das Hipóteses (Rótulos)
# ==========================================

# Modelos de Branching com descrições explícitas (hipóteses NLI)
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


# Estratégias de Release com descrições explícitas



# ==========================================
# PASSO 4: Execução da Análise
# ==========================================

print("Analisando o texto...")

result = classify_architecture(texto_analise, BRANCHING_DESCRIPTIONS)
lista = []
lista.append(result["sequence"])
print(lista)
pretty_print(result, top_k=4)
result = classify_architecture(texto_analise, RELEASE_STRATEGY_DESCRIPTIONS)
lista = []
lista.append(result["sequence"])
print(lista)
pretty_print(result, top_k=4)