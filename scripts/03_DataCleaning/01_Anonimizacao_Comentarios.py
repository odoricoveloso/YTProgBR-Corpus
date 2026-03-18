import json
import logging
import os
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

KEYS_TO_REMOVE = ('author', 'channel', 'photo')

def anonymize_comments_in_video(video):
    comments = video.get('comments', [])
    processed_count = 0
    anonymized_count = 0

    for comment in comments:
        if not isinstance(comment, dict):
            continue

        processed_count += 1
        had_sensitive_keys = any(key in comment for key in KEYS_TO_REMOVE)

        for key in KEYS_TO_REMOVE:
            comment.pop(key, None)

        if had_sensitive_keys:
            anonymized_count += 1

    return processed_count, anonymized_count

def process_channel_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    total_comments = 0
    anonymized_comments = 0

    for video in json_data:
        if not isinstance(video, dict):
            continue

        processed_count, anonymized_count = anonymize_comments_in_video(video)
        total_comments += processed_count
        anonymized_comments += anonymized_count

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    return total_comments, anonymized_comments



if __name__ == '__main__':
    channels_folder = input('Insira o caminho da pasta com os arquivos JSON unificados dos canais: ').strip()

    if not os.path.isdir(channels_folder):
        logger.error(f"O caminho '{channels_folder}' nao e uma pasta valida. Verifique o caminho e tente novamente.")
        raise SystemExit(1)

    channel_files = [f for f in os.listdir(channels_folder) if f.endswith('.json')]

    if not channel_files:
        logger.warning('Nenhum arquivo .json foi encontrado na pasta informada.')
        raise SystemExit(0)

    logger.info(f'Iniciando anonimização de {len(channel_files)} arquivo(s).')

    total_comments_global = 0
    total_anonymized_global = 0

    for channel_file in tqdm(channel_files, desc='Anonimizando comentários', unit='canal'):
        channel_path = os.path.join(channels_folder, channel_file)

        try:
            total_comments, anonymized_comments = process_channel_file(channel_path)
            total_comments_global += total_comments
            total_anonymized_global += anonymized_comments
            logger.info(
                f'Arquivo {channel_file}: {anonymized_comments} comentario(s) anonimizados de {total_comments} comentario(s).'
            )
        except json.JSONDecodeError as error:
            logger.error(f'Arquivo {channel_file} invalido (JSON malformado): {error}')
        except OSError as error:
            logger.error(f'Falha ao processar {channel_file}: {error}')

    logger.info(
        f'Processo concluido. Total de comentarios processados: {total_comments_global}; '
        f'total anonimizados: {total_anonymized_global}.'
    )