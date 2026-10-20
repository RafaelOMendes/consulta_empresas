# 🏢 Consulta Empresas — Dashboard CNPJ

Dashboard web feito em [Streamlit](https://streamlit.io/) que gera um dossiê de uma empresa brasileira a partir do CNPJ, usando os dados públicos da Receita Federal disponibilizados pela [BrasilAPI](https://brasilapi.com.br/).

## Funcionalidades

- **Consulta por CNPJ**: aceita o número com ou sem pontuação (`00.000.000/0001-91` ou `00000000000191`).
- **Dashboard da empresa** com:
  - Razão social e nome fantasia
  - Situação cadastral, data de abertura, porte e capital social
  - Endereço completo e contato (telefone e e-mail)
  - Atividade econômica principal (CNAE) e atividades secundárias
  - Quadro de sócios (QSA)
- **Investigação de sócio**: ao clicar no nome de um sócio, abre uma tela com um atalho para pesquisar o nome dele na web.

> ⚠️ **Limitação:** APIs públicas gratuitas não oferecem busca reversa (encontrar empresas a partir do nome de uma pessoa). Por isso, a tela de sócio usa uma pesquisa no Google como alternativa provisória.

## Pré-requisitos

- [Python](https://www.python.org/downloads/) 3.9 ou superior
- Conexão com a internet (os dados são consultados na BrasilAPI em tempo real)

## Como rodar

### Jeito rápido (Windows)

Dê **duplo clique em `rodar.bat`**. Na primeira execução ele cria um ambiente virtual (`venv`) e instala as dependências; nas próximas, só inicia a aplicação. O navegador abre em <http://localhost:8501>.

### Manualmente

1. **Clone o repositório** e entre na pasta:

   ```bash
   git clone <url-do-repositorio>
   cd consulta_empresas
   ```

2. **(Opcional) Crie e ative um ambiente virtual:**

   ```bash
   python -m venv venv

   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   source venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie a aplicação:**

   ```bash
   python -m streamlit run app.py
   ```

5. O navegador abrirá automaticamente em <http://localhost:8501>. Se não abrir, acesse esse endereço manualmente.

## Como usar

1. Cole um CNPJ no campo de busca.
2. Clique em **Gerar Dashboard**.
3. No quadro de sócios, clique em um nome para abrir a tela de investigação.
4. Use **⬅️ Voltar para o Dashboard** para fazer uma nova consulta.

## Estrutura do projeto

```
consulta_empresas/
├── app.py            # Aplicação Streamlit (telas de consulta CNPJ e de sócio)
├── requirements.txt  # Dependências Python
├── rodar.bat         # Atalho para rodar no Windows com duplo clique
└── README.md
```

## Tecnologias

- [Streamlit](https://streamlit.io/) — interface web
- [Requests](https://requests.readthedocs.io/) — chamadas HTTP
- [BrasilAPI — CNPJ](https://brasilapi.com.br/docs#tag/CNPJ) — fonte dos dados
