from google.cloud import bigquery
from google.oauth2 import service_account
from loguru import logger


def upload_to_bigquery(csv_file_path: str, table_id: str, credentials_path: str, replace: bool = False):
    """
    Função para carregar um arquivo CSV para o BigQuery.

    Args:
        csv_file_path (str): Caminho para o arquivo CSV a ser carregado.
        table_id (str): ID da tabela no BigQuery no formato 'projeto.dataset.tabela'.
        credentials_path (str): Caminho para o arquivo de credenciais do Google Cloud.

    Returns:
        None
    """
    # Configuração do Loguru
    logger.add("log\\steamdb_load.log", rotation="10 MB")  # Log rotacionado quando atingir 10 MB
    logger.info("Iniciando o processo de upload para o BigQuery...")

    try:
        # Carregar as credenciais a partir do arquivo JSON
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/bigquery"]
        )

        # Inicializar o cliente do BigQuery
        client = bigquery.Client(credentials=credentials)

        # Configurar o job de carga
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # Ignorar a primeira linha de cabeçalho
            autodetect=True  # Detecta automaticamente os tipos de dados
        )

        if replace:
            # Substituir os dados existentes na tabela
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
            logger.info(f"Substituindo os dados na tabela {table_id}...")
        else:
            # Anexar os novos dados à tabela existente
            job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
            logger.info(f"Anexando os dados na tabela {table_id}...")

        # Carregar o arquivo CSV para o BigQuery
        with open(csv_file_path, "rb") as source_file:
            load_job = client.load_table_from_file(source_file, table_id, job_config=job_config)

        # Aguardar a conclusão do job
        load_job.result()

        logger.info(f"Dados carregados com sucesso na tabela {table_id}.")

    except Exception as e:
        logger.error(f"Ocorreu um erro ao carregar os dados para o BigQuery: {e}")
        raise 


