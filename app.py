
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração do app
st.set_page_config(page_title="Previsão de Queda - Aviator", layout="centered")
st.markdown("<h1 style='text-align: center; color: #0047AB;'>Previsão de Queda - Aviator</h1>", unsafe_allow_html=True)

# Instruções ao usuário
with st.expander("**Como usar o app**"):
    st.markdown("""
    - Insira o tempo que o Aviator subiu (ex: 1.50, 2.30, 3.75).
    - Clique em **Adicionar** para registrar.
    - Veja a média, gráfico de tendência e alertas inteligentes.
    - Baixe o histórico como CSV se quiser guardar os dados.
    """)

# Inicialização de sessão
if "valores" not in st.session_state:
    st.session_state.valores = []

# Entrada de dados
col1, col2 = st.columns([2, 1])
with col1:
    novo_valor = st.text_input("Tempo de subida do avião (ex: 1.50):", "")
with col2:
    if st.button("Adicionar", use_container_width=True):
        try:
            valor = float(novo_valor)
            st.session_state.valores.append(valor)
            st.success(f"Valor {valor} adicionado com sucesso!")
        except ValueError:
            st.error("Por favor, insira um número válido (ex: 2.30)")

# Exibir resultados
if st.session_state.valores:
    df = pd.DataFrame(st.session_state.valores, columns=["Valor"])
    media = df["Valor"].mean()

    st.subheader("Média Atual:")
    cor = "green" if media > 3 else "orange" if media > 2 else "red"
    st.markdown(f"<h3 style='color:{cor}; text-align:center;'>{media:.2f}x</h3>", unsafe_allow_html=True)

    st.subheader("Gráfico de Tendência:")
    fig, ax = plt.subplots()
    ax.plot(df["Valor"], marker='o', linestyle='-')
    ax.axhline(media, color='blue', linestyle='--', label=f"Média ({media:.2f})")
    ax.set_ylabel("Valor")
    ax.set_xlabel("Tentativas")
    ax.set_title("Evolução dos Valores")
    ax.legend()
    st.pyplot(fig)

    # Lógica de alerta inteligente
    st.subheader("Alerta Inteligente:")
    if len(df) >= 3 and all(df["Valor"].iloc[-3:] < 2):
        st.warning("Alerta: 3 quedas consecutivas abaixo de 2.0 detectadas!")
    elif df["Valor"].iloc[-1] < 1.5:
        st.info("Último valor muito baixo. Atenção!")

    # Histórico e download
    st.subheader("Histórico de Valores:")
    st.dataframe(df.style.applymap(lambda v: "background-color: red" if v < 2 else "background-color: lightgreen"))

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar histórico em CSV", data=csv, file_name="historico_aviator.csv", mime="text/csv")
else:
    st.info("Insira pelo menos um valor para ver os resultados.")
