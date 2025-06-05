import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from datetime import datetime

def carregar_dados():
    """Carrega e retorna o dataset de COVID-19"""
    print("\nCarregando Dataset criado com dados da COVID disponiveis em https://brasil.io/dataset/covid19/files/")
    
    try:
        df = pd.read_csv('covid_janeiro_fevereiro_2022_por_estado.csv', parse_dates=['data'])
        print("\nDataset carregado com sucesso! Primeiras linhas:")
        print(df.head())
        return df
    except Exception as e:
        print(f"\nErro ao carregar o arquivo: {e}")
        exit()

def visualizacao_temporal(df):
    """Gráfico de linhas: Evolução temporal para um estado específico"""
    print("\nGerando visualização temporal...")
    
    estado_alvo = 'SP'
    df_estado = df[df['estado'] == estado_alvo]
    
    plt.figure(figsize=(12, 6))
    plt.plot(df_estado['data'], df_estado['casos'], 'r-o', label='Casos')
    plt.plot(df_estado['data'], df_estado['mortes'], 'b--s', label='Mortes')
    
    plt.title(f'Evolução de COVID-19 em {estado_alvo} (Jan-Fev/2022)')
    plt.xlabel('Data')
    plt.ylabel('Contagem')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    
    plt.savefig(f'covid_{estado_alvo}_linhas.png', dpi=300, bbox_inches='tight')
    print(f"Gráfico temporal salvo como 'covid_{estado_alvo}_linhas.png'")
    plt.show()

def visualizacao_barras(df):
    """Gráfico de barras: Casos por estado"""
    print("\nGerando visualização de barras...")
    
    casos_por_estado = df.groupby('estado')['casos'].sum().sort_values()
    
    plt.figure(figsize=(10, 8))
    casos_por_estado.plot(
        kind='barh',
        color='skyblue',
        edgecolor='black'
    )
    
    plt.title("Total de Casos de COVID-19 por Estado (Jan-Fev/2022)", fontsize=14)
    plt.xlabel("Número de Casos", fontsize=12)
    plt.ylabel("Estado", fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('casos_por_estado_barras.png', dpi=300)
    print("Gráfico de barras salvo como 'casos_por_estado_barras.png'")
    plt.show()

def visualizacao_mapa(df):
    """Mapa Choropleth: Distribuição geográfica dos casos"""
    print("\nGerando visualização geográfica...")
    
    try:
        df_estados = df.groupby('estado').agg({'casos': 'sum', 'mortes': 'sum'}).reset_index()
        brasil_map = gpd.read_file('brasil.geojson')
        
        brasil_map = brasil_map.merge(df_estados, left_on='sigla', right_on='estado')
        
        fig, ax = plt.subplots(1, figsize=(12, 8))
        brasil_map.plot(column='casos', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)
        ax.set_title('Casos de COVID-19 por Estado (Jan-Fev/2022)', fontsize=16)
        ax.axis('off')
        
        plt.savefig('mapa_covid_brasil.png', dpi=300, bbox_inches='tight')
        print("Mapa geográfico salvo como 'mapa_covid_brasil.png'")
        plt.show()
    except Exception as e:
        print(f"Erro ao gerar mapa: {e}\nCertifique-se que o arquivo 'brasil.geojson' está na pasta.")

def main():
    """Função principal que executa todas as visualizações"""
    print("=== Visualização de Dados COVID-19 (Jan-Fev/2022) ===")
    
    df = carregar_dados()
    
    # Executa as visualizações sequencialmente
    visualizacao_temporal(df)
    visualizacao_barras(df)
    visualizacao_mapa(df)
    
    print("\nProcesso concluído! Verifique os arquivos gerados na pasta.")

if __name__ == "__main__":
    main()