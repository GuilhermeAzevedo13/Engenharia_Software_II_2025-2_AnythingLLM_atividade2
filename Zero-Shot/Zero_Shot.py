import pandas as pd
from transformers import pipeline

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
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7")

# ==========================================
# PASSO 3: Definição das Hipóteses (Rótulos)
# ==========================================

# Quais modelos de Branching queremos testar?
labels_branching = [
    "GitHub Flow",               # Fluxo simples, master + features
    "Gitflow",                   # Fluxo complexo, develop + master + release branches
    "Trunk-Based Development",   # Fluxo rápido, commits diretos na main ou branches curtas
    "GitLab Flow"                # Variação com branches de ambiente
]

# Quais estratégias de Release queremos testar?
labels_release = [
    "Semantic Versioning",       # Versionamento baseado em SemVer (v1.0.0)
    "Release Train",             # Releases em datas fixas (ex: toda terça)
    "Rolling Release",           # Atualização contínua sem versões fixas
    "Ad-hoc Release"             # Releases manuais sob demanda
]

# ==========================================
# PASSO 4: Execução da Análise
# ==========================================

print("Analisando o texto...")

# Classificação do Fluxo de Trabalho
result_branch = classifier(texto_analise, labels_branching)

# Classificação da Estratégia de Release
result_release = classifier(texto_analise, labels_release)

# ==========================================
# PASSO 5: Apresentação dos Resultados
# ==========================================

# Função auxiliar para criar DataFrames bonitos
def criar_tabela(resultado, categoria):
    df = pd.DataFrame({
        'Categoria': resultado['labels'],
        'Confiança (Score)': result_branch['scores'] if categoria == 'Branching' else result_release['scores']
    })
    # Formata para porcentagem
    df['Confiança (%)'] = (df['Confiança (Score)'] * 100).map('{:.2f}%'.format)
    return df[['Categoria', 'Confiança (%)']]

# Exibindo Tabela de Branching
print("\n=== RESULTADO 1: MODELO DE BRANCHING ===")
df_branch = criar_tabela(result_branch, 'Branching')
print(df_branch)
print(f"\n✅ Vencedor: {result_branch['labels'][0]}")

# Exibindo Tabela de Release
print("\n=== RESULTADO 2: ESTRATÉGIA DE RELEASE ===")
df_release = criar_tabela(result_release, 'Release')
print(df_release)
print(f"\n✅ Vencedor: {result_release['labels'][0]}")