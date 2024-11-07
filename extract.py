from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from loguru import logger

# Função para rolar a página até o final
def scroll_down_page(driver, speed=10):
    current_scroll_position, new_height = 0, 1
    while current_scroll_position <= new_height:
        current_scroll_position += speed
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        new_height = driver.execute_script("return document.body.scrollHeight")

# Função para extrair os dados do SteamDB
def extract_data():
    # Configuração do Loguru
    logger.add("log\\steamdb_extraction.log", rotation="10 MB")

    # Inicializar o navegador com Selenium usando o ChromeDriver
    logger.info("Iniciando o navegador Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    logger.info("Navegador iniciado com sucesso.")

    # Acessa o site
    url = "https://steamdb.info/sales/"
    driver.get(url)
    logger.info("Acessando o site SteamDB para extração de dados...")

    # Espera alguns segundos para garantir que a página e os elementos foram carregados
    scroll_down_page(driver)
    time.sleep(7)

    # Inicializa a lista para armazenar os dados
    games = []

    # Seleciona as linhas da tabela de jogos
    game_rows = driver.find_elements(By.CSS_SELECTOR, "tr.app")
    logger.info(f"{len(game_rows)} linhas de jogos encontradas.")
    
    for row in game_rows:
        # Extraindo informações de cada coluna usando seletores CSS
        name = row.find_element(By.CSS_SELECTOR, "a.b").text.strip() if row.find_elements(By.CSS_SELECTOR, "a.b") else None
        desconto = row.find_element(By.CSS_SELECTOR, "td.price-discount, td.price-discount-major").text.strip() if row.find_elements(By.CSS_SELECTOR, "td.price-discount, td.price-discount-major") else None
        preco = row.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")[2].text.strip() if len(row.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")) > 2 else None
        rating = row.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")[3].text.strip() if len(row.find_elements(By.CSS_SELECTOR, "td.dt-type-numeric")) > 3 else None
        ends = row.find_elements(By.CSS_SELECTOR, "td.timeago")[0].text.strip() if len(row.find_elements(By.CSS_SELECTOR, "td.timeago")) > 0 else None
        started = row.find_elements(By.CSS_SELECTOR, "td.timeago")[1].text.strip() if len(row.find_elements(By.CSS_SELECTOR, "td.timeago")) > 1 else None

        # Adiciona o dicionário com os dados do jogo à lista
        games.append({
            "name": name,
            "desconto": desconto,
            "preço": preco,
            "rating": rating,
            "ends": ends,
            "started": started
        })

    logger.info("Extração de dados concluída.")

    # Converte a lista para DataFrame e salva em CSV
    df = pd.DataFrame(games)
    df.to_csv("steam_sales.csv", index=False)
    logger.info("Dados extraídos e salvos em steam_sales.csv")

    # Fechar o navegador
    driver.quit()
    logger.info("Navegador fechado.")
    
    return "steam_sales.csv"
