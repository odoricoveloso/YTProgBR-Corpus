# YouTube Programming Brazil Corpus (YTProgBR-Corpus)

## Descrição

O **YTProgBR-Corpus** é um corpus textual de grande escala, composto por metadados, transcrições e comentários de vídeos sobre programação de computadores em português brasileiro. Os dados foram coletados de 49 canais brasileiros relevantes na plataforma YouTube, selecionados através de uma metodologia que combina amostragem "bola de neve" e análise de relevância.

Este recurso foi desenvolvido para apoiar pesquisas em Processamento de Linguagem Natural (PLN), Linguística de Corpus, Análise de Sentimentos, Modelagem de Tópicos e estudos sobre comunidades de aprendizagem on-line no domínio da tecnologia.

## Estrutura do Corpus

O corpus é disponibilizado em formatos CSV e JSON e está organizado nos seguintes componentes:

1.  **Metadados dos Vídeos**
    * `videos_metadata.csv`
    * `videos_metadata.json`
    * **Descrição:** Contém informações detalhadas de cada vídeo, como ID, título, data de publicação, estatísticas (visualizações, curtidas, comentários) e informações do canal.

2.  **Transcrições dos Vídeos**
    * `transcricoes/`
    * **Descrição:** Uma pasta contendo arquivos de texto (`.txt`), onde cada arquivo corresponde à transcrição automática de um vídeo. O nome de cada arquivo é o ID do vídeo correspondente (ex: `videoID123.txt`).

3.  **Comentários (Corpus Desbalanceado)**
    * `comentarios_desbalanceado.json`
    * **Descrição:** Contém todos os comentários válidos coletados, mantendo sua extensão e formato originais (após o processo de limpeza). Este arquivo é ideal para análises que se beneficiam da variabilidade natural do discurso on-line.

4.  **Comentários (Corpus Balanceado)**
    * `comentarios_balanceado.csv`
    * **Descrição:** Contém segmentos textuais de 300 palavras extraídos dos comentários. Cada um dos 49 canais contribui com 8 segmentos, garantindo um conjunto de dados uniforme para análises comparativas e técnicas de PLN que exigem documentos de tamanho padronizado.

## Licença

Este corpus está disponibilizado sob a licença **Creative Commons Atribuição-NãoComercial-Compartilhalgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

Para mais detalhes, consulte: [https://creativecommons.org/licenses/by-nc-sa/4.0/](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## Como Citar

Se você utilizar este corpus em sua pesquisa, por favor, cite o seguinte artigo:

> Silva, O. G. V.; Castro, G. G.; Guelpeli, M. V. C.; Assis, W. L. S. (2025). *CRIAÇÃO DE UM CORPUS PARA ANÁLISE TEXTUAL DE CONTEÚDOS DE PROGRAMAÇÃO NO YOUTUBE: METODOLOGIA E APLICAÇÕES*.

## Repositório

O corpus completo está disponível no seguinte repositório do GitHub:
[https://github.com/odoricoveloso/YTProgBR-Corpus](https://github.com/odoricoveloso/YTProgBR-Corpus)
