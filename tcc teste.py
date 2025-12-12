import streamlit as st
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gerando Caixas Pitagóricas ", layout="wide")

# --- FUNÇÕES LÓGICAS (Do seu código original) ---
def gerar_caixa_pitagorica(m, n, k):
    """
    Gera as dimensões da caixa baseada nas fórmulas do TCC.
    """
    a = 2 * m * k
    b = 2 * n * k
    c = m * m + n * n - k * k
    d = m * m + n * n + k * k
    return a, b, c, d

def verificar_primitividade(a, b, c):
    """
    Verifica se a caixa é primitiva (MDC(a, b, c) == 1).
    """
    mdc_geral = math.gcd(a, math.gcd(b, c))
    return mdc_geral == 1, mdc_geral

def vertices_paralelepipedo(a, b, c):
    V = [
        (0, 0, 0), (a, 0, 0), (a, b, 0), (0, b, 0),
        (0, 0, c), (a, 0, c), (a, b, c), (0, b, c),
    ]
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0), 
        (4, 5), (5, 6), (6, 7), (7, 4), 
        (0, 4), (1, 5), (2, 6), (3, 7), 
    ]
    return V, edges

# --- INTERFACE WEB (STREAMLIT) ---

st.title("📦 Gerador de Caixas Pitagóricas ")
st.markdown("Uma Visão Computacional Para Gerar Caixas Pitagóricas")

# Barra Lateral para Entradas
st.sidebar.header("Parâmetros de Entrada")
m = st.sidebar.number_input("Valor de m", value=1, step=1)
n = st.sidebar.number_input("Valor de n", value=1, step=1)
k = st.sidebar.number_input("Valor de k", value=1, step=1)

# Inicializar o histórico na sessão se não existir
if 'historico' not in st.session_state:
    st.session_state.historico = []

# Botão de Gerar
if st.sidebar.button("Gerar Caixa", type="primary"):
    # Validações
    erro = None
    if k == 0:
        erro = "O valor de 'k' deve ser diferente de zero."
    elif (m**2 + n**2) <= k**2:
        erro = f"Erro Geométrico: m² + n² ({m**2 + n**2}) deve ser maior que k² ({k**2}) para que 'c' seja positivo."
    
    if erro:
        st.error(erro)
    else:
        # Cálculos
        a, b, c, d = gerar_caixa_pitagorica(m, n, k)
        eh_primitiva, mdc_val = verificar_primitividade(a, b, c)
        status_prim = "Sim" if eh_primitiva else f"Não (MDC={mdc_val})"
        
        # Salvar no histórico
        novo_dado = {
            "m": m, "n": n, "k": k,
            "a": a, "b": b, "c": c,
            "Diagonal (d)": d,
            "Primitiva?": status_prim
        }
        st.session_state.historico.insert(0, novo_dado) # Adiciona no topo

# --- EXIBIÇÃO DOS RESULTADOS ---

# Layout de Colunas: Esquerda (Gráfico) | Direita (Tabela)
col_grafico, col_dados = st.columns([1, 1.2])

with col_grafico:
    st.subheader("Visualização 3D")
    if st.session_state.historico:
        # Pega o último dado gerado (o primeiro da lista)
        ultimo = st.session_state.historico[0]
        a, b, c = ultimo['a'], ultimo['b'], ultimo['c']
        prim_bool = True if ultimo['Primitiva?'] == "Sim" else False
        
        # Plotagem
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection='3d')
        
        V, edges = vertices_paralelepipedo(a, b, c)
        cor_arestas = 'blue' if prim_bool else 'gray'
        
        # Desenha arestas
        for i, j in edges:
            ax.plot(
                [V[i][0], V[j][0]], 
                [V[i][1], V[j][1]], 
                [V[i][2], V[j][2]], 
                color=cor_arestas
            )
            
        # Desenha diagonal
        ax.plot([0, a], [0, b], [0, c], color="red", linestyle="--", label="Diagonal")
        
        # Configurações do gráfico
        ax.set_title(f"Caixa {'PRIMITIVA' if prim_bool else 'DERIVADA'}: {a}x{b}x{c}")
        ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
        
        # Ajuste de escala (para não distorcer)
        max_dim = max(a, b, c)
        ax.set_xlim(0, max_dim); ax.set_ylim(0, max_dim); ax.set_zlim(0, max_dim)
        
        st.pyplot(fig)
    else:
        st.info("Insira os parâmetros e clique em 'Gerar Caixa' para visualizar.")

with col_dados:
    st.subheader("Histórico de Cálculos")
    if st.session_state.historico:
        # Transforma a lista em Tabela (DataFrame)
        df = pd.DataFrame(st.session_state.historico)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:

        st.text("Nenhum cálculo realizado ainda.")
