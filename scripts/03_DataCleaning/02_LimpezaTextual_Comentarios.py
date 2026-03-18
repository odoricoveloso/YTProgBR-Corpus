# ---------------------------------------------------------------------------------------------------- #
# SCRIPT PARA LIMPEZA TEXTUAL DOS COMENTÁRIOS E TRANSCRIÇÕES
# ---------------------------------------------------------------------------------------------------- #

# Importação das bibliotecas necessárias
import os
import json
import re
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS as spacy_stopwords
from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import word_tokenize
import emoji
import unicodedata
from tqdm import tqdm
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# FUNÇÃO PARA CARREGAR OS DADOS DO ARQUIVO JSON
def load_json_data(file_path):
	channel_name = file_path.split(os.sep)[-1].replace('.json', '')
	with open(file_path, 'r', encoding='utf-8') as f:
		json_data = json.load(f)
	return channel_name, json_data

# FUNÇÃO PARA CARREGAR OS COMENTÁRIOS
def load_comments(channel_name, json_data):
	channel_name = channel_name
	comments = [comment for video in json_data for comment in video.get('comments', [])]
	return comments

# FUNÇÃO PARA LIMPEZA DO TEXTO
def clean_text(text):
	if not isinstance(text, str) or not text: return ''
	
	# 1. NORMALIZAÇÃO INICIAL
	text = text.strip()
	# Substitui o caractere de espaço não separável (\xa0) por um espaço comum
	text = re.sub(r'\xa0', ' ', text, flags=re.UNICODE)
	
	# 2. REMOÇÃO DE ELEMENTOS ESTRUTURADOS (URLs, emails, menções)
	# Remove e-mails e URLs (antes de outras transformações para preservar padrões completos)
	text = re.sub(r'(http|https)://[^\s]+', '', text)
	text = re.sub(r'www.[^\s]+', '', text)
	text = re.sub(r'[^\s]+.com[^\s]+', '', text)
	text = re.sub(r'\S+@\S+', '', text)
	
	# Remove menções e hashtags (após remover URLs para evitar remoção de partes de URLs)
	text = re.sub(r'@\S+', '', text)
	text = re.sub(r'#\S+', '', text)
	
	# 3. REMOÇÃO DE EMOJIS (antes de normalizar acentos para preservar caracteres unicode)
	text = emoji.replace_emoji(text, replace='')
	
	# 4. NORMALIZAÇÃO DE REPETIÇÕES (antes de remover números e caracteres)
	# Normaliza pontuação repetida
	text = re.sub(r'([.!?])\1+', r'\1', text)
	# Remove repetições de risadas (rs, kk, ha, he) com 2 ou mais ocorrências
	text = re.sub(r'\b(rs|kk|ha|he|kkk|rsrs|haha|hehe)\b', '', text, flags=re.IGNORECASE)
	# Normaliza caracteres repetidos (substitui 3 ou mais ocorrências de uma letra por apenas uma)
	text = re.sub(r'([a-zA-Z])\1{2,}', r'\1', text)
	
	# 5. CONVERSÃO PARA MINÚSCULAS (após remover repetições para manter consistência)
	text = text.lower()
	
	# 6. REMOÇÃO DE ACENTOS E NORMALIZAÇÃO UNICODE
	# Remove acentos e normaliza o texto para NFD, depois remove diacríticos
	text = unicodedata.normalize('NFD', text)
	text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
	# Normaliza de volta para NFC após remoção de acentos
	text = unicodedata.normalize('NFC', text)
	
	# 7. REMOÇÃO DE CARACTERES ESPECIAIS
	# Remove variações de aspas
	text = re.sub(r'[''′`\"""]', '', text)
	# Remove parênteses
	text = re.sub(r'[()]', '', text)
	# Remove números
	text = re.sub(r'\d+', '', text)
	# Remove símbolos e pontuação
	text = re.sub(r'[^\w\s]', '', text, flags=re.UNICODE)
	
	# 8. REMOÇÃO DE PALAVRAS CURTAS (após todas as transformações)
	# Remove palavras que não possuam pelo menos 3 caracteres
	text = re.sub(r'\b\w{1,2}\b', '', text)
	
	# 9. LIMPEZA FINAL DE ESPAÇOS
	# Remove espaços extras e linhas vazias
	text = re.sub(r'\s+', ' ', text).strip()
	text = '\n'.join([line for line in text.split('\n') if line.strip()])
	
	# Texto final
	return text

# FUNÇÃO PARA LEMATIZAÇAO COM SPACY
def lemmatize_text(text, nlp):
	doc = nlp(text)
	lemmatized_tokens = [token.lemma_ if (token.pos_ == 'VERB' and not token.is_punct and not token.is_space and token.is_alpha) else token.text for token in doc]
	lemmatized_text = ' '.join(lemmatized_tokens)
	return lemmatized_text

# FUNÇÃO PARA CARREGAR STOPWORDS
def load_stopwords(nltk_stopwords, spacy_stopwords, stopwords_file):
	# NLTK
	nltk_stopwords = nltk_stopwords.words('portuguese')
	# SPACY
	spacy_stopwords = list(spacy_stopwords)
	# STOPWORDS PERSONALIZADAS
	with open(stopwords_file, 'r', encoding='utf-8') as f:
		custom_stopwords = [line.strip() for line in f if line.strip()]
	# COMBINAR TODAS AS STOPWORDS
	all_stopwords = list(set(nltk_stopwords) | set(spacy_stopwords) | set(custom_stopwords))
	print(f"Total de stopwords carregadas: {len(all_stopwords)}")
	return all_stopwords

# FUNÇÃO PARA REMOVER STOPWORDS
def remove_stopwords(text, stopwords):
	tokens = word_tokenize(text, language='portuguese')
	filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
	return ' '.join(filtered_tokens)

# FUNÇÃO PARA REMOVER COMENTÁRIOS DO PRÓPRIO CANAL
def remove_self_comments(comments, channel_name):
	filtered_comments = [comment for comment in comments if comment.get('author').lower() != channel_name.lower()]
	return filtered_comments

if __name__ == "__main__":
    
    # Inserir o caminho da pasta com os arquivos JSON unificados dos canais
	CHANNELS_FOLDER = input("Insira o caminho da pasta com os arquivos JSON unificados dos canais: ")
	if not os.path.isdir(CHANNELS_FOLDER):
		logger.error(f"O caminho '{CHANNELS_FOLDER}' não é uma pasta válida. Verifique o caminho e tente novamente.")
		exit(1)
	else:
		logger.info(f"Pasta '{CHANNELS_FOLDER}' encontrada. Iniciando processamento dos canais.")
		CHANNELS_FILES = [f for f in os.listdir(CHANNELS_FOLDER) if f.endswith('.json')]
    
	# Carregar modelo Spacy
	nlp = spacy.load('pt_core_news_lg', disable=['ner', 'parser', 'textcat'])
	
	# Carregar stopwords
	# STOPWORDS
	stopwords_file = os.path.join(os.getcwd(), 'stopwords.txt')
	if not os.path.isfile(stopwords_file):
		logger.error(f"O arquivo '{stopwords_file}' não foi encontrado. Prosseguindo com as stopwords do NLTK e Spacy apenas.")
	else:
		logger.info(f"Arquivo de stopwords '{stopwords_file}' encontrado. Carregando stopwords combinadas.")
	spacy_stopwords = spacy_stopwords
	nltk_stopwords = nltk_stopwords
	all_stopwords = load_stopwords(nltk_stopwords, spacy_stopwords, stopwords_file)
	
	# Processar cada canal
	for channel_file in tqdm(CHANNELS_FILES, desc="Processando canais", unit="canal"):
		channel_path = os.path.join(CHANNELS_FOLDER, channel_file)
		channel_name, json_data = load_json_data(channel_path)

		# Remover comentários do próprio canal
		for video in tqdm(json_data, desc=f"  Removendo comentários do próprio canal {channel_name}", unit="vídeo", leave=False):
			video['comments'] = remove_self_comments(video.get('comments', []), channel_name)

		# Processar comentários diretamente no json_data
		for video in tqdm(json_data, desc=f"  Processando vídeos de {channel_name}", unit="vídeo", leave=False):
			for comment in video.get('comments', []):
				original_text = comment.get('text', '')
				
				# Limpeza textual
				cleaned_text = clean_text(original_text)

				# Verificar se ainda há texto para processar após a limpeza
				if cleaned_text:
					cleaned_text = lemmatize_text(cleaned_text, nlp)
					cleaned_text = remove_stopwords(cleaned_text, all_stopwords)
					cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
     
				# Adicionar cleaned_text apenas se não estiver vazio
				comment['cleaned_text'] = cleaned_text if cleaned_text else ''
				
				# Reorganizar as chaves para manter cleaned_text após text
				keys = list(comment.keys())
				if 'text' in keys and 'cleaned_text' in keys:
					text_idx = keys.index('text')
					keys.remove('cleaned_text')
					keys.insert(text_idx + 1, 'cleaned_text')
					comment = {k: comment[k] for k in keys}
					video['comments'][video['comments'].index(comment)] = comment
		
		# Salvar o arquivo JSON atualizado
		with open(channel_path, 'w', encoding='utf-8') as f:
			json.dump(json_data, f, ensure_ascii=False, indent=4)
		
		logger.info(f"Canal {channel_name} processado e salvo com sucesso")