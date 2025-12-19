from FlagEmbedding import FlagReranker
import os

reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

textos = []
for nome_arquivo in ["branches_overview.txt", "branches_recent_commits_sample.txt", "dataset.jsonl", "tags_timeline.txt", "git_describe.txt"]:
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            textos.append(f.read())

entrada = "\n".join(textos)

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

print("🔍 Analisando estratégias de branching e release com base nos arquivos de log...\n")

# Análise 1: Estratégias de Branching
print("=" * 60)
print("📊 ANÁLISE 1: ESTRATÉGIAS DE BRANCHING")
print("=" * 60 + "\n")

scores_branching = {}
for nome, descricao in BRANCHING_DESCRIPTIONS.items():
    score = reranker.compute_score([[entrada, descricao]])
    scores_branching[nome] = float(score[0]) if isinstance(score, (list, tuple)) else float(score)

ordenado_branching = sorted(scores_branching.items(), key=lambda x: x[1], reverse=True)

print("🏁 Resultado de similaridade das estratégias de branching:\n")
for i, (nome, valor) in enumerate(ordenado_branching, start=1):
    print(f"{i}. {nome:30} -> Similaridade: {valor:.4f}")

melhor_branching = ordenado_branching[0][0]
print(f"\n🔮 Estratégia de branching mais provável: {melhor_branching.upper()}")

# Análise 2: Estratégias de Release
print("\n" + "=" * 60)
print("📊 ANÁLISE 2: ESTRATÉGIAS DE RELEASE")
print("=" * 60 + "\n")

scores_release = {}
for nome, descricao in RELEASE_STRATEGY_DESCRIPTIONS.items():
    score = reranker.compute_score([[entrada, descricao]])
    scores_release[nome] = float(score[0]) if isinstance(score, (list, tuple)) else float(score)

ordenado_release = sorted(scores_release.items(), key=lambda x: x[1], reverse=True)

print("🏁 Resultado de similaridade das estratégias de release:\n")
for i, (nome, valor) in enumerate(ordenado_release, start=1):
    print(f"{i}. {nome:30} -> Similaridade: {valor:.4f}")

melhor_release = ordenado_release[0][0]
print(f"\n🔮 Estratégia de release mais provável: {melhor_release.upper()}")

print("\n" + "=" * 60)
print("📋 RESUMO FINAL")
print("=" * 60)
print(f"Branching: {melhor_branching}")
print(f"Release:   {melhor_release}")
print("=" * 60)
