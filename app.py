import streamlit as st
import requests
import re

st.set_page_config(page_title="Dashboard Empresa", page_icon="🏢", layout="wide")

# 1. GERENCIAMENTO DE ESTADO (Para navegar entre telas)
if "tela" not in st.session_state:
    st.session_state.tela = "busca_cnpj"
if "socio_alvo" not in st.session_state:
    st.session_state.socio_alvo = ""

def voltar_para_home():
    st.session_state.tela = "busca_cnpj"

# ==========================================
# TELA 2: INVESTIGAÇÃO DO SÓCIO
# ==========================================
if st.session_state.tela == "busca_socio":
    st.button("⬅️ Voltar para o Dashboard", on_click=voltar_para_home)
    
    socio = st.session_state.socio_alvo
    st.title("🔍 Investigação de Sócio")
    st.header(socio)
    
    st.warning("⚠️ Limitação Técnica de APIs Públicas")
    st.write(
        "Atualmente, APIs gratuitas não possuem rotas de busca reversa "
        "(encontrar empresas a partir do nome da pessoa física). "
        "Para implementar isso em um ambiente de produção real, seria necessário assinar uma API corporativa paga "
        "ou processar a base de dados bruta da Receita Federal em um servidor próprio."
    )
    
    # Workaround: Link direto para busca na web
    url_google = f"https://www.google.com/search?q=%22{socio.replace(' ', '+')}%22+CNPJ"
    st.markdown(f"**Como alternativa provisória, você pode buscar este nome diretamente na web:**")
    st.link_button(f"Pesquisar empresas de {socio} no Google 🔎", url_google)

# ==========================================
# TELA 1: DASHBOARD PRINCIPAL (COMPLETO)
# ==========================================
elif st.session_state.tela == "busca_cnpj":
    st.title("📊 Inteligência Corporativa - Consulta CNPJ")
    st.markdown("Cole um CNPJ abaixo para gerar o dossiê completo da empresa.")

    # Aceita colar com pontos e barras
    cnpj_input = st.text_input("CNPJ:", placeholder="Ex: 00.000.000/0001-91")
    
    # Limpa os caracteres especiais magicamente
    cnpj_limpo = re.sub(r'[^0-9]', '', cnpj_input)

    if st.button("Gerar Dashboard", type="primary"):
        if len(cnpj_limpo) == 14:
            with st.spinner("Consultando a base de dados da Receita Federal..."):
                url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
                response = requests.get(url)

                if response.status_code == 200:
                    data = response.json()
                    
                    # --- RESTAURANDO O DASHBOARD COMPLETO ---
                    nome_fantasia = data.get('nome_fantasia') or "Sem Nome Fantasia cadastrado"
                    st.header(f"{data.get('razao_social')}")
                    st.subheader(f"🏷️ {nome_fantasia}")
                    st.divider()

                    # Linha 1: Métricas Principais
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Situação Cadastral", data.get("descricao_situacao_cadastral"))
                    col2.metric("Data de Abertura", data.get("data_inicio_atividade"))
                    col3.metric("Porte da Empresa", data.get("porte"))
                    
                    capital = data.get('capital_social', 0)
                    col4.metric("Capital Social", f"R$ {capital:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

                    st.divider()

                    # Linha 2: Endereço e Contato
                    col_end, col_cont = st.columns(2)
                    
                    with col_end:
                        st.markdown("### 📍 Localização")
                        st.write(f"**Logradouro:** {data.get('logradouro')}, {data.get('numero')} {data.get('complemento', '')}")
                        st.write(f"**Bairro:** {data.get('bairro')} | **CEP:** {data.get('cep')}")
                        st.write(f"**Cidade/UF:** {data.get('municipio')} - {data.get('uf')}")

                    with col_cont:
                        st.markdown("### 📞 Contato")
                        st.write(f"**Telefone:** {data.get('ddd_telefone_1', 'Não informado')}")
                        st.write(f"**E-mail:** {data.get('email', 'Não informado')}")

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
                        st.markdown("### 👥 Quadro de Sócios")
                        st.caption("Clique no nome de um sócio para investigar.")
                        socios = data.get("qsa", [])
                        if socios:
                            for socio in socios:
                                nome_socio = socio.get('nome_socio')
                                cargo = socio.get('qualificacao_socio')
                                
                                # Botão que engatilha a página do sócio
                                if st.button(f"🔍 {nome_socio} \n\n({cargo})", key=nome_socio, use_container_width=True):
                                    st.session_state.socio_alvo = nome_socio
                                    st.session_state.tela = "busca_socio"
                                    st.rerun()
                        else:
                            st.write("Nenhum sócio listado na base.")

                else:
                    st.error("Erro ao buscar os dados. Verifique o CNPJ ou a estabilidade da API.")
        elif cnpj_input:
            st.warning("O CNPJ deve conter exatamente 14 números (pontos e barras são ignorados).")