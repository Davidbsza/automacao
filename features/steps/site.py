from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


@given("que o navegador Microsoft Edge está aberto")
def step_open_browser(context):
    print("Iniciando o Microsoft Edge")
    options = Options()
    options.add_argument("--start-maximized")
    # Desativa a detecção de automação
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Remove mensagens de log desnecessárias
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    context.driver = Edge(options=options)
    context.driver.get("https://formulario-contato-m8p8.onrender.com")


@when("o usuário preenche o formulário com os dados")
def step_fill_form(context):
    driver = context.driver

    pessoa = {
        "nome": "David bs",
        "email": "davidbbsouza@gmail.com",
        "telefone": "12992267683",
        "cidade": "ilhabela",
        "bairro": "barra velha",
        "escolaridade": "Superior",
        "mensagem": "Olá! Esta é uma mensagem automatizada e esse é meu primeiro dia fazendo QA."
    }

    # Preenche os campos
    driver.find_element(By.NAME, "nome").send_keys(pessoa["nome"])
    driver.find_element(By.NAME, "email").send_keys(pessoa["email"])
    driver.find_element(By.NAME, "telefone").send_keys(pessoa["telefone"])
    driver.find_element(By.NAME, "bairro").send_keys(pessoa["bairro"])
    driver.find_element(By.NAME, "cidade").send_keys(pessoa["cidade"])
    driver.find_element(By.XPATH, "/html/body/div/div/form/div[3]/label[3]").click()
    driver.find_element(By.NAME, "mensagem").send_keys(pessoa["mensagem"])

    time.sleep(5)
    print("Formulario preenchido corretamente!.")

    # Clicar no botão de envio
    try:
        botao = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enviar')]"))
        )
        botao.click()
        print("Formulário enviado.")
    except Exception as e:
        print("Erro ao clicar no botão:", e)

    time.sleep(3)


@then("formulário deve ser enviado com sucesso")
def step_verify_submission(context):
    driver = context.driver

    try:
        print("⏳ Aguardando mensagem de sucesso aparecer...")

        # 1️⃣ Tenta encontrar o elemento com ID 'mensagem-sucesso'
        try:
            mensagem_elemento = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "mensagem-sucesso"))
            )
            mensagem = mensagem_elemento.text
            print(f"📩 Mensagem (ID detectado): {mensagem}")

        # 2️⃣ Se não encontrar, tenta achar o texto 'sucesso' ou 'enviado' no corpo da página
        except:
            print("⚠️ Elemento com ID 'mensagem-sucesso' não encontrado. Verificando texto na página...")
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "sucesso")
            )
            mensagem = "Texto 'sucesso' detectado no corpo da página."

        # 3️⃣ Validação final
        assert "sucesso" in mensagem.lower() or "enviado" in mensagem.lower()
        print("✅ Formulário enviado com sucesso!")

    except Exception as e:
        print("❌ Erro ao verificar envio:", e)
        driver.save_screenshot("erro_envio.png")
        print("🖼️ Screenshot salva como 'erro_envio.png'")
        print("🔎 HTML atual da página (trecho):")
        print(driver.page_source[:1000])  # Mostra um pedaço do HTML atual
        raise

    context.driver.save_screenshot("Trabalho.png")
    time.sleep(5)
    driver.quit()

