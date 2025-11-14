"""
Converte a planilha do IBGE com os municípios do Brasil para um banco de dados SQLite.
"""

import pandas as pd

# Configurações
EXCEL_FILE = "RELATORIO_DTB_BRASIL_2024_MUNICIPIOS.xls"
DB_FILE = "municipios_brasil.db"
TABLE_NAME = "municipios"

# Dicionário com abreviações dos estados brasileiros
ESTADOS_ABREV = {
    "Acre": "AC",
    "Alagoas": "AL",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Bahia": "BA",
    "Ceará": "CE",
    "Distrito Federal": "DF",
    "Espírito Santo": "ES",
    "Goiás": "GO",
    "Maranhão": "MA",
    "Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Minas Gerais": "MG",
    "Pará": "PA",
    "Paraíba": "PB",
    "Paraná": "PR",
    "Pernambuco": "PE",
    "Piauí": "PI",
    "Rio de Janeiro": "RJ",
    "Rio Grande do Norte": "RN",
    "Rio Grande do Sul": "RS",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Santa Catarina": "SC",
    "São Paulo": "SP",
    "Sergipe": "SE",
    "Tocantins": "TO",
}


def ler_dados_excel(excel_file: str) -> pd.DataFrame:
    """Lê os dados do arquivo Excel e retorna um DataFrame."""
    print(f"Lendo dados do arquivo Excel: {excel_file}")
    df = pd.read_excel(excel_file)
    print(f"Dados lidos: {len(df)} linhas, {len(df.columns)} colunas")
    return df


def salvar_sqlite(df: pd.DataFrame):
    """Abrir o banco de dados SQLite e salvar os dados"""

    import sqlite3

    conn = sqlite3.connect(DB_FILE)
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Dados salvos no banco de dados SQLite: {DB_FILE}, tabela: {TABLE_NAME}")


if __name__ == "__main__":
    df = ler_dados_excel(EXCEL_FILE)

    ## Limpeza básica dos dados
    df = df.iloc[
        5:, :-1
    ]  # pula as primeiras 5 linhas de metadados e remove a última coluna vazia

    df.columns = df.iloc[0]  # define a primeira linha como cabeçalho
    df = df.iloc[1:]  # remove a primeira linha (antigo cabeçalho)

    df = df.reset_index(drop=True)

    # Cria coluna com abreviação do estado
    df["UF"] = df["Nome_UF"].map(ESTADOS_ABREV)

    # Normaliza os nomes das cidades para busca na coluna 'nome_normalizado'
    df["nome_normalizado"] = (
        df["Nome_Município"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
        .str.lower()
    )

    print(df["Nome_Município"].head(10))
    print(df["nome_normalizado"].head(10))
    print(df["UF"].head(10))

    print(df.head(10))
    # print(df.columns)
    salvar_sqlite(df)
