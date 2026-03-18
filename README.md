# YouTube Programming Brazil Corpus (YTProgBR-Corpus)

<!-- > **Observação:** Este corpus está vinculado a uma pesquisa científica em andamento e será disponibilizado após a publicação do artigo associado. -->

## Descrição

O **YTProgBR-Corpus** é um corpus textual de grande escala, composto por metadados, transcrições e comentários de vídeos sobre programação de computadores em português brasileiro. Os dados foram coletados de 80 canais brasileiros relevantes na plataforma YouTube, selecionados através de uma metodologia que combina amostragem "bola de neve" e análise de relevância.

Este recurso foi desenvolvido para apoiar pesquisas em Processamento de Linguagem Natural (PLN), Linguística de Corpus, Análise de Sentimentos, Modelagem de Tópicos e estudos sobre comunidades de aprendizagem on-line no domínio da tecnologia.

## Estrutura Atual do Repositório

O repositório está organizado em três partes principais:

1. **Documentação**
    * `README.md`
    * `README_EN.md`

2. **Dados por canal (`data/`)**
    * Contém **80 arquivos JSON** (um por canal), no padrão `@nomeCanal.json`.
    * Cada arquivo agrega, por vídeo, metadados, transcrição, transcrição limpa e comentários.

3. **Pipeline de processamento (`scripts/`)**
    * Estruturado em 6 etapas numeradas, da descoberta de canais à modelagem de tópicos.

### Árvore de diretórios

```text
YTProgBR-Corpus/
|-- README.md
|-- README_EN.md
|-- data/
|   |-- @99coders.json
|   |-- @AlexandreCardoso.json
|   |-- ... (80 arquivos JSON de canais)
|-- scripts/
|   |-- 01_DataDiscovery/
|   |   |-- DataDiscovery.ipynb
|   |   |-- channel_ids.csv
|   |   |-- channel_ids.txt
|   |   |-- channelsearch_*.csv
|   |   |-- channelnet_*.gdf
|   |   |-- canais_filtrados_DataTools.json
|   |   `-- canais_selecionados_DataTools.{csv,json}
|   |-- 02_DataCollection/
|   |   |-- 01_metadados_youtube_data_tools.py
|   |   |-- 02_commentsScraper.py
|   |   |-- 03_captionsScrapper.py
|   |   `-- 04_unificarDadosporCanal.py
|   |-- 03_DataCleaning/
|   |   |-- 01_Anonimizacao_Comentarios.py
|   |   |-- 02_LimpezaTextual_Comentarios.py
|   |   |-- 03_LimpezaTextual_Transcricoes.py
|   |   `-- stopwords.txt
|   |-- 04_CorpusCharacterization/
|   |   |-- estatisticas_descritivas_corpus.py
|   |   |-- estatisticas_descritivas_corpus.json
|   |   `-- estatisticas_descritivas_corpus.xlsx
|   |-- 05_SentimentAnalysis/
|   `-- 06_TopicModeling/
```

## Etapas do Pipeline

| Etapa | Pasta | Status atual | Conteúdo principal |
| :---- | :---- | :----------- | :----------------- |
| 01 | `scripts/01_DataDiscovery` | Implementada | Notebook e artefatos de busca/rede de canais (`.csv`, `.gdf`, IDs e seleção). |
| 02 | `scripts/02_DataCollection` | Implementada | Scripts de coleta de metadados, comentários e transcrições; unificação por canal. |
| 03 | `scripts/03_DataCleaning` | Implementada | Anonimização e limpeza textual de comentários/transcrições + stopwords. |
| 04 | `scripts/04_CorpusCharacterization` | Implementada | Geração de estatísticas descritivas em Python com saídas `.json` e `.xlsx`. |
| 05 | `scripts/05_SentimentAnalysis` | Estrutura criada | Pasta reservada para análise de sentimentos. |
| 06 | `scripts/06_TopicModeling` | Estrutura criada | Pasta reservada para modelagem de tópicos. |

---

## Dicionário de Dados

A seguir, a descrição da estrutura observada nos JSONs da pasta `data/`.

### 1. Estrutura de cada arquivo de canal (`data/@canal.json`)

Cada arquivo é uma **lista de vídeos** do canal.

| Campo | Tipo de Dado | Descrição |
| :---- | :----------- | :-------- |
| `video_id` | Texto (String) | ID do vídeo no YouTube. |
| `metadata` | Objeto (JSON) | Metadados do vídeo. |
| `transcript` | Texto (String) | Transcrição bruta (quando disponível). |
| `cleaned_transcript` | Texto (String) | Transcrição após limpeza textual. |
| `comments` | Lista de Objetos | Comentários associados ao vídeo. |

### 2. Campos em `metadata`

| Campo | Tipo de Dado | Descrição |
| :---- | :----------- | :-------- |
| `id` | Texto (String) | Identificador único do vídeo no YouTube. |
| `title` | Texto (String) | Título do vídeo. |
| `publishDate` | RFC 3339 | Data e hora de publicação do vídeo. |
| `caption` | Booleano ou Texto | Indica/discrimina disponibilidade de legenda/transcrição. |
| `duration` | `HH:MM:SS` (String) | Duração do vídeo. |
| `category` | Texto (String) | Categoria do vídeo no YouTube. |
| `channelId` | Texto (String) | Identificador do canal no YouTube. |
| `channelTitle` | Texto (String) | Nome do canal. |
| `thumbnail` | URL (String) | URL da miniatura do vídeo. |
| `commentCount` | Inteiro | Número de comentários. |
| `likeCount` | Inteiro | Número de curtidas. |
| `viewCount` | Inteiro | Número de visualizações. |
| `description` | Texto (String) | Descrição do vídeo. |
| `tags` | Texto (String) | Tags associadas ao vídeo (separadas por vírgula na coleta atual). |

### 3. Campos em cada item de `comments`

| Campo | Tipo de Dado | Descrição |
| :---- | :----------- | :-------- |
| `cid` | Texto (String) | Identificador único do comentário. |
| `text` | Texto (String) | Conteúdo textual original do comentário. |
| `cleaned_text` | Texto (String) | Comentário após limpeza textual. |
| `time` | Texto (String) | Indicação relativa de tempo de publicação (ex.: "há 2 dias"). |
| `votes` | Texto (String) | Quantidade de likes no comentário. |
| `replies` | Texto (String) | Conteúdo agregado de respostas (quando houver). |
| `heart` | Booleano | Indica se recebeu coração do canal. |
| `reply` | Booleano | Indica se o comentário é uma resposta. |
| `time_parsed` | Número (Float) | Timestamp Unix de coleta/processamento. |

---

## Licença

Este corpus está disponibilizado sob a licença **Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional (CC BY-NC-SA 4.0)**.

Para mais detalhes, consulte: <https://creativecommons.org/licenses/by-nc-sa/4.0/>

<!-- ## Como Citar

Se você utilizar este corpus em sua pesquisa, por favor, cite o seguinte artigo:

> ... -->

## Repositório

O corpus completo está disponível no seguinte repositório do GitHub:
<https://github.com/odoricoveloso/YTProgBR-Corpus>
