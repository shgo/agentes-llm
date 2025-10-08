chart_task = """Crie gráficos claros e visualmente atraentes utilizando a biblioteca seaborn.
Instale os requisitos (seaborn) e siga as seguintes regras:
1. Adicione um título, eixos rotulados (com unidades), e legenda se necessário.
2. Use `sns.set_context("notebook")` para que textos e configurações de tema como `sns.set_theme()` ou `sns.set_style("whitegrid")` funcionem.
3. Use paletas de cores acessíveis como `sns.color_palette("husl")`.
4. Escolha o plot apropriado: `sns.lineplot()`, `sns.barplot()`, ou `sns.heatmap()`.
5. Anote pontos importantes (e.g., "Pico em 2020") para clareza.
6. Certifique-se que a largura e a resolução do gráfico não passe de 1000px.
7. Mostre a figura com `plt.show()`.
8. Salve a figura no diretório atual (/home/churros/codes/agentes/appropriate_name.pdf) utilizando `plt.savefig(appropriate_name.pdf)`

Objetivo: Produzir gráficos corretos, engajantes e fáceis de interpretar."""


## System prompt
def make_system_prompt(suffix: str) -> str:
    return (
        "Você é um assistente de IA, colaborando com outros assistentes."
        " Use as ferramentas fornecidas para avançar na resposta para a pergunta do usuário."
        " Caso você não consiga responder uma pergunta ou terminar a atividade solicitada, está tudo bem, outro assistente com as ferramentas adequadas"
        " irá continuar o trabalho de onde você parar. Execute o que conseguir para ter progresso."
        " Se você chegar na resposta final ou terminar completamente a atividade, coloque um prefixo na resposta com FINAL ANSWER para o time saber a hora de parar."
        f"\n{suffix}"
    )
