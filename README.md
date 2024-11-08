# Steam DB ETL

Este é um projeto de ETL (Extract, Transform, Load) para extrair dados de jogos da Steam via web scraping utilizando Selenium, transformá-los e carregá-los em uma tabela do Google BigQuery. O projeto é baseado em Python e utiliza diversas bibliotecas para facilitar o processo.

[Link](https://docs.google.com/spreadsheets/d/19VIHAI2io0SyPuBggWFceqJ22lAth5IFkwhpKkUA1oE/edit?gid=1285333755#gid=1285333755) para acessar Google Sheets conectado ao BigQuery

## Funcionalidades

- **Extração de Dados**: Coleta informações de jogos da Steam via web scraping com Selenium.
- **Transformação de Dados**: Manipula e organiza os dados extraídos para carregá-los em formato CSV.
- **Carregamento no BigQuery**: Carrega os dados transformados na tabela do BigQuery, com a opção de substituir ou anexar dados existentes.

## Pré-requisitos

Antes de começar, é necessário ter os seguintes pré-requisitos instalados:

- Python 3.x
- Conta na Google Cloud Platform com permissões para acessar BigQuery.

## Configuração

1. **Configuração do Google Cloud (BigQuery)**:
   - Crie um projeto na Google Cloud Platform (GCP).
   - Habilite a API do BigQuery.
   - Crie uma chave de serviço (`.json`) e configure o caminho da chave como variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`.

2. **Arquivo `.env`**:
   - Crie um arquivo `.env` no diretório raiz do projeto para armazenar variáveis de ambiente.
   - Exemplo de configuração do `.env`:
   
   ```ini
   GOOGLE_APPLICATION_CREDENTIALS=/caminho/para/seu/arquivo/credentials.json
   ```

## Como Rodar

### Passo 1: Extração de Dados

A função `extract_data()` é responsável por extrair dados de jogos da Steam via web scraping com o Selenium. Ela irá salvar os dados no formato CSV.

```python
csv_file_path = extract_data()
```

### Passo 2: Transformação (opcional)

Os dados extraídos podem ser manipulados e transformados com `pandas` ou outras ferramentas que você desejar.

### Passo 3: Carregar para o BigQuery

Chame a função `upload_to_bigquery()` para carregar os dados para o BigQuery. Você pode decidir se deseja **substituir** ou **anexar** os dados à tabela existente.

```python
upload_to_bigquery(csv_file_path, table_id, credentials_path, replace=True)
```

Parâmetros da função:
- `csv_file_path`: Caminho para o arquivo CSV que contém os dados.
- `table_id`: ID da tabela no BigQuery no formato `projeto.dataset.tabela`.
- `credentials_path`: Caminho para o arquivo de credenciais do Google Cloud.
- `replace`: Se `True`, substitui os dados existentes. Se `False`, anexa os dados.

### Passo 4: Execução

Execute o script `main.py` para rodar o processo de ETL completo (Extração, Transformação e Carregamento):

```bash
python main.py
```

## Logs

Os logs do processo são armazenados no arquivo `load.log` (configurado com `loguru`), onde você pode acompanhar o progresso do processo de carregamento de dados no BigQuery.

## Estrutura de Diretórios

```plaintext
steamDbETL/
│
├── .git                       # git
├── log                        # Alguns arquivos de log
├── .gitignore                 # Gitignore
├── extract.py                 # Código para extração dos dados via Selenium
├── load.py                    # Código para carregar dados no BigQuery
├── main.py                    # Script principal
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências do projeto
└── steam_sales.csv            # Arquivo csv do primeiro resultado
```


