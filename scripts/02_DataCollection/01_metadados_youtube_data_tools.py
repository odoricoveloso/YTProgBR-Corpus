import os
import json
import time
from playwright.sync_api import sync_playwright
from playwright_recaptcha import recaptchav2

# Arquivo com os IDs e nomes dos canais
JSON_FILE = input('Insira o caminho do arquivo JSON: ')

def read_channels_from_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [(item['id'], item['title']) for item in data if 'id' in item and 'title' in item]
    except FileNotFoundError:
        print(f"Arquivo {filename} não encontrado!")
        return []
    except Exception as e:
        print(f"Erro ao ler arquivo {filename}: {e}")
        return []

def file_already_exists(channel_name):
	folder_name = channel_name
	file_path = os.path.join(folder_name, f'videolist_{channel_name}.csv')
	return os.path.exists(file_path)

def process_channel(page, channel_id, channel_name):
	print(f"\n{'='*50}")
	print(f"Processando canal: {channel_name} ({channel_id})")
	print(f"{'='*50}")
	
	# Vai para a página inicial
	page.goto('https://ytdt.digitalmethods.net/mod_videos_list.php')
	
	# Preenche o ID do canal
	input_element = page.locator('input[name="channel"]')
	input_element.fill(channel_id)

	# Resolve o captcha apenas uma vez por sessão
	try:
		# Verifica se há captcha visível
		if page.locator('iframe[src*="recaptcha"]').count() > 0:
			with recaptchav2.SyncSolver(page) as solver:
				solver.solve_recaptcha(wait=True)
				print('Captcha Resolvido')
	except Exception as e:
		print(f"Erro com captcha: {e}")
	
	time.sleep(1)
	
	# Clica no botão submit
	page.click('input[type="submit"]', timeout=0)
	
	# Aguarda o início do processamento
	try:
		page.wait_for_selector('div.rowTab:has-text("Processing:")', timeout=0)
		print(f'Processamento iniciado para {channel_name}...')
	except Exception as e:
		print(f"Erro ao aguardar processamento: {e}")
		return False
	
	# Monitora o progresso em tempo real
	last_number = -1
	total_videos = None
	
	while True:
		try:
			# Rola a página para baixo para manter os elementos visíveis
			page.evaluate("window.scrollTo(0, Math.max(document.body.scrollHeight, document.documentElement.scrollHeight))")
			
			# Localiza a div de processamento
			processing_div = page.locator('div.rowTab:has-text("Processing:")')
			
			if processing_div.count() > 0:
				content = processing_div.inner_text()
				
				# Extrai o número total de vídeos se ainda não foi obtido
				if total_videos is None and "Getting video details (" in content:
					start_idx = content.find("Getting video details (") + len("Getting video details (")
					end_idx = content.find("):", start_idx)
					if end_idx > start_idx:
						total_videos = int(content[start_idx:end_idx])
						print(f"Total de vídeos para processar: {total_videos}")
				
				# Extrai os números processados
				if "): " in content:
					numbers_part = content.split("): ")[1].split("<br>")[0]
					numbers = numbers_part.strip().split()
					
					if numbers and numbers[-1].isdigit():
						current_number = int(numbers[-1])
						
						# Só mostra o progresso se mudou
						if current_number != last_number:
							last_number = current_number
							progress = current_number + 1  # +1 porque começa do 0
							
							if total_videos:
								percentage = (progress / total_videos) * 100
								print(f"\r{channel_name}: {progress}/{total_videos} ({percentage:.1f}%)", end="", flush=True)
							else:
								print(f"\r{channel_name}: {progress} vídeos...", end="", flush=True)
			
			# Verifica se o processamento terminou
			if page.locator('text=The script has created a file').count() > 0:
				print(f"\nProcessamento de {channel_name} concluído!")
				break
				
			time.sleep(0.5)  # Aguarda meio segundo antes da próxima verificação
			
		except Exception as e:
			print(f"Erro ao monitorar progresso: {e}")
			return False
	
	time.sleep(2)
	
	# Download do arquivo
	try:
		file_link_element = page.locator('a:has-text("videolist_channel")')
		file_link_element.wait_for(timeout=0)

		with page.expect_download() as download_info:
			file_link_element.click()
		download = download_info.value
		
		# Salva o arquivo na pasta correspondente
		folder_name = channel_name
		os.makedirs(folder_name, exist_ok=True)
		file_path = os.path.join(folder_name, f'videolist_{channel_name}.csv')
		download.save_as(file_path)
		print(f'Arquivo salvo em: {file_path}')
		return True
		
	except Exception as e:
		print(f"Erro ao fazer download: {e}")
		return False

# Execução principal
channels = read_channels_from_json(JSON_FILE)

if not channels:
	print("Nenhum canal encontrado no arquivo!")
	exit()

print(f"Encontrados {len(channels)} canais para processar:")
print("🔍 Verificando arquivos existentes...")

with sync_playwright() as playwright:
	browser = playwright.firefox.launch(headless=False)
	page = browser.new_page()
	
	successful = 0
	failed = 0
	skipped = 0
	
	for i, (channel_id, channel_name) in enumerate(channels, 1):
		print(f"\n[{i}/{len(channels)}] Verificando {channel_name}...")
		
		# Verifica se o arquivo já existe
		if file_already_exists(channel_name) and os.path.getsize(os.path.join(channel_name, f'videolist_{channel_name}.csv')) > 0:
			print(f"⏭️  Arquivo já existe para {channel_name}, pulando...")
			skipped += 1
			continue
		
		print(f"🔄 Processando {channel_name}...")
		
		if process_channel(page, channel_id, channel_name):
			successful += 1
		else:
			failed += 1
			print(f"❌ Falha ao processar {channel_name}")
		
		# Pequena pausa entre canais
		time.sleep(3)
	
	print(f"\n{'='*50}")
	print(f"RESUMO FINAL:")
	print(f"Total de canais: {len(channels)}")
	print(f"✅ Processados com sucesso: {successful}")
	print(f"⏭️  Pulados (já existiam): {skipped}")
	print(f"❌ Falharam: {failed}")
	print(f"{'='*50}")
	
	page.close()
	browser.close()
