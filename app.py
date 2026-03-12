import streamlit as st
from groq import Groq
import os

# Configuração inicial da página
st.set_page_config(page_title="OPEERA - Tutor Inteligente", page_icon="🎓", layout="centered")

# --- ESTILIZAÇÃO PERSONALIZADA (CSS) ---
st.markdown(f"""
    <style>
    /* Estilo para o Título OPEERA com Tooltip Centralizado */
    .tooltip-container {{
        text-align: center; /* Centraliza o container do título */
        margin-top: 20px;
        margin-bottom: 10px;
    }}

    .tooltip {{
        position: relative;
        display: inline-block;
        font-size: 42px;
        font-weight: 800;
        color: #07b458; 
        cursor: help;
    }}

    .tooltip .tooltiptext {{
        visibility: hidden;
        width: 320px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 8px;
        padding: 12px;
        position: absolute;
        z-index: 10;
        bottom: 125%; /* Espaço superior maior */
        left: 50%;
        transform: translateX(-50%); /* Centraliza exatamente no meio do título */
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
        font-weight: normal;
        line-height: 1.5;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }}

    /* Triângulo indicador do tooltip */
    .tooltip .tooltiptext::after {{
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #333 transparent transparent transparent;
    }}

    .tooltip:hover .tooltiptext {{
        visibility: visible;
        opacity: 1;
    }}

    /* Título Área do Aluno na Sidebar */
    [data-testid="stSidebar"] h1 {{
        color: #07b458 !important;
        font-size: 24px;
    }}

    /* Cor da pergunta na Sidebar (Azul Escuro) */
    .stSelectbox label p {{
        color: #1A237E !important; 
        font-weight: bold;
    }}

    /* Estilo das mensagens */
    [data-testid="stChatMessageAssistant"] {{
        border: 1px solid #07b458;
        background-color: #f9fffb;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DA API GROQ ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("⚠️ Erro: Chave 'GROQ_API_KEY' não configurada.")
    st.stop()

# --- INICIALIZAÇÃO DE ESTADOS ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("logo.png", use_column_width=True)
    st.title("Área do Aluno")
    
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

# Título Principal Centralizado com Tooltip Melhorado
st.markdown("""
    <div class="tooltip-container">
        <div class="tooltip">Opeera (Gestor Educacional)
            <span class="tooltiptext">
                União do nome OPEE com "Era" (uma nova era de aprendizado) ou uma "ópera" de conhecimentos.
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"<h4 style='color: #07b458; text-align: center; margin-top: -10px;'>Assistente de {materia}</h4>", unsafe_allow_html=True)
st.divider()

# --- LÓGICA DO CHAT ---
prompts_especificos = {
    "Geral": "Você é um tutor da Opee Educação. Explique de forma didática.",
    "Matemática": "Você é um professor de matemática. Use LaTeX.",
    "Português": "Você é um professor de gramática.",
    "História e Geografia": "Você é um historiador/geógrafo.",
    "Ciências e Biologia": "Você é um cientista."
}

# Container para as mensagens (isso ajuda na organização visual)
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# Entrada do Aluno
if prompt := st.chat_input("Escreva sua dúvida aqui..."):
    # Adiciona e exibe imediatamente a dúvida do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_container:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

    # Resposta da IA
    with chat_container:
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("OPEERA está formulando sua explicação..."):
                try:
                    system_prompt = {"role": "system", "content": f"{prompts_especificos[materia]} Responda em português."}
                    mensagens_com_contexto = [system_prompt] + st.session_state.messages
                    
                    
                    chat_completion = client.chat.completions.create(
                        messages=mensagens_com_contexto,
                        model="llama-3.3-70b-versatile", # <--- Nova IA mais potente
                        temperature=0.6,
                    )
                    response = chat_completion.choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # O Streamlit já rola para o final automaticamente em novos inputs
                    # O rerun garante que o histórico e os estados laterais estejam sincronizados
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Erro de conexão: {e}")