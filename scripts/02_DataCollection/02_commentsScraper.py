import youtube_comment_downloader as ycd
import pandas as pd
import logging
import os
import csv
from tqdm import tqdm

def configurar_logger(nome_logger, log_filename):
    logger = logging.getLogger(nome_logger)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

logger = configurar_logger('commentsScraper', os.path.join(os.getcwd(), 'commentsScraper.log'))

def getComments(videoid, pasta, pbar=None):
    writefilename = os.path.join(os.getcwd(), pasta, f'{pasta}_comentarios_{videoid}.json')
    if os.path.isfile(writefilename):
        try:
            df = pd.read_json(writefilename)
            if len(df.index) > 0:
                message = f'Arquivo de comentários do vídeo {videoid} já existe com {len(df.index)} comentários'
                logger.info(message)
                if pbar:
                    pbar.update(1)
                return
        except:
            pass
    
    downloader = ycd.YoutubeCommentDownloader()
    
    try:
        logger.info(f'Iniciando raspagem de comentários do vídeo {videoid}')
        comments = downloader.get_comments(videoid)
    
    except:
        message = f'Erro ao baixar comentários do vídeo {videoid}'
        logger.error(message)
        if pbar:
            pbar.update(1)
        return

    try:
        df = pd.DataFrame(comments)
        count = len(df.index)
        json_filename = os.path.join(os.getcwd(), pasta, f'{pasta}_comentarios_{videoid}.json')
        with open(json_filename, 'w', encoding='utf8') as f:
            df.to_json(f, force_ascii=False, orient='records', indent=4)
    except Exception as e:
        message = f'Erro ao salvar arquivo de comentários do vídeo {videoid}: {e}'
        logger.error(message)
        if pbar:
            pbar.update(1)
        return

    message = f'{count} comentários baixados do vídeo {videoid}. Concluído!'
    logger.info(message)
    if pbar:
        pbar.update(1)


pastas = [d for d in os.listdir(os.getcwd()) if d.startswith('@')]

for pasta in pastas:
    nome_pasta = os.path.join(os.getcwd(), pasta)
    logger.info(f'Iniciando raspagem de comentários da pasta {pasta}')
    csv_file = os.path.join(nome_pasta, f'videolist_{pasta}.csv')
    
    # Contar total de vídeos no CSV
    with open(csv_file, newline='', encoding='utf8') as f:
        total_videos = sum(1 for _ in csv.DictReader(f))
    
    # Processar com barra de progresso
    with open(csv_file, newline='', encoding='utf8') as f:
        reader = csv.DictReader(f)
        with tqdm(total=total_videos, desc=f'{pasta}', unit='vídeo', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]\n') as pbar:
            for row in reader:
                videoid = row['videoId']
                getComments(videoid, pasta, pbar)
    
    logger.info(f'Concluída raspagem de comentários da pasta {pasta}')

print('Concluído!')
