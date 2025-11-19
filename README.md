O Arquivo .gitignore
Para que serve: Este arquivo diz ao Git o que NÃO deve ser enviado para a internet. Isso protege sua privacidade (currículo) e evita enviar lixo (pasta venv).

Crie um arquivo chamado .gitignore (com o ponto na frente mesmo) na raiz do projeto e cole isso:

Snippet de código

# Ignorar ambiente virtual (pesado e específico da sua máquina)
venv/
.env

# Ignorar arquivos compilados do Python
__pycache__/
*.pyc

# Ignorar arquivos de dados e logs gerados durante a execução
*.csv
*.log

# IMPORTANTE: Ignorar dados pessoais e currículos
*.pdf
*.docx

# Ignorar configurações de IDE (VS Code)
.vscode/
2. O Arquivo README.md
Para que serve: É a "capa" do seu projeto no GitHub. Explica o que o código faz, como instalar e como rodar.

Crie um arquivo chamado README.md e cole o conteúdo abaixo. Eu já formatei bonitinho com Markdown:

Markdown

# 🤖 Bot de Candidatura Automática - LinkedIn (Selenium)

Este projeto é um script de automação desenvolvido em **Python** utilizando **Selenium**. O objetivo é facilitar a busca por vagas de **Programador Python Júnior**, automatizando o processo de "Candidatura Simplificada" (Easy Apply) no LinkedIn.

> **Status:** ✅ Funcional (Testado no Linux Mint 22.1)

## 🚀 Funcionalidades

- **Filtros Inteligentes:** Acessa vagas já filtradas por URL (Remoto, Brasil, Easy Apply, Nível Júnior).
- **Candidatura Híbrida:** - Se o formulário for simples (apenas "Enviar"), o bot finaliza sozinho.
    - Se houver perguntas extras, o bot **pausa**, emite um alerta e aguarda o preenchimento manual antes de continuar para a próxima vaga.
- **Anti-Bloqueio:** Utiliza pausas estratégicas (`time.sleep`) e rolagens de página para simular comportamento humano.
- **Log de Execução:** Gera um arquivo `vagas_aplicadas.csv` com o histórico de todas as vagas tentadas e o status (Enviada, Manual, Erro).

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Selenium WebDriver
- Webdriver Manager (Gerenciamento automático do Driver do Chrome)
- CSV (Para relatórios)

## ⚙️ Pré-requisitos

Antes de começar, você precisa ter instalado:
- [Google Chrome](https://www.google.com/chrome/)
- [Python 3](https://www.python.org/)

## 📦 Como Instalar e Rodar

### 1. Clone o repositório
```bash
git clone [https://github.com/FlowDev1994/automacao-vagas-python.git](https://github.com/FlowDev1994/automacao-vagas-python.git)
cd automacao-vagas-python
2. Crie e ative o ambiente virtual
No Linux/Mac:

Bash

python3 -m venv venv
source venv/bin/activate
3. Instale as dependências
Bash

pip install selenium webdriver-manager
4. Configuração (Opcional)
Abra o arquivo vagas_v4_final.py e edite as variáveis no topo se quiser mudar a busca:

Python

KEYWORDS = "programador python"
MAX_VAGAS_POR_EXECUCAO = 15
5. Execute o Bot
Bash

python3 vagas_v4_final.py
📝 Como Usar
Ao rodar o script, uma janela do Chrome será aberta na página de login do LinkedIn.

Faça o login manualmente.

Volte ao terminal e pressione ENTER.

O bot começará a entrar nas vagas.

Se o terminal mostrar 🛑 [INTERVENÇÃO NECESSÁRIA], vá ao navegador, responda as perguntas da vaga, envie e depois pressione ENTER no terminal para continuar.

⚠️ Aviso Legal
Este script foi criado para fins de aprendizado e uso pessoal. O uso excessivo de automação pode infringir os Termos de Serviço do LinkedIn. Recomenda-se usar com moderação (ex: limites baixos de vagas por dia).

Desenvolvido por Tayara Romero 💜


---

### Como criar esses arquivos pelo Terminal (Linux Mint)

Se quiser criar rapidinho sem abrir editor de texto, rode no seu terminal (dentro da pasta do projeto):

1.  **Criar o gitignore:**
    ```bash
    nano .gitignore
    ```
    *(Cole o conteúdo do gitignore acima, aperte `Ctrl+O` depois `Enter` para salvar, e `Ctrl+X` para sair).*

2.  **Criar o README:**
    ```bash
    nano README.md
    ```
    *(Cole o conteúdo do README acima, aperte `Ctrl+O` depois `Enter` para salvar, e `Ctrl+X` para sair).*

Depois disso, é só fazer o combo final para subir tudo:

```bash
git add .
git commit -m "Adicionando documentação README e gitignore"
git push
