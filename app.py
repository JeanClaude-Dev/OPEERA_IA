import streamlit as st
from groq import Groq
import os

# Configuração inicial da página
st.set_page_config(page_title="OPEERA - Tutor Inteligente da Opee Educação", page_icon="🎓", layout="centered")

# --- ESTILIZAÇÃO PARA UM LOOK PROFISSIONAL ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #f0f2f6; }
    .stChatInput { border-radius: 10px; }
    [data-testid="stSidebar"] { background-color: #f8f9fa; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave 'GROQ_API_KEY' não encontrada nos Secrets do Streamlit.")
    st.stop()

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Espaço para o Logo (Se tiver o arquivo no GitHub, descomente a linha abaixo)
     st.image("logo.png", use_column_width=True)
    
    st.title("🎓 Área do Aluno")
    st.subheader("Configurações de Estudo")
    
    # Menu de Matérias
    materia = st.selectbox(
        "Sobre o que vamos estudar hoje?",
        ("Geral", "Matemática", "Português", "História e Geografia", "Ciências e Biologia")
    )
    
    # Ajuste do System Prompt baseado na matéria
    prompts_especificos = {
        "Geral": "Você é um tutor educacional versátil. Explique tudo de forma didática.",
        "Matemática": "Você é um professor de matemática. Use fórmulas em LaTeX, mostre o passo a passo dos cálculos e dê exercícios extras.",
        "Português": "Você é um professor de gramática e literatura. Foque na norma culta, explique regras ortográficas e dê exemplos de frases.",
        "História e Geografia": "Você é um historiador e geógrafo. Use contextos temporais, cause-consequência e descrições espaciais.",
        "Ciências e Biologia": "Você é um cientista. Use termos técnicos explicando seus significados e faça analogias com o mundo real."
    }
    
    st.divider()
    if st.button("🗑️ Reiniciar Conversa"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Desenvolvido por: Jcb")

# --- INICIALIZAÇÃO DO HISTÓRICO ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "system", "content": f"{prompts_especificos[materia]} Responda sempre em português. Seja encorajador e paciente."}
    ]

# --- INTERFACE DE CHAT ---
st.write(f"### Assistente de **{materia}**")

# Exibir histórico de mensagens
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- LÓGICA DE INTERAÇÃO ---
if prompt := st.chat_input("Como posso te ajudar com essa matéria?"):
    # Adiciona mensagem do aluno
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Chamada para a IA (Groq)
    with st.chat_message("assistant"):
        with st.spinner("Preparando explicação..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3-8b-8192", # Modelo ultra rápido e grátis
                    temperature=0.6,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Salva a resposta da IA na memória
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erro ao conectar com o servidor: {e}")