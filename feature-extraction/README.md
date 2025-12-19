# Análise de Padrões de Engenharia de Software via Classificação Zero-Shot

Este documento apresenta uma análise técnica detalhada da solução implementada em Python para realizar **classificação Zero-Shot** sobre textos técnicos de projetos de software. O objetivo é identificar automaticamente:

1. **Modelo de Fluxo de Trabalho (Branching Model)** utilizado no repositório.
2. **Estratégia de Releases** adotada pelo projeto.

A solução emprega um **Large Language Model (LLM)** especializado em **Natural Language Inference (NLI)**, utilizando a biblioteca **Hugging Face Transformers**, sem a necessidade de treinamento supervisionado adicional (fine-tuning).

---

## 🧠 Conceito: Classificação Zero-Shot

A classificação Zero-Shot é uma técnica onde um modelo é capaz de classificar textos em **rótulos nunca vistos durante o seu treinamento**, baseando-se apenas:

* No **significado semântico** do texto de entrada.
* Na **descrição textual** dos rótulos candidatos.

Nesse paradigma, o problema de classificação é reformulado como um problema de **inferência lógica**:

> *"O texto de entrada implica semanticamente a hipótese representada por este rótulo?"*

Essa abordagem elimina a necessidade de datasets rotulados manualmente, tornando-a extremamente valiosa para cenários de engenharia de software e análise de documentação técnica.

---

## 🤖 O Modelo Utilizado

O modelo selecionado para esta tarefa foi o **`MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7`**.

Trata-se de uma versão avançada do **DeBERTa v3**, treinada extensivamente para tarefas de **NLI** em múltiplos idiomas.

### Principais Características

* **Arquitetura:** Baseada em Transformer com atenção *disentangled* (separando conteúdo e posição).
* **Treinamento:** Mais de 2 milhões de exemplos NLI.
* **Suporte:** Multilíngue (incluindo Português com alta fidelidade).
* **Desempenho:** Estado da arte em tarefas Zero-Shot.

### Por que este modelo?

1. A tarefa de Zero-Shot é essencialmente NLI (decidir entre *entailment*, *neutral* ou *contradiction*).
2. O modelo consegue interpretar textos longos e técnicos, como descrições de arquitetura.
3. Mantém estabilidade de scores mesmo com múltiplos rótulos semanticamente próximos.

---

## 🛠️ Implementação Técnica

### Dependências

* `pandas`: Organização tabular dos resultados.
* `transformers`: Abstração de pipeline da Hugging Face.
* `typing`: Tipagem explícita para legibilidade.

### Carregamento do Classificador

```python
def load_zero_shot_classifier(model_name: str = "MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7"):
    return pipeline("zero-shot-classification", model=model_name)
```

Este método cria o pipeline, carrega o modelo NLI e prepara o ambiente para inferência sem necessidade de treinamento.

### Função de Classificação

```python
def classify(description, descriptions, model_name, multi_label=True):
    # ... lógica interna ...
```

**Destaque para `multi_label=True`:**

Esta configuração é fundamental. Ela permite que:

* Mais de um rótulo seja considerado semanticamente compatível.
* Os scores não precisem somar 1 (independência de probabilidade).
* O modelo avalie cada hipótese isoladamente.

Isso é necessário pois conceitos de engenharia de software frequentemente se sobrepõem (ex: GitHub Flow e Trunk-Based Development compartilham características de integração contínua).

---

## 📋 Definição das Hipóteses (Rótulos)

Para garantir precisão, os rótulos não são apenas palavras-chave, mas descrições explicativas. O modelo compara o significado da entrada com essas definições.

### Categoria 1: Modelos de Branching

* **GitHub Flow:** Caracterizado por branch única (main) e features curtas.
* **Trunk-Based Development:** Commits frequentes na main, foco em CI.
* **Gitflow:** Branches fixas (develop, master, release, hotfix).
* **GitLab Flow:** Features combinadas com branches de ambiente/versão.

### Categoria 2: Estratégias de Release

* **Semantic Versioning:** Uso de MAJOR.MINOR.PATCH.
* **Release Train:** Datas fixas e previsíveis.
* **Rolling Release:** Entregas contínuas sem versões fechadas.
* **Ad-hoc Release:** Releases manuais sem periodicidade.

---

## 📊 Resultados Obtidos

Abaixo, os resultados da inferência do modelo sobre os dados do projeto analisado.

### 1. Modelo de Branching

| Rótulo | Score (Similaridade) |
|--------|---------------------|
| GitHub Flow | 0.5341 |
| Trunk-Based Development | 0.2828 |
| Gitflow | 0.1507 |
| GitLab Flow | 0.0867 |

**Interpretação:**

Há uma forte evidência para o **GitHub Flow**. A ausência de uma branch `develop` no projeto reduziu drasticamente a probabilidade do Gitflow, enquanto a prática de integração contínua manteve o Trunk-Based como uma possibilidade secundária.

### 2. Estratégia de Release

| Rótulo | Score (Similaridade) |
|--------|---------------------|
| Release Train | 0.7988 |
| Semantic Versioning | 0.5834 |
| Rolling Release | 0.1941 |
| Ad-hoc Release | 0.0168 |

**Interpretação:**

O modelo identificou com alta confiança (~0.80) características de **Release Train**, sugerindo releases frequentes e organizadas. O **Semantic Versioning** aparece logo em seguida (~0.58), o que é coerente, pois projetos frequentemente usam Release Trains que respeitam o versionamento semântico nas suas tags.

---

## 🚀 Como Executar

1. Instale as dependências:

```bash
pip install transformers pandas torch
```

2. Execute o script Python fornecido.
3. O modelo será baixado automaticamente na primeira execução.

---

## 📝 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.