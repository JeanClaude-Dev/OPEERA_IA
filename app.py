import streamlit as st
from groq import Groq
import os

# Configuração inicial da página
st.set_page_config(page_title="OPEERA - Tutor Inteligente", page_icon="🎓", layout="centered")

# --- ESTILIZAÇÃO PERSONALIZADA (CSS) ---
st.markdown(f"""
    <style>
    /* Cor principal nos títulos da Sidebar */
    [data-testid="stSidebar"] h1 {{
        color: #07b458;
        font-weight: 800;
    }}
    
    /* Customização das mensagens do Chat */
    .stChatMessage {{
        border-radius: 15px;
        margin-bottom: 10px;
    }}
    
    /* Borda de destaque na mensagem do assistente */
    [data-testid="stChatMessageAssistant"] {{
        border: 1px solid #07b458;
        background-color: #f9fffb;
    }}

    /* Estilização do Botão de Reiniciar */
    .stButton>button {{
        width: 100%;
        border-radius: 20px;
        border: 1px solid #07b458;
        color: #07b458;
        background-color: transparent;
    }}
    
    .stButton>button:hover {{
        background-color: #07b458;
        color: white;
    }}

    /* Cor do Spinner e elementos de carregamento */
    .stSpinner > div {{
        border-top-color: #07b458 !important;
    }}
    
    /* Ajuste da barra lateral */
    [data-testid="stSidebar"] {{
        background-color: #ffffff;
        border-right: 1px solid #eee;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave 'GROQ_API_KEY' não encontrada.")
    st.stop()

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Logo e Título
    st.image("logo.png", use_column_width=True)
    st.title("Área do Aluno")
    
    # Menu de Matérias com ícone monocromático
    materia = st.selectbox(
        "📚 O que vamos estudar hoje?",
        ("Geral", "Matemática", "Português", "História e Geografia", "Ciências e Biologia")
    )
    
    prompts_especificos = {
        "Geral": "Você é um tutor educacional versátil da Opee Educação. Explique de forma didática.",
        "Matemática": "Você é um professor de matemática. Use LaTeX e mostre o passo a passo.",
        "Português": "Você é um professor de gramática. Foque na norma culta e clareza.",
        "História e Geografia": "Você é um professor de humanidades. Foque em contextos e causas.",
        "Ciências e Biologia": "Você é um professor de ciências. Use analogias práticas."
    }
    
    st.divider()
    if st.button("Limpar Histórico"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Desenvolvido por: Jcb | Opee Educação")

# --- INICIALIZAÇÃO DO HISTÓRICO ---
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "system", "content": f"{prompts_especificos[materia]} Responda sempre em português. Seja encorajador."}
    ]

# --- INTERFACE DE CHAT ---
st.markdown(f"<h3 style='color: #444;'>Assistente de {materia}</h3>", unsafe_allow_html=True)

# Exibir histórico (usando ícones cinzas para manter o foco no verde do layout)
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# --- LÓGICA DE INTERAÇÃO ---
if prompt := st.chat_input("Escreva sua dúvida aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("OPEERA está processando..."):
            try:
                chat_completion = client.chat.completions.create(
                    messages=st.session_state.messages,
                    model="llama-3.1-8b-instant",
                    temperature=0.6,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Erro de conexão: {e}")