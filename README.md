# Agentes Baseados em LLM
Este repositório contém uma demonstração de como implementar um agente simples baseado em LLM e também um sistema multi-agentes, utilizando a biblioteca Langhchain.
O material foi criado para as aulas da disciplina "Tecnologias Emergentes em TI", dos cursos de Sistemas de Informação e Engenharia de Software, no segundo semestre de 2025.

Os arquivos desse repositório são:
- **agente_simples.py**: interface com LLM para responder perguntas simples diretamente.
- **multi_agentes.py**: 3 agentes com acesso a ferramentas de busca e execução de código python cooperam para atender um requisito do usuário.
- **prompts.py**: definições de texto utilizadas para contextualizar agentes.
- **tools.py**: definições das ferramentas disponíveis para os agentes da demonstração de multi-agentes.

## Langchain
Utilizamos o langchain como ferramenta de orquestração dos agentes.
O exemplo do sistema multi-agentes foi baseado na demonstração [multi-agent collaboration](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/multi_agent/multi-agent-collaboration.ipynb).

## Github Models
https://docs.github.com/en/github-models/quickstart
https://github.com/marketplace/models/azure-openai/gpt-4-1/playground

# Instruções de Uso
1. Crie um ambiente virtual e instale as dependências do projeto:
Instruções para o linux:
```
python -m venv env
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -f requirements.txt

```
2. Exporte seu token de autenticação do Github, para poder utilizar o Github Models: ```export GITHUB_TOKEN=\"...\"```
3. Caso você utilize a busca com a ferramenta Tavily, deve exportar o token de autenticação da API também.
4. Execute o agente que deseja: ```python agente_simples.py``` ou ```python multi_agentes.py```

-----
# Atividade em Grupo

Vocês deverão criar um sistema multi-agente que seja capaz de responder perguntas sobre a economia de qualquer cidade brasileira.
Seu sistema deve ser capaz de responder perguntas diretas sobre o clima com base em dados da WEB, e também criar gráficos históricos com informações sobre a economia de uma cidade determinada pelo usuário.
As perguntas irão envolver questões pontuais do momento atual, bem como visões históricas sobre a economia da cidade envolvendo no máximo o intervalo de 5 anos.

Lembre-se:
1. Escreva **bons prompts** para cada agente. Essa é a chave para um bom sistema.
2. Atenção ao **controle de fluxo** das ações entre agentes.
3. **Ajuste bem o contexto** que cada agente tem acesso.
4. **Estruture a saída** dos seus agentes se for necessário (JSON, por exemplo).
5. Mantenha o uso do modelo ```openai/gpt-5-mini```.

Serão penalizados:
- Sistemas complexos demais;
- Sistemas que alucinam muito;
- Sistemas que não resolvem casos básicos;

Para dicas mais detalhadas sobre o design de agentes, consulte os documentos referenciados abaixo:
- [Anthropic - Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
- [OpenAI - A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
- [12 Factor Agents - Principles for building reliable LLM applications](https://github.com/humanlayer/12-factor-agents)
