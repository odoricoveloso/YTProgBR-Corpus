# YouTube Programming Brazil Corpus (YTProgBR-Corpus)

> **Note:** This corpus is linked to ongoing scientific research and will be made available after the publication of the associated article.

## Description

The **YTProgBR-Corpus** is a large-scale textual corpus composed of metadata, transcriptions, and comments from computer programming videos in Brazilian Portuguese. The data was collected from 49 relevant Brazilian channels on the YouTube platform, selected through a methodology that combines "snowball" sampling and relevance analysis.

This resource was developed to support research in Natural Language Processing (NLP), Corpus Linguistics, Sentiment Analysis, Topic Modeling, and studies on online learning communities in the technology domain.

## Corpus Structure

The corpus is available in CSV and JSON formats and is organized into the following components:

1. **Video Metadata**
    * `videos_metadata.csv`
    * `videos_metadata.json`
    * **Description:** Contains detailed information about each video, such as ID, title, publication date, statistics (views, likes, comments), and channel information.

2. **Video Transcriptions**
    * `transcricoes/`
    * **Description:** A folder containing text files (`.txt`), where each file corresponds to the automatic transcription of a video. The name of each file is the corresponding video ID (e.g., `videoID123.txt`).

3. **Comments (Unbalanced Corpus)**
    * `comentarios_desbalanceado.json`
    * **Description:** Contains all valid comments collected, maintaining their original length and format (after the cleaning process). This file is ideal for analyses that benefit from the natural variability of online discourse.

4. **Comments (Balanced Corpus)**
    * `comentarios_balanceado.csv`
    * **Description:** Contains 300-word text segments extracted from comments. Each of the 49 channels contributes 8 segments, ensuring a uniform dataset for comparative analyses and NLP techniques that require standardized document sizes.

---

## Data Dictionary

Below is the detailed description of each field present in the corpus files.

### 1. Video Metadata (`videos_metadata.csv` / `.json`)

| Field             | Data Type         | Description                                                  |
| :---------------- | :---------------- | :----------------------------------------------------------- |
| `id`              | Text (String)     | Unique video identifier on YouTube.                         |
| `title`           | Text (String)     | Video title.                                                 |
| `publishDate`     | RFC 3339          | Video publication date and time.                             |
| `caption`         | Text (String)     | Language code of the transcription.                         |
| `duration`        | ISO 8601 (Time)   | Video duration in ISO 8601 format.                          |
| `category`        | Text (String)     | Video category defined by YouTube.                          |
| `channelId`       | Text (String)     | Unique channel identifier on YouTube.                       |
| `channelTitle`    | Text (String)     | Channel title.                                               |
| `thumbnail`       | URL (String)      | Link to the video thumbnail image.                          |
| `commentCount`    | Integer           | Total number of comments.                                    |
| `likeCount`       | Integer           | Total number of likes.                                       |
| `viewCount`       | Integer           | Total number of views.                                       |
| `description`     | Text (String)     | Video description text.                                      |
| `tags`            | List of Strings   | List of keywords (tags) associated with the video.          |

### 2. Unbalanced Comments (`comentarios_desbalanceado.json`)

| Field             | Data Type         | Description                                                         |
| :---------------  | :---------------- | :-----------------------------------------------------------        |
| `cid`             | Text (String)     | Unique comment identifier.                                          |
| `text`            | Text (String)     | Original comment textual content.                                   |
| `soft_clean_text` | Text (String)     | Comment textual content after initial cleaning process.            |
| `hard_clean_text` | Text (String)     | Comment textual content after deep cleaning process.               |
| `time`            | Text (String)     | How long ago the comment was published.                            |
| `author`          | Text (String)     | Anonymized ID (hash) of the comment author.                        |
| `channel`         | Text (String)     | Unique channel identifier.                                          |
| `votes`           | Text (String)     | Number of likes the comment has.                                    |
| `replies`         | Text (String)     | Content of replies to the comment (if any).                        |
| `photo`           | URL (String)      | Link to the comment author's profile picture.                      |
| `heart`           | Boolean           | Indicates if the comment received a "heart" from the channel creator. |
| `reply`           | Boolean           | Indicates if this comment is a reply to another comment.           |
| `time_parsed`     | Number (Float)    | Unix timestamp of the comment collection/processing moment.        |

### 3. Balanced Comments (`comentarios_balanceado.csv`)

| Field          | Data Type      | Description                                         |
| :------------- | :------------- | :-------------------------------------------------- |
| `channel_id`   | Text (String)  | ID of the channel from which the segment originated. |
| `video_id`     | Text (String)  | ID of the video from which the segment originated.   |
| `segment_text` | Text (String)  | Text segment with exactly 300 words.                |

---

## License

This corpus is available under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** license.

For more details, see: <https://creativecommons.org/licenses/by-nc-sa/4.0/>

## How to Cite

If you use this corpus in your research, please cite the following article:

> ...

## Repository

The complete corpus is available in the following GitHub repository:
<https://github.com/odoricoveloso/YTProgBR-Corpus>
