import os
import json
from tqdm import tqdm

CHANNELS_FOLDER = input('Insira o caminho da pasta com os canais: ')
OUTPUT_FOLDER = os.path.join(CHANNELS_FOLDER, 'dadosUnificados')
CHANNELS_FOLDERS_LIST = [folder for folder in os.listdir(CHANNELS_FOLDER) if os.path.isdir(os.path.join(CHANNELS_FOLDER, folder)) and folder.startswith('@')]

# Criar pasta de saída se não existir
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def extract_video_id_from_filename(filename):
	basename = os.path.basename(filename)
	# Remove a extensão (.json ou .txt)
	name_without_ext = os.path.splitext(basename)[0]
	# Pega os últimos 11 caracteres
	if len(name_without_ext) >= 11:
		return name_without_ext[-11:]
	return None

# Barra de progresso principal para canais
for channel_folder in tqdm(CHANNELS_FOLDERS_LIST, desc="Processando canais", unit="canal"):
	channel_name = channel_folder
	
	# Caminhos dos arquivos
	channel_path = os.path.join(CHANNELS_FOLDER, channel_folder)
	# Criar pasta para vídeos unificados do canal
	channel_output_folder = os.path.join(OUTPUT_FOLDER, channel_name)
	os.makedirs(channel_output_folder, exist_ok=True)
	
	comments_filenames = [os.path.join(channel_path, f) for f in os.listdir(channel_path) if 'comentarios' in f and f.endswith('.json')]
	transcripts_filenames = [os.path.join(channel_path, f) for f in os.listdir(channel_path) if 'transcricao' in f and f.endswith('.txt')]
	metadata_filenames = [os.path.join(channel_path, f) for f in os.listdir(channel_path) if 'metadata' in f and f.endswith('.json')]
	
	if not metadata_filenames:
		tqdm.write(f"  ⚠️  {channel_name}: Nenhum arquivo de metadados encontrado")
		continue
	
	# Carregar metadados
	with open(metadata_filenames[0], 'r', encoding='utf-8') as f:
		all_metadata = json.load(f)
	
	# Criar dicionários para busca rápida
	comments_dict = {}
	for comment_file in comments_filenames:
		video_id = extract_video_id_from_filename(comment_file)
		if video_id:
			comments_dict[video_id] = comment_file
	
	transcripts_dict = {}
	for transcript_file in transcripts_filenames:
		video_id = extract_video_id_from_filename(transcript_file)
		if video_id:
			transcripts_dict[video_id] = transcript_file
	
	# Processar cada vídeo
	unified_videos = []
	videos_incompletos = 0
	
	# Barra de progresso para vídeos do canal
	for video_metadata in tqdm(all_metadata, desc=f"  {channel_name}", unit="vídeo", leave=False):
		video_id = video_metadata.get('id') or video_metadata.get('video_id')
		
		if not video_id:
			continue
		
		# Verificar se existem comentários e transcrição
		if video_id not in comments_dict or video_id not in transcripts_dict:
			videos_incompletos += 1
			continue
		
		# Carregar comentários
		with open(comments_dict[video_id], 'r', encoding='utf-8') as f:
			comments = json.load(f)
		
		# Carregar transcrição
		with open(transcripts_dict[video_id], 'r', encoding='utf-8') as f:
			transcript = f.read()
		
		# Criar objeto unificado
		unified_video = {
			'video_id': video_id,
			'metadata': video_metadata,
			'transcript': transcript,
			'comments': comments
		}
		
		# Salvar JSON individual do vídeo
		video_output_file = os.path.join(channel_output_folder, f"{channel_name}_{video_id}.json")
		with open(video_output_file, 'w', encoding='utf-8') as f:
			json.dump(unified_video, f, ensure_ascii=False, indent=4)
		
		unified_videos.append(unified_video)
	
	# Salvar arquivo JSON por canal
	if unified_videos:
		output_file = os.path.join(OUTPUT_FOLDER, f"{channel_name}.json")
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(unified_videos, f, ensure_ascii=False, indent=4)
		tqdm.write(f"  ✅ {channel_name}: {len(unified_videos)} vídeos completos, {videos_incompletos} incompletos")
	else:
		tqdm.write(f"  ❌ {channel_name}: Nenhum vídeo completo encontrado ({videos_incompletos} incompletos)")

tqdm.write("\n✨ Processamento concluído!")

