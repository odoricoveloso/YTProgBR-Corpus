# YouTube Programming Brazil Corpus (YTProgBR-Corpus)

> **Observação:** Este corpus está vinculado a uma pesquisa científica em andamento e será disponibilizado após a publicação do artigo associado.

## Descrição

O **YTProgBR-Corpus** é um corpus textual de grande escala, composto por metadados, transcrições e comentários de vídeos sobre programação de computadores em português brasileiro. Os dados foram coletados de 49 canais brasileiros relevantes na plataforma YouTube, selecionados através de uma metodologia que combina amostragem "bola de neve" e análise de relevância.

Este recurso foi desenvolvido para apoiar pesquisas em Processamento de Linguagem Natural (PLN), Linguística de Corpus, Análise de Sentimentos, Modelagem de Tópicos e estudos sobre comunidades de aprendizagem on-line no domínio da tecnologia.

## Estrutura do Corpus

O corpus é disponibilizado em formatos CSV e JSON e está organizado nos seguintes componentes:

1. **Metadados dos Vídeos**
    * `videos_metadata.csv`
    * `videos_metadata.json`
    * **Descrição:** Contém informações detalhadas de cada vídeo, como ID, título, data de publicação, estatísticas (visualizações, curtidas, comentários) e informações do canal.

2. **Transcrições dos Vídeos**
    * `transcricoes/`
    * **Descrição:** Uma pasta contendo arquivos de texto (`.txt`), onde cada arquivo corresponde à transcrição automática de um vídeo. O nome de cada arquivo é o ID do vídeo correspondente (ex: `videoID123.txt`).

3. **Comentários (Corpus Desbalanceado)**
    * `comentarios_desbalanceado.json`
    * **Descrição:** Contém todos os comentários válidos coletados, mantendo sua extensão e formato originais (após o processo de limpeza). Este arquivo é ideal para análises que se beneficiam da variabilidade natural do discurso on-line.

4. **Comentários (Corpus Balanceado)**
    * `comentarios_balanceado.csv`
    * **Descrição:** Contém segmentos textuais de 300 palavras extraídos dos comentários. Cada um dos 49 canais contribui com 8 segmentos, garantindo um conjunto de dados uniforme para análises comparativas e técnicas de PLN que exigem documentos de tamanho padronizado.

---

## Dicionário de Dados

A seguir, a descrição detalhada de cada campo presente nos arquivos do corpus.

### 1. Metadados dos Vídeos (`videos_metadata.csv` / `.json`)

| Campo             | Tipo de Dado      | Descrição                                                    |
| :---------------- | :---------------- | :----------------------------------------------------------- |
| `id`              | Texto (String)    | Identificador único do vídeo no YouTube.                     |
| `title`           | Texto (String)    | Título do vídeo.                                             |
| `publishDate`     | RFC 3339          | Data e hora de publicação do vídeo.                          |
| `caption`         | Texto (String)    | Código do idioma da transcrição.                             |
| `duration`        | ISO 8601 (Time)   | Duração do vídeo no formato ISO 8601.                        |
| `category`        | Texto (String)    | Categoria do vídeo definida pelo YouTube.                    |
| `channelId`       | Texto (String)    | Identificador único do canal no YouTube.                     |
| `channelTitle`    | Texto (String)    | Título do canal.                                             |
| `thumbnail`       | URL (String)      | Link para a imagem de capa (thumbnail) do vídeo.             |
| `commentCount`    | Inteiro (Integer) | Número total de comentários.                                 |
| `likeCount`       | Inteiro (Integer) | Número total de curtidas.                                    |
| `viewCount`       | Inteiro (Integer) | Número total de visualizações.                               |
| `description`     | Texto (String)    | Texto da descrição do vídeo.                                 |
| `tags`            | Lista de Strings  | Lista de palavras-chave (tags) associadas ao vídeo.          |

### 2. Comentários Desbalanceado (`comentarios_desbalanceado.json`)

| Campo             | Tipo de Dado      | Descrição                                                           |
| :---------------  | :---------------- | :-----------------------------------------------------------        |
| `cid`             | Texto (String)    | Identificador único do comentário.                                  |
| `text`            | Texto (String)    | Conteúdo textual do comentário original.                            |
| `soft_clean_text` | Texto (String)    | Conteúdo textual do comentário após o processo de limpeza inicial.  |
| `hard_clean_text` | Texto (String)    | Conteúdo textual do comentário após o processo de limpeza profunda. |
| `time`            | Texto (String)    | Há quanto tempo o comentário foi publicado.                         |
| `author`          | Texto (String)    | ID anonimizado (hash) do autor do comentário.                       |
| `channel`         | Texto (String)    | Identificador único do canal.                                       |
| `votes`           | Texto (String)    | Quantidade de likes que o comentário tem.                           |
| `replies`         | Texto (String)    | Conteúdo das respostas ao comentário (se houver).                   |
| `photo`           | URL (String)      | Link para a foto de perfil do autor do comentário.                  |
| `heart`           | Booleano (Boolean)| Indica se o comentário recebeu um "coração" do criador do canal.    |
| `reply`           | Booleano (Boolean)| Indica se este comentário é uma resposta a outro comentário.        |
| `time_parsed`     | Número (Float)    | Timestamp Unix do momento da coleta/processamento do comentário.    |

### 3. Comentários Balanceado (`comentarios_balanceado.csv`)

| Campo          | Tipo de Dado   | Descrição                                          |
| :------------- | :------------- | :------------------------------------------------- |
| `channel_id`   | Texto (String) | ID do canal de onde o segmento foi originado.      |
| `video_id`     | Texto (String) | ID do vídeo de onde o segmento foi originado.      |
| `segment_text` | Texto (String) | Segmento textual com exatamente 300 palavras.      |

---

## Licença

Este corpus está disponibilizado sob a licença **Creative Commons Atribuição-NãoComercial-Compartilhalgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

Para mais detalhes, consulte: <https://creativecommons.org/licenses/by-nc-sa/4.0/>

## Como Citar

Se você utilizar este corpus em sua pesquisa, por favor, cite o seguinte artigo:

> ...

## Repositório

O corpus completo está disponível no seguinte repositório do GitHub:
<https://github.com/odoricoveloso/YTProgBR-Corpus>
