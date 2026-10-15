import time
import streamlit as st

# Configuração da Página (Layout Largo)
st.set_page_config(
    page_title="Painel de Automação CRM com WhatsApp", page_icon="🤖", layout="wide"
)

st.title("🚀 Painel de Automação de CRM & Envio WhatsApp")
st.write(
    "Gerencie a extração de contatos, acompanhe o progresso, visualize os logs"
    " em tempo real e envie os dados."
)

# Inicializando o estado da sessão
if "automacao_concluida" not in st.session_state:
  st.session_state.automacao_concluida = False
if "dados_extraidos" not in st.session_state:
  st.session_state.dados_extraidos = []

# Dividindo a tela principal nas 3 partes solicitadas
col_login, col_browser, col_terminal = st.columns([1.2, 1.5, 1.3])

# ==========================================
# PARTE 1: DADOS DE LOGIN E CONFIGURAÇÃO
# ==========================================
with col_login:
  st.subheader("1️⃣ Dados de Login")

  with st.form("form_automacao"):
    usuario = st.text_input("Usuário do CRM", placeholder="seu.email@empresa.com")
    senha = st.text_input(
        "Senha do CRM", type="password", placeholder="Sua senha"
    )

    qtd_contatos = st.slider(
        "Quantidade de Contatos",
        min_value=1,
        max_value=50,
        value=10,
        help="Limite máximo de 50 contatos por execução.",
    )

    btn_executar = st.form_submit_button("🚀 Executar Automação")

  st.markdown("---")
  st.subheader("📱 Pós-Processamento")

  telefone_destino = st.text_input(
      "Número do WhatsApp (com DDD)", placeholder="5511999999999"
  )
  btn_whatsapp = st.button(
      "📤 Enviar Dados via WhatsApp",
      disabled=not st.session_state.automacao_concluida,
  )

  if btn_whatsapp:
    if not telefone_destino:
      st.error("Informe o número de telefone do WhatsApp.")
    else:
      st.success(
          f"✅ Dados enviados com sucesso para o WhatsApp {telefone_destino}!"
      )
      st.balloons()

# ==========================================
# PARTE 2: TELA DO NAVEGADOR (VISUALIZADOR)
# ==========================================
with col_browser:
  st.subheader("2️⃣ Tela do Navegador")
  browser_placeholder = st.empty()

  if not st.session_state.automacao_concluida:
    browser_placeholder.info(
        "Aguardando início... O navegador será simulado ao clicar em Executar."
    )

# ==========================================
# PARTE 3: TERMINAL COM LOG DE DADOS
# ==========================================
with col_terminal:
  st.subheader("3️⃣ Terminal de Logs")
  terminal_placeholder = st.empty()

  if not st.session_state.automacao_concluida:
    terminal_placeholder.text(
        "[SYS] Sistema pronto para iniciar...\n[SYS] Aguardando comando do"
        " usuário."
    )

# ==========================================
# LÓGICA DE EXECUÇÃO DA AUTOMAÇÃO
# ==========================================
if btn_executar:
  if not usuario or not senha:
    st.error("Por favor, preencha o usuário e a senha!")
  else:
    st.session_state.automacao_concluida = False
    st.session_state.dados_extraidos = []

    logs_acumulados = "[SYS] Automação iniciada com sucesso!\n"
    terminal_placeholder.text(logs_acumulados)

    lista_temporaria = []

    for i in range(1, qtd_contatos + 1):
      browser_placeholder.success(
          f"🌐 Navegador em Execução\n\nStatus: Processando contato {i} de"
          f" {qtd_contatos}\nAção: Extraindo dados do CRM..."
      )

      dado = f"Contato {i}: Cliente_{i} | Tel: (11) 98888-{i:04d}"
      lista_temporaria.append(dado)

      logs_acumulados += f"[DADO EXTRAÍDO] {dado}\n"
      terminal_placeholder.text(logs_acumulados)

      time.sleep(0.5)

    st.session_state.dados_extraidos = lista_temporaria
    st.session_state.automacao_concluida = True

    browser_placeholder.success(
        "✅ Automação Concluída!\n\nDados extraídos com sucesso. Botão de"
        " WhatsApp liberado."
    )
    logs_acumulados += (
        "[SYS] Processo finalizado com 100% de sucesso. Aguardando envio via"
        " WhatsApp."
    )
    terminal_placeholder.text(logs_acumulados)
    st.toast("Automação finalizada! WhatsApp liberado.", icon="🎉")
    st.rerun()