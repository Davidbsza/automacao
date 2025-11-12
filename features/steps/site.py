from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from behave import given, when, then
from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time


@given("que o navegador Microsoft Edge está aberto")
def step_open_browser(context):
    
    print("Iniciando o Microsoft Edge")
    options = Options()
    options.add_argument("--start-maximized")
    
    context.driver = Edge(options=options)
    context.driver.get("https://formulario-contato-m8p8.onrender.com")
    


@when("o usuário preenche o formulário com os dados")
def step_fill_form(context):
    driver = context.driver
    
    # Exemplo de dados da pessoa
    pessoa = {
        "nome": "David bs",
        "email": "davidbbsouza@gmail.com",
        "telefone": "12992267683",
        "cidade": "ilhabela",
        "bairro": "barra velha",
        "escolaridade": "Superior",
        "mensagem": "Olá! Esta é uma mensagem automatizada e esse é meu primeiro dia fazendo QA."
    }

    # Preenche os campos — verifique o nome/id dos inputs no HTML
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
        print(" Formulário enviado.")
    except Exception as e:
        print("Erro ao clicar no botão:", e)

    time.sleep(3)


@then("formulário deve ser enviado com sucesso")
def step_verify_submission(context):
    driver = context.driver

    # Exemplo de verificação de mensagem de sucesso (ajuste conforme o site)
    mensagem = driver.find_element(By.ID, "mensagem-sucesso").text
    assert "enviado com sucesso" in mensagem.lower()
    
    context.driver.save_screenshot("Trabalho.png")
    time.sleep(5)
    
    driver.quit()

