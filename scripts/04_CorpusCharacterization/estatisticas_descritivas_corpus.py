import os
import json
import statistics
import pandas as pd
from tqdm import tqdm

# CAMINHOS DAS PASTAS E ARQUIVOS
CHANNELS_FOLDER = input("Insira o caminho da pasta com os arquivos JSON unificados dos canais: ").strip()
OUTPUT_FOLDER = os.getcwd()
CHANNELS_FILES = [f for f in os.listdir(CHANNELS_FOLDER) if f.endswith(".json")]

# FUNÇÕES AUXILIARES
def load_json_data(file_path):
	channel_name = os.path.basename(file_path).replace(".json", "")
	with open(file_path, "r", encoding="utf-8") as f:
		json_data = json.load(f)
	return channel_name, json_data

def count_words(text):
	if not text or not isinstance(text, str):
		return 0
	return len(text.split())

# COLETA DE DADOS
all_comment_authors = set()

all_comment_word_counts = []
all_comment_words = []

all_transcript_word_counts = []
all_transcript_words = []

total_videos = 0
total_comments = 0

for filename in tqdm(CHANNELS_FILES, desc="Processando arquivos de canais", unit="arquivo"):
	file_path = os.path.join(CHANNELS_FOLDER, filename)
	channel_name, json_data = load_json_data(file_path)
	total_videos += len(json_data)

	for video in json_data:
		for comment in video.get("comments", []):
			cleaned = comment.get("text", "") or ""
			wc = count_words(cleaned)
			all_comment_word_counts.append(wc)
			all_comment_words.extend(cleaned.split())
			total_comments += 1
   
			author = comment.get("author", "") or ""
			if author.strip():
				all_comment_authors.add(author.strip())

		transcript = video.get("transcript", "") or ""
		if transcript.strip():
			wc = count_words(transcript)
			all_transcript_word_counts.append(wc)
			all_transcript_words.extend(transcript.split())

# CÁLCULO DAS ESTATÍSTICAS
num_channels = len(CHANNELS_FILES)
num_videos = total_videos
num_comments = total_comments
words_comments = len(all_comment_words)
unique_words_comments = len(set(all_comment_words))
avg_comment_len = round(statistics.mean(all_comment_word_counts), 2) if all_comment_word_counts else 0
median_comment_len = round(statistics.median(all_comment_word_counts), 2) if all_comment_word_counts else 0
unique_authors = len(all_comment_authors)
num_transcriptions = len(all_transcript_word_counts)
words_transcriptions = len(all_transcript_words)
unique_words_transcriptions = len(set(all_transcript_words))
avg_transcript_len = round(statistics.mean(all_transcript_word_counts), 2) if all_transcript_word_counts else 0
median_transcript_len = round(statistics.median(all_transcript_word_counts), 2) if all_transcript_word_counts else 0

# MONTAGEM DA TABELA
stats = {
	"Quantidade de canais": num_channels,
	"Quantidade de videos": num_videos,
	"Quantidade de comentarios": num_comments,
	"Quantidade de palavras nos comentarios": words_comments,
	"Quantidade de palavras unicas nos comentarios": unique_words_comments,
	"Comprimento medio dos comentarios": avg_comment_len,
	"Mediana de palavras nos comentarios": median_comment_len,
	"Quantidade de autores unicos": unique_authors,
	"Quantidade de transcricoes": num_transcriptions,
	"Quantidade de palavras nas transcricoes": words_transcriptions,
	"Quantidade de palavras unicas nas transcricoes": unique_words_transcriptions,
	"Comprimento medio das transcricoes": avg_transcript_len,
	"Mediana de palavras nas transcricoes": median_transcript_len,
}

# MOSTRAR NO CONSOLE
print()
print("=" * 65)
print(" ESTATISTICAS DESCRITIVAS DO CORPUS")
print("=" * 65)
for label, value in stats.items():
	print(f" {label:<58} {value:>10}")
print("=" * 65)
print()

# EXPORTAR PARA JSON E XLSX
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

json_path = os.path.join(OUTPUT_FOLDER, "estatisticas_descritivas_corpus.json")
with open(json_path, "w", encoding="utf-8") as f:
	json.dump(stats, f, ensure_ascii=False, indent=4)
print(f"JSON salvo em: {json_path}")

df = pd.DataFrame(list(stats.items()), columns=["Estatistica", "Valor"])
xlsx_path = os.path.join(OUTPUT_FOLDER, "estatisticas_descritivas_corpus.xlsx")
with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
	df.to_excel(writer, index=False, sheet_name="Estatisticas")
	ws = writer.sheets["Estatisticas"]
	for col in ws.columns:
		max_len = max(len(str(cell.value)) for cell in col if cell.value) + 4
		ws.column_dimensions[col[0].column_letter].width = max_len
print(f"XLSX salvo em: {xlsx_path}")