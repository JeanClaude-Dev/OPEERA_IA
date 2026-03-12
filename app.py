import streamlit as st
from groq import Groq
import os

# Configuração inicial da página
st.set_page_config(page_title="OPEERA - Tutor Inteligente", page_icon="🎓", layout="centered")

# --- ESTILIZAÇÃO PERSONALIZADA (CSS) ---
st.markdown(f"""
    <style>
    /* Estilo para o Título OPEERA com Tooltip */
    .tooltip {{
        position: relative;
        display: inline-block;
        font-size: 42px;
        font-weight: 800;
        color: #07b458; 
        margin-bottom: 5px;
        cursor: help;
    }}

    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 280px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 110%; 
        left: 0%;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        font-weight: normal;
        line-height: 1.4;
    }}

    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}

    /* Cor do Título Área do Aluno na Sidebar (Verde OPEE) */
    [data-testid="stSidebar"] h1 {{
        color: #07b458 !important;
        font-size: 24px;
    }}

    /* Cor da pergunta na Sidebar (Azul Escuro) */
    .stSelectbox label p {{
        color: #1A237E !important; 
        font-weight: bold;
        font-size: 16px;
    }}

    /* Estilo das mensagens */
    [data-testid="stChatMessageAssistant"] {{
        border: 1px solid #07b458;
        background-color: #f9fffb;
        border-radius: 15px;
    }}
    
    [data-testid="stChatMessageUser"] {{
        border-radius: 15px;
    }}

    /* Botão customizado */
    .stButton>button {{
        border-radius: 20px;
        border: 1px solid #07b458;
        color: #07b458;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Configuração Necessária: Adicione a 'GROQ_API_KEY' nos Secrets do Streamlit.")
    st.stop()

# --- INICIALIZAÇÃO DE ESTADOS ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.title("Área do Aluno") # Este título agora é Verde OPEE
    
    # Seletor de Matéria
    materia = st.selectbox(
        "Sobre o que vamos estudar hoje?",
        ("Geral", "Matemática", "Português", "História e Geografia", "Ciências e Biologia")
    )
    
    st.divider()
    
    if st.button("🗑️ Reiniciar Conversa"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Desenvolvido por: Jcb | Opee Educação")

# --- INTERFACE PRINCIPAL ---

# Título Principal com Tooltip
st.markdown("""
    <div class="tooltip">Opeera (Gestor Educacional)
        <span class="tooltiptext">
            União do nome OPEE com "Era" (uma nova era de aprendizado) ou uma "ópera" de conhecimentos.
        </span>
    </div>
    """, unsafe_allow_html=True)

# Subtítulo Assistente em Verde OPEE
st.markdown(f"<h3 style='color: #07b458; margin-top: -15px;'>Assistente de {materia}</h3>", unsafe_allow_html=True)

# --- LÓGICA DO CHAT ---
prompts_especificos = {
    "Geral": "Você é um tutor da Opee Educação. Explique de forma didática.",
    "Matemática": "Você é um professor de matemática. Use LaTeX para fórmulas.",
    "Português": "Você é um professor de gramática. Foque na clareza e norma culta.",
    "História e Geografia": "Você é um historiador/geógrafo. Foque em contextos e causas.",
    "Ciências e Biologia": "Você é um cientista. Use analogias do cotidiano."
}

system_prompt = {"role": "system", "content": f"{prompts_especificos[materia]} Responda em português e seja motivador."}

# Exibir histórico
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Entrada do Aluno
if prompt := st.chat_input("Como posso te ajudar agora?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("OPEERA está formulando sua explicação..."):
            try:
                mensagens_com_contexto = [system_prompt] + st.session_state.messages
                
                chat_completion = client.chat.completions.create(
                    messages=mensagens_com_contexto,
                    model="llama-3.1-8b-instant",
                    temperature=0.6,
                )
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
                
            except Exception as e:
                st.error(f"Erro de conexão: {e}")