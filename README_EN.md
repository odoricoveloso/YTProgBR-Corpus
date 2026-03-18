# YouTube Programming Brazil Corpus (YTProgBR-Corpus)

> **Note:** This corpus is linked to ongoing scientific research and will be made available after the publication of the associated article.

## Description

The **YTProgBR-Corpus** is a large-scale textual corpus composed of metadata, transcriptions, and comments from computer programming videos in Brazilian Portuguese. The data was collected from 80 relevant Brazilian channels on the YouTube platform, selected through a methodology that combines "snowball" sampling and relevance analysis.

This resource was developed to support research in Natural Language Processing (NLP), Corpus Linguistics, Sentiment Analysis, Topic Modeling, and studies on online learning communities in the technology domain.

## Current Repository Structure

The repository is organized into three main parts:

1. **Documentation**
    * `README.md`
    * `README_EN.md`

2. **Channel-based data (`data/`)**
    * Contains **80 JSON files** (one per channel), using the `@channelName.json` pattern.
    * Each file aggregates, per video, metadata, transcript, cleaned transcript, and comments.

3. **Processing pipeline (`scripts/`)**
    * Organized into 6 numbered stages, from channel discovery to topic modeling.

### Directory tree

```text
YTProgBR-Corpus/
|-- README.md
|-- README_EN.md
|-- data/
|   |-- @99coders.json
|   |-- @AlexandreCardoso.json
|   |-- ... (80 channel JSON files)
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

## Pipeline Stages

| Stage | Folder | Current status | Main content |
| :---- | :----- | :------------- | :----------- |
| 01 | `scripts/01_DataDiscovery` | Implemented | Notebook and channel search/network artifacts (`.csv`, `.gdf`, IDs, and selected channels). |
| 02 | `scripts/02_DataCollection` | Implemented | Scripts for metadata, comments, and transcript collection; per-channel merge. |
| 03 | `scripts/03_DataCleaning` | Implemented | Comment/transcript anonymization and text cleaning + stopwords. |
| 04 | `scripts/04_CorpusCharacterization` | Implemented | Descriptive statistics generation in Python with `.json` and `.xlsx` outputs. |
| 05 | `scripts/05_SentimentAnalysis` | Scaffold created | Reserved folder for sentiment analysis. |
| 06 | `scripts/06_TopicModeling` | Scaffold created | Reserved folder for topic modeling. |

---

## Data Dictionary

Below is the observed structure of the JSON files in the `data/` folder.

### 1. Structure of each channel file (`data/@channel.json`)

Each file is a **list of videos** from that channel.

| Field | Data Type | Description |
| :---- | :-------- | :---------- |
| `video_id` | Text (String) | YouTube video ID. |
| `metadata` | Object (JSON) | Video metadata. |
| `transcript` | Text (String) | Raw transcript (when available). |
| `cleaned_transcript` | Text (String) | Transcript after text cleaning. |
| `comments` | List of Objects | Comments associated with the video. |

### 2. Fields in `metadata`

| Field | Data Type | Description |
| :---- | :-------- | :---------- |
| `id` | Text (String) | Unique YouTube video identifier. |
| `title` | Text (String) | Video title. |
| `publishDate` | RFC 3339 | Video publication date and time. |
| `caption` | Boolean or Text | Indicates/describes subtitle/transcript availability. |
| `duration` | `HH:MM:SS` (String) | Video duration. |
| `category` | Text (String) | YouTube video category. |
| `channelId` | Text (String) | YouTube channel identifier. |
| `channelTitle` | Text (String) | Channel name. |
| `thumbnail` | URL (String) | Video thumbnail URL. |
| `commentCount` | Integer | Number of comments. |
| `likeCount` | Integer | Number of likes. |
| `viewCount` | Integer | Number of views. |
| `description` | Text (String) | Video description. |
| `tags` | Text (String) | Video tags (comma-separated in the current collection format). |

### 3. Fields in each item of `comments`

| Field | Data Type | Description |
| :---- | :-------- | :---------- |
| `cid` | Text (String) | Unique comment identifier. |
| `text` | Text (String) | Original comment text. |
| `cleaned_text` | Text (String) | Comment text after cleaning. |
| `time` | Text (String) | Relative publication time (e.g., "2 days ago"). |
| `votes` | Text (String) | Number of likes on the comment. |
| `replies` | Text (String) | Aggregated reply content (when available). |
| `heart` | Boolean | Whether the comment received a heart from the channel. |
| `reply` | Boolean | Whether the comment is a reply. |
| `time_parsed` | Number (Float) | Unix timestamp of collection/processing time. |

---

## License

This corpus is available under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

For more details, see: <https://creativecommons.org/licenses/by-nc-sa/4.0/>

<!-- ## How to Cite

If you use this corpus in your research, please cite the following article:

> ... -->

## Repository

The complete corpus is available in the following GitHub repository:
<https://github.com/odoricoveloso/YTProgBR-Corpus>
