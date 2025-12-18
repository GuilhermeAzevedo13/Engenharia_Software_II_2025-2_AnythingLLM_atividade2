# Engenharia_Software_II_2025-2_AnythingLLM_atividade2
Atividade 2 de Engenharia de Software

Gerando o dataset de branches e releases

Este projeto utiliza um script em Python para extrair informações essenciais do repositório Git e gerar um dataset estruturado (dataset.jsonl) para análise da estratégia de branches e da estratégia de releases com modelos de linguagem.



1) Clonar o repositório

Caso ainda não tenha o projeto localmente:

git clone https://github.com/Mintplex-Labs/anything-llm.git
cd anything-llm

2) Atualizar as referências do repositório remoto

Este passo é importante para que o script consiga identificar branches remotas, que são fundamentais para inferir o modelo de fluxo de trabalho (branching model).

git fetch --all --prune


Você pode conferir as branches remotas com:

git branch -r

3) Posicionar o script no projeto

Crie o arquivo abaixo no projeto:

scripts/DataSet_extractor.py


Cole nele o código do extrator fornecido neste trabalho.

4) Configurar o identificador do repositório

No arquivo DataSet_extractor.py, ajuste o método _repo_id() para garantir que o dataset seja portável e independente do caminho local:

def _repo_id(self) -> str:
    return "github.com/Mintplex-Labs/anything-llm"

5) Ajustar os parâmetros de execução

No final do arquivo DataSet_extractor.py, configure:

O caminho do repositório (REPO)

A quantidade de commits por branch utilizada como amostragem

Exemplo:

REPO = r"."
N_COMMITS_PER_BRANCH = 10


Observação: valores entre 5 e 10 commits por branch são suficientes para capturar padrões de fluxo sem gerar excesso de dados.

6) Executar o script

Com o terminal aberto na raiz do projeto, execute:

python scripts/DataSet_extractor.py

7) Arquivos gerados

Após a execução, será criada a pasta:

git_strategy_output/


Principais arquivos:

dataset.jsonl
Dataset estruturado (JSONL) utilizado como entrada para os modelos de linguagem.

branches_overview.txt
Visão geral das branches (locais e remotas), incluindo data e mensagem do último commit.

branches_recent_commits_sample.txt
Amostra dos últimos N commits por branch, utilizada para inferir o modelo de fluxo de trabalho.

tags_timeline.txt
Histórico de tags, representando as releases do projeto.

git_describe.txt
Indica a posição atual do código em relação à última release.

8) Uso do dataset na análise com modelos de linguagem

O arquivo dataset.jsonl deve ser fornecido igualmente a pelo menos três modelos de linguagem diferentes na plataforma Hugging Face para:

Identificar a estratégia de releases adotada pelo projeto.

Identificar o modelo de fluxo de trabalho (branching model).

Justificar as conclusões com base nos dados observados.

Comparar os resultados obtidos entre os modelos selecionados.
