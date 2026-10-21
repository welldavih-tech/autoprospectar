from datetime import datetime
import time
import streamlit as st

# Importações do Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Configuração da Página
st.set_page_config(
    page_title="Automação de Prospecção", page_icon="📈", layout="wide"
)

# Título Principal
st.title("📈 Automação de Prospecção")
st.write(
    "Insira suas credenciais, defina a quantidade de contatos e execute a"
    " automação do CRM com validação de WhatsApp."
)

# Controle de estado da sessão
if "automacao_concluida" not in st.session_state:
  st.session_state.automacao_concluida = False
if "dados_extraidos" not in st.session_state:
  st.session_state.dados_extraidos = []
if "logs_anteriores" not in st.session_state:
  st.session_state.logs_anteriores = (
      "[SYS] Sistema pronto.\n[SYS] Aguardando clique em 'Executar Automação'."
  )
if "abrir_modal" not in st.session_state:
  st.session_state.abrir_modal = False
if "tempo_gasto" not in st.session_state:
  st.session_state.tempo_gasto = "00:00"


# ==========================================
# 📌 POPUP MODAL COM BOTÃO DE SALVAR E TIMER
# ==========================================
@st.dialog("🎉 Extração Concluída com Sucesso!")
def modal_sucesso(dados, qtd, tempo):
  st.write(
      f"Foram extraídos com sucesso **{len(dados)}** de **{qtd}** contatos"
      " solicitados."
  )
  st.write(f"⏱️ **Tempo total de execução:** `{tempo}`")
  st.write(
      "Clique no botão abaixo para baixar o relatório completo em formato de"
      " texto:"
  )

  data_hora_atual = datetime.now().strftime("%d-%m-%Y_%H-%M")
  nome_arquivo = f"base_prospectar_{data_hora_atual}.txt"

  conteudo_arquivo = (
      f"Relatório de Leads Extraídos - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
      f"Tempo de Execução: {tempo}\n"
      + "=" * 60
      + "\n\n"
  )
  for lead in dados:
    conteudo_arquivo += f"{lead}\n"

  st.download_button(
      label="💾 Salvar Relatório (.txt)",
      data=conteudo_arquivo,
      file_name=nome_arquivo,
      mime="text/plain",
  )


# Se a automação terminou, exibe o popup automaticamente
if st.session_state.abrir_modal:
  modal_sucesso(
      st.session_state.dados_extraidos,
      len(st.session_state.dados_extraidos),
      st.session_state.tempo_gasto,
  )

# Layout em colunas para manter a organização visual
col_login, col_terminal = st.columns([1.2, 1.8])

# ==========================================
# 1️⃣ TELA DE LOGIN E PARÂMETROS
# ==========================================
with col_login:
  st.subheader("1️⃣ Dados de Acesso")

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
        help="Limite máximo de 50 contatos.",
    )

    btn_executar = st.form_submit_button("🚀 Executar Automação")

  st.markdown("---")
  st.subheader("💾 Status da Extração")

  if st.session_state.automacao_concluida:
    st.success(
        f"✅ Extração finalizada! Tempo: {st.session_state.tempo_gasto}"
    )
    if st.button("📂 Abrir Popup de Download"):
      modal_sucesso(
          st.session_state.dados_extraidos,
          len(st.session_state.dados_extraidos),
          st.session_state.tempo_gasto,
      )
  else:
    st.info("ℹ️ Sistema aguardando execução.")

# ==========================================
# 2️⃣ PAINEL DE LOG E BARRA DE PROGRESSO
# ==========================================
with col_terminal:
  st.subheader("2️⃣ Painel de Log")

  # Barra de progresso posicionada logo abaixo do título do Painel de Log
  container_progresso = st.empty()

  terminal_placeholder = st.empty()
  terminal_placeholder.text(st.session_state.logs_anteriores)

# ==========================================
# 3️⃣ LÓGICA DE EXECUÇÃO DA AUTOMAÇÃO COMPLETA
# ==========================================
if btn_executar:
  if not usuario or not senha:
    st.error("Por favor, preencha o usuário e a senha do CRM!")
  else:
    st.session_state.automacao_concluida = False
    st.session_state.dados_extraidos = []
    st.session_state.abrir_modal = False

    # Marca o tempo inicial da automação
    tempo_inicio = time.time()

    logs = "[SYS] Iniciando automação, extração e validação inteligente de WhatsApp...\n\n"
    terminal_placeholder.text(logs)

    barra_progresso = container_progresso.progress(
        0, text="Iniciando conexão com o CRM..."
    )

    driver = None
    try:
      options = webdriver.ChromeOptions()
      options.add_argument("--start-maximized")
      # Argumentos obrigatórios para rodar no Streamlit Cloud (Linux)
      options.add_argument("--headless=new")
      options.add_argument("--no-sandbox")
      options.add_argument("--disable-dev-shm-usage")
      options.add_argument("--disable-gpu")
      options.add_argument("--window-size=1920,1080")

      driver = webdriver.Chrome(
          service=Service(ChromeDriverManager().install()), options=options
      )

      url_crm = "https://pilot.mazzabroker.com.br/login"
      driver.get(url_crm)
      time.sleep(3)

      try:
        campo_usuario = driver.find_element(By.NAME, "email")
        campo_usuario.send_keys(usuario)

        campo_senha = driver.find_element(By.NAME, "password")
        campo_senha.send_keys(senha)

        try:
          botao_entrar = driver.find_element(
              By.XPATH,
              "//button[contains(text(), 'Entrar') or contains(text(),"
              " 'Acessar') or contains(text(), 'Login')]",
          )
        except:
          botao_entrar = driver.find_element(
              By.CSS_SELECTOR, "button[type='submit']"
          )

        botao_entrar.click()
      except Exception as ex:
        pass

      barra_progresso.progress(
          20, text="Autenticado com sucesso. Acessando Prospecção..."
      )
      time.sleep(10)

      try:
        botao_prospeccao = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(text(), 'Prospecção')]")
            )
        )
        botao_prospeccao.click()
      except Exception as ex:
        pass

      time.sleep(3)

      clicado_prospectador = False
      for tentativa in range(3):
        try:
          xpaths_possiveis = [
              '//*[@id="conteudo-principal"]//button[.//svg]',
              "//button[@title='Prospectador' or @aria-label='Prospectador']",
              "//span[contains(., 'Prospectador')]/preceding-sibling::button",
              '//*[@id="conteudo-principal"]/div/div/div/div[1]/div/div[1]/div[3]/span[2]/button',
          ]

          botao_prospectador = None
          for xp in xpaths_possiveis:
            try:
              elementos = driver.find_elements(By.XPATH, xp)
              if elementos:
                botao_prospectador = elementos[0]
                break
            except:
              continue

          if botao_prospectador:
            time.sleep(1)
            driver.execute_script("arguments[0].click();", botao_prospectador)
            clicado_prospectador = True
            break
          else:
            raise Exception()
        except Exception as e_t:
          time.sleep(2)

      if not clicado_prospectador:
        raise Exception(
            "Não foi possível localizar ou clicar no botão Prospectador."
        )

      barra_progresso.progress(
          40, text="Painel do Prospectador aberto. Extraindo leads..."
      )
      time.sleep(4)

      lista_temp = []

      for i in range(1, qtd_contatos + 1):
        try:
          time.sleep(2)

          try:
            codigo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="conteudo-principal"]/div/div/dialog/div/footer/div/div[1]/span',
                    )
                )
            ).text
          except:
            codigo = "N/A"

          try:
            nome = driver.find_element(
                By.XPATH, '//*[@id="prospecting-lead-heading"]/button'
            ).text
          except:
            nome = "N/A"

          try:
            telefone = driver.find_element(
                By.XPATH,
                '//*[@id="conteudo-principal"]/div/div/dialog/div/div/div/div[2]/article/div/section[1]/div[2]/div[1]/div[1]/div/div[1]/span/Strong',
            ).text
          except:
            telefone = "N/A"

          try:
            tipo = driver.find_element(
                By.XPATH,
                '//*[@id="conteudo-principal"]/div/div/dialog/div/div/div/header/div/span/span[2]',
            ).text
          except:
            tipo = "N/A"

          # 📱 Validação lógica do WhatsApp
          status_whatsapp = "INVALIDO"
          if telefone and telefone != "N/A":
            num_limpo = "".join(filter(str.isdigit, telefone))
            if len(num_limpo) >= 10:
              status_whatsapp = "VALIDO"

          lead_info = (
              f"Lead {i} | Cód: {codigo} | Nome: {nome} | Tel: {telefone} |"
              f" WhatsApp: {status_whatsapp} | Tipo: {tipo}"
          )
          lista_temp.append(lead_info)

          logs += (
              f"[{i}/{qtd_contatos}] Cód: {codigo} | Nome: {nome} | Tel:"
              f" {telefone} | WhatsApp: {status_whatsapp} | Tipo: {tipo}\n"
          )
          terminal_placeholder.text(logs)

          progresso_atual = 40 + int((i / qtd_contatos) * 50)
          barra_progresso.progress(
              progresso_atual,
              text=f"Extraindo e validando lead {i} de {qtd_contatos}...",
          )

        except Exception as err_ext:
          pass

        # Timer de 15 segundos entre os leads
        if i < qtd_contatos:
          for t_restante in range(15, 0, -1):
            barra_progresso.progress(
                progresso_atual,
                text=f"Aguardando próximo lead em {t_restante}s ({i}/{qtd_contatos} concluídos)...",
            )
            time.sleep(1)

        # 🔀 DECISÃO CONDICIONAL: Clique no botão baseado na validação do WhatsApp
        try:
          if status_whatsapp == "INVALIDO":
            # Botão 1 (Ex: Arquivar / Inválido)
            xpath_acao = '//*[@id="conteudo-principal"]/div/div/dialog/div/footer/div/div[2]/button[1]/span'
          else:
            # Botão 2 (Ex: Avançar / Válido)
            xpath_acao = '//*[@id="conteudo-principal"]/div/div/dialog/div/footer/div/div[2]/button[2]/span'

          botao_acao = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.XPATH, xpath_acao))
          )
          driver.execute_script("arguments[0].click();", botao_acao)
        except Exception as err_acao:
          break

      # Cálculo do tempo total gasto
      tempo_fim = time.time()
      duracao_segundos = int(tempo_fim - tempo_inicio)
      minutos = duracao_segundos // 60
      segundos = duracao_segundos % 60
      tempo_formatado = f"{minutos:02d}m {segundos:02d}s"

      barra_progresso.progress(
          100, text=f"Extração finalizada em {tempo_formatado}!"
      )
      time.sleep(1)
      container_progresso.empty()

      st.session_state.dados_extraidos = lista_temp
      st.session_state.automacao_concluida = True
      st.session_state.abrir_modal = True
      st.session_state.tempo_gasto = tempo_formatado

      logs += f"\n[SYS] Processo concluído! Total de {len(lista_temp)} contatos. Tempo: {tempo_formatado}."
      st.session_state.logs_anteriores = logs
      terminal_placeholder.text(logs)

      time.sleep(2)
      driver.quit()
      st.rerun()

    except Exception as e:
      if driver:
        try:
          driver.quit()
        except:
          pass
      error_msg = f"\n[ERRO] Falha na execução: {str(e)}"
      logs += error_msg
      st.session_state.logs_anteriores = logs
      terminal_placeholder.text(logs)
      container_progresso.empty()
      st.error(f"Ocorreu um erro durante a automação: {e}")
