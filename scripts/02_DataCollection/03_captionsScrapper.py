import os
import csv
import json
import logging
from tqdm import tqdm
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.proxies import GenericProxyConfig
from datetime import datetime
from youtube_transcript_api._errors import (
	TranscriptsDisabled,
	VideoUnavailable, 
	CouldNotRetrieveTranscript,
	NoTranscriptFound,
	NotTranslatable,
	TranslationLanguageNotAvailable,
	VideoUnplayable,
	InvalidVideoId,
	RequestBlocked,
	IpBlocked,
	AgeRestricted,
	YouTubeRequestFailed,
	FailedToCreateConsentCookie,
	PoTokenRequired
)

def configurar_logger(nome_logger, log_filename):
	logger = logging.getLogger(nome_logger)
	logger.setLevel(logging.INFO)

	if not logger.handlers:
		file_handler = logging.FileHandler(log_filename, encoding='utf-8')
		
		formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d_%H:%M:%S_%Z')
		file_handler.setFormatter(formatter)
		
		logger.addHandler(file_handler)
	
	return logger

logger = configurar_logger('captionsScrapper', os.path.join(os.getcwd(), 'captionsScrapper.log'))

# Lista de códigos de idiomas suportados pelo YouTube
youtube_language_codes = [
	'ab', 'af', 'am', 'ar', 'as', 'ay', 'az', 'be', 'bg', 'bn', 'br', 'bs', 'ca', 'cop', 'cs', 'da', 'de', 'de-AT', 'de-CH', 'de-DE', 'dz', 'el', 'en', 'en-AU', 'en-CA', 'en-GB', 'en-IE', 'en-IN', 'en-US', 'eo', 'es', 'es-419', 'es-ES', 'es-MX', 'es-US', 'et', 'eu', 'fa', 'fa-IR', 'fi', 'fil', 'fo', 'fr', 'fr-BE', 'fr-CA', 'fr-FR', 'ga', 'gd', 'gl', 'gn', 'gu', 'ha', 'hd', 'hi', 'hi-Latn', 'hr', 'hu', 'hy', 'id', 'is', 'it', 'iw', 'ja', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'lt', 'lv', 'mg', 'ml', 'mr', 'ms', 'mt', 'nl', 'nl-BE', 'nl-NL', 'no', 'or', 'pa', 'pl', 'pt', 'pt-BR', 'pt-PT', 'rm', 'ro', 'ru', 'ru-Latn', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'tk', 'tr', 'ts', 'uk', 'und', 'ur', 'uz', 'vi', 'wo', 'yue-HK', 'zh', 'zh-CN', 'zh-HK', 'zh-Hans', 'zh-Hant', 'zh-TW', 'zu', 'zxx'
]

def gettranscript(videoid, pasta_canal, pbar=None):
	
	#check if transcript file already exists
	writefilename = os.path.join(os.getcwd(), pasta_canal, f'{pasta_canal}_transcricao_{videoid}.txt')
	if os.path.isfile(writefilename):
		msg = f'📁 Arquivo já existe: {videoid}'
		logger.info(f'Transcript file already exists: {videoid}')
		if pbar:
			pbar.write(msg)
		return True
	
	try:
		ytt_api = YouTubeTranscriptApi(
			proxy_config=GenericProxyConfig(
				http_url='socks5://127.0.0.1:9050',
				https_url='socks5://127.0.0.1:9050',
			)
		)
		formatter = TextFormatter()
		transcript = formatter.format_transcript(ytt_api.fetch(videoid, languages=youtube_language_codes))

		if not transcript:
			msg = f'❌ Sem transcrição: {videoid}'
			logger.info(f'❌ Sem transcrição: {videoid}')
			if pbar:
				pbar.write(msg)
			return False
			
	# Tratamento específico para cada tipo de exceção
	except TranscriptsDisabled:
		msg = f'🚫 Transcrições desabilitadas: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except VideoUnavailable:
		msg = f'📵 Vídeo indisponível: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except NoTranscriptFound:
		msg = f'🔍 Nenhuma transcrição encontrada: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except AgeRestricted:
		msg = f'🔞 Vídeo restrito por idade: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except InvalidVideoId:
		msg = f'❌ ID de vídeo inválido: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except VideoUnplayable:
		msg = f'⏸️ Vídeo não reproduzível: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except (RequestBlocked, IpBlocked):
		msg = f'🚨 IP bloqueado pelo YouTube: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except NotTranslatable:
		msg = f'🌐 Idioma não traduzível: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except TranslationLanguageNotAvailable:
		msg = f'🈲 Idioma de tradução indisponível: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except YouTubeRequestFailed:
		msg = f'🌐 Falha na requisição ao YouTube: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except FailedToCreateConsentCookie:
		msg = f'🍪 Falha ao criar cookie de consentimento: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except PoTokenRequired:
		msg = f'🔑 PO Token requerido: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except CouldNotRetrieveTranscript as e:
		# Captura outros erros gerais da API
		msg = f'❌ Erro geral da API: {videoid} - {str(e)[:50]}...'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False
		
	except Exception as e:
		# Captura erros não relacionados à API (rede, etc.)
		msg = f'⚠️ Erro inesperado: {videoid} - {str(e)[:50]}...'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False

	try:
		with open(writefilename, 'w', encoding='utf-8') as text_file:
			text_file.write(transcript)
		msg = f'✅ Salvo: {videoid}'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return True
	except Exception as e:
		msg = f'💾 Erro ao salvar {videoid}: {e}...'
		logger.info(msg)
		if pbar:
			pbar.write(msg)
		return False


# while True:
for pasta in [d for d in os.listdir(os.getcwd()) if d.startswith('@')]:
	# nome_pasta = os.path.join(os.getcwd(), pasta)
	logger.info(f'Iniciando raspagem de transcrições da pasta {pasta}')
	csv_file = os.path.join(pasta, f'videolist_{pasta}.csv')
	with open(csv_file, newline='', encoding='utf8') as f:
		reader = csv.DictReader(f)
		video_ids = [row['videoId'] for row in reader if 'videoId' in row]

	comments_filenames = [os.path.join(pasta, f) for f in os.listdir(pasta) if 'comentarios' in f and f.endswith('.json')]

	# Contadores para o resumo final
	sucessos = 0
	falhas = 0

	with tqdm(
		total=len(video_ids),
		desc=f'Processando {pasta}',
		unit='vídeo',
		bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}] {rate_fmt}',
		position=0,
		leave=True
	) as pbar:
		
		for i, video_id in enumerate(video_ids):
			# Atualiza com horário atual
			current_time = datetime.now().strftime('%H:%M:%S')

			# Verificar se há um arquivo de comentários correspondente e se ele contém comentários
			corresponding_comments_file = next((cf for cf in comments_filenames if video_id in cf), None)
			if corresponding_comments_file:
				try:
					with open(corresponding_comments_file, 'r', encoding='utf-8') as comments_file:
						comments_data = json.load(comments_file)
						if len(comments_data) == 0:
							msg = f'⚠️ Pulando {video_id} - Sem comentários'
							logger.info(msg)
							pbar.write(msg)
							pbar.update(1)
							continue
						# Se houver comentários, processa o vídeo normalmente
						else:
							# Processa o vídeo passando a referência da barra de progresso
							resultado = gettranscript(video_id, pasta, pbar)
						
							# Conta sucessos e falhas
							if resultado:
								sucessos += 1
								pbar.set_description(f'✅ {pasta} - {video_id[:11]} [{current_time}]')
							else:
								falhas += 1
								pbar.set_description(f'❌ {pasta} - {video_id[:11]} [{current_time}]')

							# Atualiza a barra de progresso
							pbar.update(1)
				except Exception as e:
					msg = f'⚠️ Erro ao ler {corresponding_comments_file}: {e}'
					logger.info(msg)
					pbar.write(msg)
					falhas += 1
					pbar.update(1)

	# Exibe resumo final
	logger.info(f"\n📊 Resumo do processamento:")
	logger.info(f"✅ Sucessos: {sucessos}")
	logger.info(f"❌ Falhas: {falhas}")
	logger.info(f"📁 Total processado: {len(video_ids)}")
	logger.info(f"📋 Log salvo em: captionsScrapper.log")
	logger.info("------------------------------------------------------")
