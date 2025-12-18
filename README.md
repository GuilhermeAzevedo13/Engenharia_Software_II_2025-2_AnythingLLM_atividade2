# Dataset de Estratégia de Branches e Releases

Este repositório utiliza um script em Python para extrair informações essenciais do histórico Git, com o objetivo de **identificar e analisar**:

- a **estratégia de branches** (modelo de fluxo de trabalho, ex.: GitHub Flow, Gitflow);
- a **estratégia de releases** (ex.: Rapid Releases, Release Train, LTS + Current).

Os dados extraídos são utilizados como entrada para **modelos de linguagem (LLMs)** da plataforma **Hugging Face**, permitindo comparar as análises produzidas por diferentes modelos.

---

## 📌 Visão geral da abordagem

A análise parte da seguinte premissa:

- **Estratégia de Releases** → inferida a partir de **tags** e de sua cadência temporal (*ritmo de entrega*).
- **Modelo de Fluxo de Trabalho (Branching Model)** → inferido a partir do padrão de **branches** e **commits recentes** (*organização do código*).

O script gera um dataset **estruturado e enxuto**, evitando excesso de dados e favorecendo inferências consistentes.

---

## 📦 Pré-requisitos

Antes de executar o script, certifique-se de ter:

- **Git** instalado  
```bash
git --version
```

- **Python 3.9+**  
```bash
python --version
```

---

## 📥 Clonando o repositório

Caso ainda não tenha o projeto localmente:

```bash
git clone https://github.com/Mintplex-Labs/anything-llm.git
cd anything-llm
```

---

## 🔄 Atualizando branches remotas (passo essencial)

Para que o script consiga identificar corretamente o **modelo de fluxo de trabalho**, é necessário buscar as **branches remotas** do repositório:

```bash
git fetch --all --prune
```

Verifique se as branches remotas estão visíveis:

```bash
git branch -r
```

---

## 🧾 Script de extração

O script responsável pela extração dos dados chama-se:

```
DataSet_extractor.py
```

Sugestão de organização no projeto:

```
scripts/
 └── DataSet_extractor.py
```

---

## ⚙️ Configuração do script

### 1️⃣ Identificador do repositório

Para evitar referências ao caminho local da máquina, o identificador do repositório é fixado no script.

No arquivo `DataSet_extractor.py`, ajuste o método abaixo:

```python
def _repo_id(self) -> str:
    return "github.com/Mintplex-Labs/anything-llm"
```

Isso garante que o dataset seja **portável** e adequado para análise acadêmica.

---

### 2️⃣ Ajuste do caminho do repositório local (**obrigatório**)

No bloco `main` do script, **verifique e ajuste o caminho do repositório local**:

```python
if __name__ == "__main__":
    REPO = r"."  # caminho do repositório local
    N_COMMITS_PER_BRANCH = 10

    extractor = GitStrategyExtractorEssential(
        repo_path=REPO,
        output_dir="git_strategy_output",
        recent_commits_per_branch=N_COMMITS_PER_BRANCH
    )
    extractor.extract_all()
```

**Observações importantes:**
- Use `REPO = "."` se o script estiver sendo executado a partir da raiz do projeto.
- Caso contrário, informe o caminho relativo ou absoluto correto.
- Um caminho incorreto impedirá a leitura de branches, commits e tags.

---

### 3️⃣ Quantidade de commits por branch

O parâmetro `N_COMMITS_PER_BRANCH` define o tamanho da amostragem utilizada para inferir padrões de fluxo:

```python
N_COMMITS_PER_BRANCH = 10
```

Recomendação:
- **5 a 10 commits** por branch são suficientes para capturar padrões sem gerar ruído excessivo.

---

## ▶️ Execução do script

Com o terminal aberto na raiz do projeto, execute:

```bash
python scripts/DataSet_extractor.py
```

---

## 📂 Arquivos gerados

Após a execução, será criada a pasta:

```
git_strategy_output/
```

Conteúdo principal:

### 🔹 `dataset.jsonl`
Dataset estruturado (formato JSONL), utilizado como entrada para os modelos de linguagem.

Cada linha representa um registro independente, por exemplo:
- visão geral de uma branch
- amostra de commit
- informação de tag (release)

---

### 🔹 `branches_overview.txt`
Visão geral das branches (locais e remotas), incluindo:
- nome da branch
- data do último commit
- autor
- mensagem do commit

---

### 🔹 `branches_recent_commits_sample.txt`
Amostra dos últimos *N* commits por branch, utilizada para inferir:
- padrão de trabalho
- integração no tronco
- granularidade das mudanças

---

### 🔹 `tags_timeline.txt`
Histórico de tags do projeto, representando as **releases** e sua cadência temporal.

---

### 🔹 `git_describe.txt`
Indica a posição atual do código em relação à última release, permitindo avaliar:
- frequência de releases
- distância entre entregas

---

## 🤖 Uso do dataset com modelos de linguagem

O arquivo `dataset.jsonl` deve ser fornecido **igualmente** a pelo menos **três modelos de linguagem distintos** na plataforma Hugging Face para:

1. Identificar a **estratégia de releases** adotada pelo projeto.
2. Identificar o **modelo de fluxo de trabalho (branching model)**.
3. Justificar as conclusões com base nos dados observados.
4. Comparar os resultados entre os modelos utilizados.

---

## 📊 Resultado esperado

A partir da análise, espera-se conseguir classificar:

- **Estratégia de Releases**  
  (ex.: Rapid Releases, Release Train, LTS + Current)

- **Modelo de Fluxo de Trabalho**  
  (ex.: GitHub Flow, Gitflow, Trunk-Based Development)

Com justificativas fundamentadas nos dados extraídos do repositório.
