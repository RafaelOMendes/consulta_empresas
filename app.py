import streamlit as st
import requests

# 1. Configuração inicial da página (deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Dashboard Empresa", page_icon="🏢", layout="wide")

# 2. Título principal
st.title("📊 Inteligência Corporativa - Consulta CNPJ")
st.markdown("Insira um CNPJ abaixo para gerar o dossiê completo da empresa.")

# 3. Campo de busca
cnpj_input = st.text_input("Digite o CNPJ (apenas números):", max_chars=14)

# 4. Ação ao clicar no botão
if st.button("Gerar Dashboard", type="primary"):
    if len(cnpj_input) == 14 and cnpj_input.isdigit():
        with st.spinner("Consultando a base de dados da Receita Federal..."):
            
            # Consumindo a Brasil API
            url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_input}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                # --- CONSTRUÇÃO DO DASHBOARD ---
                
                # Cabeçalho da Empresa
                nome_fantasia = data.get('nome_fantasia') or "Sem Nome Fantasia cadastrado"
                st.header(f"{data.get('razao_social')}")
                st.subheader(f"🏷️ {nome_fantasia}")
                st.divider()

                # Linha 1: Métricas Principais
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Situação Cadastral", data.get("descricao_situacao_cadastral"))
                col2.metric("Data de Abertura", data.get("data_inicio_atividade"))
                col3.metric("Porte da Empresa", data.get("porte"))
                
                # Formatando o capital social para Reais (R$)
                capital = data.get('capital_social', 0)
                col4.metric("Capital Social", f"R$ {capital:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

                st.divider()

                # Linha 2: Endereço e Contato
                col_end, col_cont = st.columns(2)
                
                with col_end:
                    st.markdown("### 📍 Localização")
                    st.write(f"**Logradouro:** {data.get('logradouro')}, {data.get('numero')} {data.get('complemento', '')}")
                    st.write(f"**Bairro:** {data.get('bairro')}")
                    st.write(f"**Cidade/UF:** {data.get('municipio')} - {data.get('uf')}")
                    st.write(f"**CEP:** {data.get('cep')}")

                with col_cont:
                    st.markdown("### 📞 Contato")
                    ddd_tel = data.get('ddd_telefone_1', 'Não informado')
                    email = data.get('email', 'Não informado')
                    st.write(f"**Telefone Principal:** {ddd_tel}")
                    st.write(f"**E-mail:** {email}")

                st.divider()

                # Linha 3: Atividades e Quadro Societário
                col_cnae, col_qsa = st.columns(2)

                with col_cnae:
                    st.markdown("### 💼 Atividades Econômicas (CNAE)")
                    st.success(f"**Principal:** {data.get('cnae_fiscal_descricao')} (Código: {data.get('cnae_fiscal')})")
                    
                    cnaes_sec = data.get("cnaes_secundarios", [])
                    if cnaes_sec:
                        with st.expander("Ver Atividades Secundárias"):
                            for cnae in cnaes_sec:
                                st.write(f"- {cnae.get('descricao')} ({cnae.get('codigo')})")

                with col_qsa:
                    st.markdown("### 👥 Quadro de Sócios (QSA)")
                    socios = data.get("qsa", [])
                    if socios:
                        for socio in socios:
                            st.info(f"**{socio.get('nome_socio')}** \n\nCargo: {socio.get('qualificacao_socio')}")
                    else:
                        st.write("Nenhum sócio listado ou empresa individual.")

            else:
                st.error("Erro ao buscar os dados. Verifique se o CNPJ está correto ou se a API está fora do ar.")
    else:
        st.warning("Por favor, insira um CNPJ válido contendo exatamente 14 números.")