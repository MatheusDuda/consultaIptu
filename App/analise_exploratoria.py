import pandas as pd
import os

def analise_exploratoria():
    try:
        # Carrega os dados
        caminho_arquivo = os.path.join(os.path.dirname(__file__), "iptu-bairro.csv")
        df = pd.read_csv(caminho_arquivo, sep=";", encoding="utf-8", dtype=str)
        
        print("ANALISE EXPLORATORIA - IPTU BELO HORIZONTE 2022")
        print("=" * 50)
        
        # Converte formatos brasileiros
        df['VALOR_NUMERICO'] = df['VALOR_TOTAL_LANCADO'].str.replace('.', '').str.replace(',', '.').astype(float)
        df['QDE_NUMERICO'] = df['QDE_LANCAMENTOS'].str.replace('.', '').astype(int)
        
        print("\nESTATISTICAS GERAIS:")
        print(f"   Total de bairros: {len(df)}")
        print(f"   Valor total lancado: R$ {df['VALOR_NUMERICO'].sum():,.2f}")
        print(f"   Media por bairro: R$ {df['VALOR_NUMERICO'].mean():,.2f}")
        print(f"   Maior valor: R$ {df['VALOR_NUMERICO'].max():,.2f}")
        print(f"   Menor valor: R$ {df['VALOR_NUMERICO'].min():,.2f}")
        print(f"   Total de lancamentos: {df['QDE_NUMERICO'].sum():,}")
        
        print("\nTOP 10 BAIRROS COM MAIOR VALOR LANCADO:")
        top10_valor = df.nlargest(10, 'VALOR_NUMERICO')[['BAIRRO', 'VALOR_NUMERICO', 'QDE_NUMERICO']]
        for i, row in top10_valor.iterrows():
            valor_formatado = f"R$ {row['VALOR_NUMERICO']:,.2f}"
            print(f"   {row['BAIRRO']:<25} {valor_formatado:>20} ({row['QDE_NUMERICO']} lancamentos)")
        
        print("\nTOP 10 BAIRROS COM MAIS LANÇAMENTOS:")
        top10_qde = df.nlargest(10, 'QDE_NUMERICO')[['BAIRRO', 'QDE_NUMERICO', 'VALOR_NUMERICO']]
        for i, row in top10_qde.iterrows():
            valor_formatado = f"R$ {row['VALOR_NUMERICO']:,.2f}"
            print(f"   {row['BAIRRO']:<25} {row['QDE_NUMERICO']:>6} lancamentos {valor_formatado:>20}")
        
        # Tenta gerar grafico se matplotlib estiver disponivel
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(12, 8))
            
            # Grafico 1: Top 10 bairros por valor
            plt.subplot(2, 1, 1)
            top10 = df.nlargest(10, 'VALOR_NUMERICO')
            plt.barh(top10['BAIRRO'], top10['VALOR_NUMERICO'] / 1e6)
            plt.xlabel('Valor (Milhoes R$)')
            plt.title('Top 10 Bairros - Maior Valor de IPTU 2022')
            plt.gca().invert_yaxis()
            
            # Grafico 2: Distribuicao por faixas
            plt.subplot(2, 1, 2)
            faixas = [0, 1000000, 5000000, 10000000, 50000000, float('inf')]
            labels = ['Ate 1M', '1M-5M', '5M-10M', '10M-50M', 'Acima 50M']
            df['FAIXA'] = pd.cut(df['VALOR_NUMERICO'], bins=faixas, labels=labels)
            distribuicao = df['FAIXA'].value_counts()
            distribuicao.plot(kind='bar')
            plt.xlabel('Faixa de Valor')
            plt.ylabel('Quantidade de Bairros')
            plt.title('Distribuicao de Bairros por Faixa de Valor')
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            plt.savefig('analise_iptu.png', dpi=300, bbox_inches='tight')
            print("\nGrafico salvo como 'analise_iptu.png'")
            
        except ImportError:
            print("\nMatplotlib nao disponivel. Graficos nao gerados.")
            
    except Exception as e:
        print(f"Erro na analise: {e}")

if __name__ == "__main__":
    analise_exploratoria()