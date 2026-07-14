import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- CONFIGURAÇÕES DO TESTE ---
TARGET_URL = "https://book.omnibees.com/hotelresults?c=11362&version=4&q=19736&CheckIn=15082026&CheckOut=18082026&ad=2"
# Ajuste o caminho do driver se for testar o Selenium (tire da lixeira se necessário)
DRIVER_PATH = "./chromedriver.exe" 
NUM_REPETICOES = 3

try:
    import psutil
    def obter_memoria_atual():
        process = psutil.Process(os.getpid())
        # Retorna a memória em Megabytes (MB)
        return process.memory_info().rss / (1024 * 1024)
except ImportError:
    print("Dica: Instale 'psutil' (pip install psutil) para medir a memória RAM.")
    def obter_memoria_atual():
        return 0

# --- METODO 1: REQUESTS + BEAUTIFUL SOUP ---
def testar_requests():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    mem_antes = obter_memoria_atual()
    inicio = time.perf_counter()
    
    # Executa a requisição
    response = requests.get(TARGET_URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    quartos = soup.find_all('p', {'class': 'room_name'})
    qtd_quartos = len(quartos)
    
    fim = time.perf_counter()
    mem_depois = obter_memoria_atual()
    
    tempo_gasto = fim - inicio
    memoria_usada = max(0, mem_depois - mem_antes)
    
    return tempo_gasto, memoria_usada, qtd_quartos

# --- METODO 2: SELENIUM (HEADLESS) ---
def testar_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    mem_antes = obter_memoria_atual()
    inicio = time.perf_counter()
    
    # Inicializa e roda o navegador
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(TARGET_URL)
    rendered_html = driver.page_source
    driver.quit()
    
    # Processa o HTML
    soup = BeautifulSoup(rendered_html, "html.parser")
    quartos = soup.find_all('p', {'class': 'room_name'})
    qtd_quartos = len(quartos)
    
    fim = time.perf_counter()
    mem_depois = obter_memoria_atual()
    
    tempo_gasto = fim - inicio
    memoria_usada = max(0, mem_depois - mem_antes)
    
    return tempo_gasto, memoria_usada, qtd_quartos

# --- EXECUÇÃO DO BENCHMARK ---
if __name__ == "__main__":
    print("=" * 50)
    print(" INICIANDO BENCHMARK COMPARATIVO ")
    print("=" * 50)
    
    # 1. Testando Requests
    print(f"\n[1/2] Rodando {NUM_REPETICOES} testes com REQUESTS + BS4...")
    tempos_req = []
    mems_req = []
    for i in range(NUM_REPETICOES):
        t, m, q = testar_requests()
        tempos_req.append(t)
        mems_req.append(m)
        print(f"   Execução {i+1}: {t:.2f}s | RAM extra: {m:.2f}MB | Quartos: {q}")
        time.sleep(1) # Intervalo amigável para o servidor
        
    media_tempo_req = sum(tempos_req) / NUM_REPETICOES
    media_mem_req = sum(mems_req) / NUM_REPETICOES
    
    # 2. Testando Selenium (Apenas se o driver existir)
    if os.path.exists(DRIVER_PATH) or True: # Remova o 'or True' se não quiser que ele tente rodar sem o driver
        print(f"\n[2/2] Rodando {NUM_REPETICOES} testes com SELENIUM...")
        tempos_sel = []
        mems_sel = []
        try:
            for i in range(NUM_REPETICOES):
                t, m, q = testar_selenium()
                tempos_sel.append(t)
                mems_sel.append(m)
                print(f"   Execução {i+1}: {t:.2f}s | RAM extra: {m:.2f}MB | Quartos: {q}")
                time.sleep(1)
                
            media_tempo_sel = sum(tempos_sel) / NUM_REPETICOES
            media_mem_sel = sum(mems_sel) / NUM_REPETICOES
            
            # --- RESULTADO FINAL ---
            print("\n" + "=" * 50)
            print(" RESULTADOS DO COMPARATIVO REAL ")
            print("=" * 50)
            print(f"MÉTODO 1 (Requests + BS4):")
            print(f"   - Tempo Médio: {media_tempo_req:.2f} segundos")
            print(f"   - Consumo Médio de RAM do script: {media_mem_req:.2f} MB")
            print("-" * 50)
            print(f"MÉTODO 2 (Selenium Headless):")
            print(f"   - Tempo Médio: {media_tempo_sel:.2f} segundos")
            print(f"   - Consumo Médio de RAM (Python): {media_mem_sel:.2f} MB")
            print("-" * 50)
            
            ganho_performance = (media_tempo_sel / media_tempo_req)
            print(f"🚀 O método novo (Requests) foi cerca de {ganho_performance:.1f}x MAIS RÁPIDO!")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n[AVISO] Não foi possível rodar o teste do Selenium. Detalhes: {e}")
            print("Provavelmente o chromedriver foi deletado. Você pode preencher a tabela usando os dados reais do Requests coletados acima!")

    else:
        print("\n[Aviso] Chromedriver não encontrado. Rodando apenas o teste do Requests.")