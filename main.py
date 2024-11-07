from load import upload_to_bigquery
from extract import extract_data
from dotenv import load_dotenv
from loguru import logger
import os

def main():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()  
    logger.add("log\\main.log", rotation="10 MB") 
    try:
        # Chama a função de extração de dados
        csv_file_path = extract_data() 
        logger.info(f"Arquivo CSV extraído: {csv_file_path}")

        # Defina os parâmetros para o BigQuery
        table_id = "sylvan-mode-441000-p3.prices.steam_prices"  # ID da tabela no BigQuery
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Caminho para as credenciais do Google

        # Chama a função para fazer o upload no BigQuery
        upload_to_bigquery(csv_file_path, table_id, credentials_path,replace=True)
        logger.info("Processo de upload concluído com sucesso.")
    except Exception as e:
        logger.error(f"Ocorreu um erro durante o processo de ETL: {e}")

if __name__ == "__main__":
    main()

