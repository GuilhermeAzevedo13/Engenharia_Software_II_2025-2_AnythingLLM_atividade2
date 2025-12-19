## Tutorial da Análise de Similaridade de Fluxos de Trabalho e Releases

Nesta atividade, foi escolhida a abordagem de feature extraction via embeddings semânticos para identificar os processos de desenvolvimento e entrega do software. O modelo utilizado foi o Qwen/**Qwen3-Embedding-0.6B**, disponível no Hugging Face. Esse modelo foi carregado no script Python por meio da biblioteca `sentence-transformers`, que permite converter textos em representações vetoriais (embeddings) para cálculo de similaridade contextual.

A primeira etapa consistiu em estruturar um resumo técnico do projeto **AnythingLLM**, contendo dados estatísticos e comportamentais sobre o repositório, como a estrutura de branches, frequência de Pull Requests, ausência de branch "develop" e padrões de versionamento (tags).

Em seguida, foram criadas descrições curtas e objetivas divididas em duas categorias de análise:

1. Modelos de Branching:

   - GitHub Flow

   - Gitflow

   - Trunk-Based Development

   - GitLab Flow

2. Estratégias de Release:

   - Semantic Versioning
 
   - Release Train

   - Rolling Release

   - Ad-hoc Release

Cada descrição foi mapeada em dicionários Python para facilitar o processamento sequencial.

Com o modelo carregado e os textos definidos, o script gerou embeddings tanto para o resumo do AnythingLLM quanto para cada definição teórica. Depois, foi calculada a similaridade entre o vetor da entrada e os vetores dos padrões utilizando o cosseno como métrica.

O resultado final exibiu, em ordem decrescente, quais modelos de fluxo e estratégias de entrega apresentavam maior correlação semântica com a realidade do projeto. Assim, foi possível identificar, de forma quantitativa, que o AnythingLLM adota predominantemente o GitHub Flow como fluxo de trabalho e o Semantic Versioning como estratégia de lançamento.