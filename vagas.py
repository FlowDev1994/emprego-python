import os
import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# -----------------------
# CONFIGURAÇÕES
# -----------------------
KEYWORDS = "programador python"
MAX_VAGAS_POR_EXECUCAO = 15
PASTA_SALVAR = os.path.expanduser("~/Área de trabalho/Devs/Projetos/vagas")
CSV_PATH = os.path.join(PASTA_SALVAR, "vagas_aplicadas.csv")

# URL Filtrada (Remoto + Easy Apply + Júnior + Brasil)
BASE_URL = f"https://www.linkedin.com/jobs/search/?keywords={KEYWORDS}&f_AL=true&f_WT=2&f_E=2&geoId=106057199&location=Brasil"

# -----------------------
# INICIAR DRIVER
# -----------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("detach", True) # Mantém navegador aberto

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

def processar_modal():
    """
    Função inteligente que clica em Avançar/Revisar até achar o Enviar.
    Se travar (perguntas), pede ajuda ao usuário.
    """
    tentativas = 0
    max_passos = 10 # Evita loop infinito se algo der errado
    
    while tentativas < max_passos:
        time.sleep(1.5) # Respira entre passos
        
        # 1. Tenta Encontrar Botão de ENVIAR (Sucesso)
        botoes_enviar = driver.find_elements(By.XPATH, "//button[contains(., 'Enviar candidatura') or contains(., 'Submit application')]")
        if botoes_enviar:
            try:
                botoes_enviar[0].click()
                print("   🚀 [SUCESSO] Botão 'Enviar' clicado!")
                time.sleep(2)
                # Tenta fechar popup de 'vaga enviada'
                try: driver.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss']").click()
                except: pass
                return "Enviada Auto"
            except:
                pass # Se falhar clique, tenta lógica abaixo

        # 2. Tenta Encontrar Botão AVANÇAR ou REVISAR
        botoes_avancar = driver.find_elements(By.XPATH, "//button[contains(., 'Avançar') or contains(., 'Next') or contains(., 'Revisar') or contains(., 'Review')]")
        
        if botoes_avancar:
            botao = botoes_avancar[0]
            try:
                # Tenta clicar em Avançar
                botao.click()
                print(f"   ➡️ Passo {tentativas+1}: Clicou em 'Avançar/Revisar'...")
                
                # Verifica se avançou mesmo ou se travou (validação de perguntas)
                time.sleep(1)
                # Se o botão avançar continuar visível e habilitado, provavelmente travou numa pergunta obrigatória
                # Mas cuidado: às vezes o botão avançar da PRÓXIMA tela é igual.
                # Vamos deixar o fluxo seguir. Se ele não conseguir terminar em 'max_passos', pede ajuda.
            except:
                print("   ⚠️ Erro ao clicar em Avançar.")
        else:
            # Se não tem botão enviar nem avançar, pode ser que tenha acabado ou travado.
            pass

        tentativas += 1

    # SE SAIU DO LOOP SEM ENVIAR:
    # Provavelmente caiu na tela de PERGUNTAS ou ERRO.
    print("\n   🛑 [INTERVENÇÃO NECESSÁRIA] Pausa para perguntas ou erro.")
    print("   👉 Preencha manualmente no navegador e finalize a candidatura.")
    input("   🟢 Quando terminar essa vaga, pressione ENTER aqui para continuar para a próxima...")
    return "Manual/Misto"

try:
    # LOGIN
    driver.get("https://www.linkedin.com/login")
    print("\n🔴 [AÇÃO] Faça login manualmente.")
    input("🟢 Pressione ENTER aqui APÓS ver o feed de notícias...")

    # BUSCAR
    driver.get(BASE_URL)
    time.sleep(4)

    # LISTAR VAGAS
    possible_selectors = [".jobs-search-results__list-item", ".scaffold-layout__list-item", ".job-card-container"]
    vagas = []
    used_selector = ""
    for sel in possible_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if len(els) > 0:
            vagas = els
            used_selector = sel
            break
    
    if not vagas:
        print("❌ Nenhuma vaga encontrada na lista lateral.")
        exit()

    # CRIAR CSV
    if not os.path.isfile(CSV_PATH):
        with open(CSV_PATH, mode="w", encoding="utf-8") as f:
            csv.writer(f).writerow(["Data", "Titulo", "Status"])

    # LOOP DE VAGAS
    for i in range(MAX_VAGAS_POR_EXECUCAO):
        print(f"\n-------------------------------------------------")
        # Recarrega elementos
        vagas = driver.find_elements(By.CSS_SELECTOR, used_selector)
        if i >= len(vagas): break
        
        card = vagas[i]
        
        # Clica na vaga
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", card)
            time.sleep(1)
            card.click()
            time.sleep(2)

            # Pega Título
            try: titulo = driver.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__job-title h1").text
            except: titulo = "Vaga sem título"
            
            print(f"💼 [{i+1}/{MAX_VAGAS_POR_EXECUCAO}] Processando: {titulo}")

            # Clica Easy Apply
            try:
                apply_btn = driver.find_element(By.CSS_SELECTOR, ".jobs-apply-button--top-card button")
                driver.execute_script("arguments[0].click();", apply_btn)
                time.sleep(1)
                
                # CHAMA A FUNÇÃO QUE LIDA COM O MODAL
                status_final = processar_modal()

            except Exception as e:
                print(f"   🚫 Botão 'Candidatura Simplificada' não disponível ou erro: {e}")
                status_final = "Pulada/Já aplicada"

            # Salva log
            with open(CSV_PATH, mode="a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([datetime.now(), titulo, status_final])

        except Exception as e:
            print(f"Erro genérico na vaga {i}: {e}")

except Exception as e:
    print(f"Erro fatal: {e}")

print("\n🏁 Execução finalizada.")



# MINHAS ANOTAÇÕES PARA RODAR O CÓDIGO:

# Entrar na pasta onde esta o código (com o terminal) - Area de trabalho/Devs/Projetos/vagas 
# cd ~/Área\ de\ trabalho/Devs/Projetos/vagas
# source venv/bin/activate
# python3 vagas_v4_final.py
