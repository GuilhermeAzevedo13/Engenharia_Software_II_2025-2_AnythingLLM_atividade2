# Tutorial — Identificando Estratégias de Branching e Release usando `text-classification` (BAAI/bge-reranker-v2-m3)

Este tutorial explica, passo a passo, como identificar a **estratégia de branching** e a **estratégia de release** de um projeto Git.  
O método escolhido foi **text-classification** com um *reranker* (modelo `BAAI/bge-reranker-v2-m3`) que compara os textos dos arquivos de histórico Git com descrições de estratégias conhecidas e retorna um score de similaridade.  

> 💡 **Importante:** todos os arquivos `.txt` (ex.: `branches_overview.txt`, `branches_recent_commits_sample.txt`, `dataset.jsonl`, `tags_timeline.txt`, `git_describe.txt`) **devem estar na mesma pasta** onde você executa o script — o script lê todos esses arquivos localmente.

---

## 🧭 1. Resumo do processo

1. Escolher a *task* **text-classification** no Hugging Face.  
2. Usar o modelo **BAAI/bge-reranker-v2-m3** — um reranker de similaridade textual.  
3. Escrever descrições resumidas de estratégias de branching (GitHub Flow, Gitflow, Trunk-Based Development, GitLab Flow) e estratégias de release (Semantic Versioning, Release Train, Rolling Release, Ad-hoc Release).  
4. Usar como entrada os arquivos de histórico Git (branches, commits, tags etc.).  
5. O script analisa o conteúdo dos arquivos e calcula a similaridade entre o histórico do projeto e cada descrição de estratégia.  
6. O resultado indica quais estratégias de branching e release são mais compatíveis com o projeto.

---

## ⚙️ 2. Por que o modelo `BAAI/bge-reranker-v2-m3`?

- Modelos **reranker** são feitos para comparar dois textos e medir o quanto eles se relacionam.  
- No caso, queremos saber **qual descrição de estratégia se parece mais com o histórico do projeto**.  
- O modelo `bge-reranker-v2-m3` é uma escolha sólida por ser relativamente leve e eficiente em tarefas de similaridade textual.

---

## 📉 3. Por que os valores de similaridade são negativos?

Os scores retornados aparecem como:

GitHub Flow -> Similaridade: -8.8984
Gitflow -> Similaridade: -7.1562
Trunk-Based Development -> Similaridade: -6.5430


Isso é **normal**.  
O reranker **não retorna probabilidades (0–1)**, e sim **valores de logit** — números reais (positivos ou negativos) que representam relevância.  
Eles **não devem ser interpretados literalmente**: apenas comparados entre si.

👉 **Quanto maior o valor (menos negativo), mais compatível o par de textos.**  
Por exemplo:  
`-6.5` indica mais compatibilidade do que `-9.2`.

---

## 🧰 4. Instalação dos pacotes necessários

No terminal, instale as dependências com:

```bash
pip3 install FlagEmbedding torch
```

## 📂 5. Estrutura esperada de arquivos
/meu_projeto/

├── branches_overview.txt

├── branches_recent_commits_sample.txt

├── dataset.jsonl

├── tags_timeline.txt

├── git_describe.txt

└── text-classification.py

## 6 — Como executar o script

1. Abra o terminal e navegue até a pasta que contém o script `text-classification.py` e os arquivos `.txt`.

2. Garanta que as dependências estejam instaladas:
    ```bash
    pip3 install FlagEmbedding torch
    ```

3. Execute o script
    ```bash
    python3 text-classification.py
    ```
4. Observações:

    Na primeira execução o modelo será baixado (pode levar alguns minutos).

    Certifique-se de que todos os arquivos de histórico Git estejam na mesma pasta do script.

### Exemplo de saída:

============================================================
📊 ANÁLISE 1: ESTRATÉGIAS DE BRANCHING
============================================================

🏁 Resultado de similaridade das estratégias de branching:

1. GitHub Flow                  -> Similaridade: -5.5664
2. Gitflow                      -> Similaridade: -5.7656
3. Trunk-Based Development      -> Similaridade: -6.2383
4. GitLab Flow                  -> Similaridade: -6.6836

🔮 Estratégia de branching mais provável: GITHUB FLOW

============================================================
📊 ANÁLISE 2: ESTRATÉGIAS DE RELEASE
============================================================

🏁 Resultado de similaridade das estratégias de release:

1. Semantic Versioning          -> Similaridade: -6.1234
2. Rolling Release              -> Similaridade: -7.2456
3. Release Train                -> Similaridade: -7.8123
4. Ad-hoc Release               -> Similaridade: -8.3456

🔮 Estratégia de release mais provável: SEMANTIC VERSIONING

============================================================
📋 RESUMO FINAL
============================================================
Branching: GitHub Flow
Release:   Semantic Versioning
============================================================

## Interpretação do resultado

O modelo realiza **duas análises independentes**:

1. **Estratégia de Branching**: Compara o histórico de branches com descrições de GitHub Flow, Gitflow, Trunk-Based Development e GitLab Flow.
2. **Estratégia de Release**: Compara as tags e versões com descrições de Semantic Versioning, Release Train, Rolling Release e Ad-hoc Release.

Em cada análise, o score mais alto (menos negativo) indica a estratégia mais compatível.

Nesse exemplo, o projeto foi identificado como usando **GitHub Flow** para branching e **Semantic Versioning** para release.

**Os valores negativos não representam erro, apenas a forma interna de cálculo do modelo.**