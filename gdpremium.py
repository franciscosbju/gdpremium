import streamlit as st
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import os
import requests
from PIL import Image
from dotenv import load_dotenv  # Importa dotenv

# 🔒 Carregar variáveis do .env
load_dotenv()
USUARIO_CORRETO = "gdpremium"
SENHA_CORRETA = "premium"

# Inicializar sessão de autenticação
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if "usuario_digitado" not in st.session_state:
    st.session_state.usuario_digitado = False

# Criar tela de login antes de carregar qualquer outra coisa
if not st.session_state.autenticado:
    st.title("🔒 Login")

    # Campo de usuário com atualização dinâmica do estado
    usuario = st.text_input("Usuário")
    
    # Atualiza o estado para bloquear/desbloquear a senha em tempo real
    st.session_state.usuario_digitado = bool(usuario.strip())

    # Campo de senha (desativado se usuário estiver vazio)
    senha = st.text_input("Senha", type="password", disabled=not st.session_state.usuario_digitado)

    # Lógica para pressionar ENTER no campo de senha e logar automaticamente
    if senha and usuario:
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("✅ Login bem-sucedido!")
            st.rerun()  # 🔄 Atualiza a página corretamente
        else:
            st.error("❌ Usuário ou senha incorretos!")

    # Botão de login (caso o usuário prefira clicar ao invés de pressionar ENTER)
    if st.button("Entrar"):
        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            st.session_state.autenticado = True
            st.success("✅ Login bem-sucedido!")
            st.rerun()
        else:
            st.error("❌ Usuário ou senha incorretos!")

    st.stop()  # Impede que o resto da página seja carregado até login válido

import random

# 📌 Gerar número de pedido aleatório de 4 dígitos, se ainda não existir na sessão
if "numero_pedido" not in st.session_state:
    st.session_state.numero_pedido = random.randint(1000, 9999)

# 📌 URL da logo
img_url = "https://i.imgur.com/WT5aFHG.png"
img_path = "logo.png"

# 📌 Função para formatar telefone automaticamente
def formatar_telefone(numero):
    numero = ''.join(filter(str.isdigit, numero))  # Remove caracteres não numéricos
    if len(numero) == 11:  # Formato correto (11 dígitos)
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    return numero  # Retorna o que foi digitado se não for 11 dígitos

from fpdf import FPDF

def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 8, "GD PREMIUM JÓIAS 18k-750", ln=True, align='C')
    
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 4, "Endereço: Rua Radialista Edesio de Oliveira, nº 80,", ln=True, align='C')
    pdf.cell(200, 4, "Bairro Centro, Juazeiro do Norte - CE", ln=True, align='C')
    pdf.cell(200, 4, "Telefone P/ Contato: (88) 98805-4374", ln=True, align='C')
    pdf.cell(200, 4, "E-mail: gdgdpremium10@gmail.com", ln=True, align='C')
    pdf.cell(200, 4, "Instagram: @gd.premium", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Recibo - Tipo: {dados['tipo']}", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    titulo_numero = "Número do Pedido" if dados['tipo'] == "Pedido" else "Número do Orçamento"
    pdf.cell(200, 8, f"{titulo_numero}: {dados['numero_pedido']}", ln=True, align='L')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 8, f"Data: {dados['data']}", ln=True, align='L')
    pdf.cell(200, 8, f"Cliente: {dados['cliente']}", ln=True, align='L')
    pdf.cell(200, 8, f"Telefone: {dados['telefone']}", ln=True, align='L')
    pdf.cell(200, 8, f"Estado: {dados['estado']}", ln=True, align='L')
    pdf.cell(200, 8, f"Cidade: {dados['cidade']}", ln=True, align='L')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(20, 8, "Qtd", 1, align='C')
    pdf.cell(110, 8, "Descrição", 1, align='C')
    pdf.cell(30, 8, "V. Unit", 1, align='C')
    pdf.cell(30, 8, "Valor Total", 1, align='C')
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    
    for item in dados['itens']:
        y_start = pdf.get_y()
        
        descricao_linhas = pdf.multi_cell(110, 6, item['Descrição'], border=0, align='L', split_only=True)
        altura_linha = len(descricao_linhas) * 6
        
        pdf.cell(20, altura_linha, str(item['Qtd']), 1, align='C')
        x_descricao = pdf.get_x()
        pdf.multi_cell(110, 6, item['Descrição'], border=1, align='L')
        
        y_end = pdf.get_y()
        
        pdf.set_xy(x_descricao + 110, y_start)
        pdf.cell(30, altura_linha, formatar_valor(item['V. Unit']), 1, align='C')
        pdf.cell(30, altura_linha, formatar_valor(item['Valor']), 1, align='C')
        pdf.ln()
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Total R$: {formatar_valor(dados['total'])}", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 8, f"Entrada R$: {formatar_valor(float(dados.get('entrada', 0)))}", ln=True, align='L')

    # 📌 Captura valores corretamente e garante que sejam float
    desconto = float(dados.get('desconto', 0))  # Garante que sempre seja um número
    tipo_desconto = dados.get('tipo_desconto', '').strip()  # Remove espaços extras
    percentual = float(dados.get('percentual', 0))  # Garante que seja um número

    # 📌 Inicializa desconto_texto e verifica se há desconto aplicado
    desconto_texto = ""

    if desconto > 0 and tipo_desconto == "Valor R$":
        desconto_texto = f"Desconto: {formatar_valor(desconto)}"
    elif percentual > 0 and tipo_desconto == "Percentual (%)":
        desconto_texto = f"Desconto: {percentual:.2f}%"

    # 📌 Agora o desconto será sempre impresso corretamente caso seja maior que 0
    if desconto_texto.strip():  # Garante que não seja uma string vazia
        pdf.cell(200, 8, desconto_texto, ln=True, align='L')

    pdf.cell(200, 8, f"Resta R$: {formatar_valor(float(dados.get('resta', 0)))}", ln=True, align='L')
    
    # 📌 Data de Entrega ou Data de Validade (Dependendo do Tipo)
    if dados["tipo"] == "Orçamento":
        pdf.cell(200, 8, f"Data de Validade: {dados['data_entrega']}", ln=True, align='L')

        # 📌 Mensagem de Alerta para Orçamentos
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(255, 0, 0)  # Vermelho para destaque
        pdf.cell(200, 8, "Atenção: O valor do orçamento está sujeito a alterações a qualquer momento.", ln=True, align='L')
        pdf.set_text_color(0, 0, 0)  # Resetando a cor para preto

    else:
        pdf.cell(200, 8, f"Data de Entrega: {dados['data_entrega']}", ln=True, align='L')

    pdf.ln(20)

    # 📌 Assinatura apenas se for Pedido
    if dados["tipo"] == "Pedido":
        pdf.cell(200, 10, "_________________________________________", ln=True, align='C')
        pdf.cell(200, 10, "Gabriel Paulino Gonçalves", ln=True, align='C')

    # Posiciona as notas no rodapé ajustando dinamicamente
    pdf.ln(10)

    # 📌 Notas no rodapé (sempre presentes)
    pdf.set_font("Arial", 'BI', 7)  # Negrito e Itálico
    pdf.set_text_color(255, 0, 0)  # Cor vermelha

    pdf.cell(200, 2, "Nota 01: Prazo de entrega sujeito a alteração, a depender da demanda.", ln=True, align='L')
    pdf.ln(4)
    pdf.cell(200, 2, "Nota 02: Em casos de cancelamento, será ressarcido apenas 70% do valor pago.", ln=True, align='L')

    pdf.set_text_color(0, 0, 0)  # Resetando a cor para preto

    pdf_file = "recibo.pdf"
    pdf.output(pdf_file)
    return pdf_file

# Exibir título com a logo ao lado direito
st.markdown(
    """
    <div style="display: flex; align-items: center;">
        <h1 style="margin-right: 10px;">Gerador de Recibos</h1>
        <img src="https://i.imgur.com/WT5aFHG.png" width="80">
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("*Developed by Francisco Carneiro - (88) 99976-2740*", unsafe_allow_html=True)

# 📌 Escolher o tipo (Pedido ou Orçamento)
tipo = st.radio("Tipo:", ["Pedido", "Orçamento"])

# 📌 Definir o nome do campo dinamicamente
titulo_pedido = "Número do Pedido" if tipo == "Pedido" else "Número do Orçamento"

# 📌 Número do Pedido/Orçamento (Não editável)
st.markdown(
    f"""
    <h3 style="display: inline;">📌 <b>{titulo_pedido}:</b> 
    <span style="font-size: 24px; font-weight: bold; color: black;">{st.session_state.numero_pedido}</span>
    </h3>
    """,
    unsafe_allow_html=True
)

# 📌 Data formatada corretamente
data = st.date_input("📅 Data do Pedido/Orçamento", datetime.today(), key="data_pedido").strftime('%d/%m/%Y')
st.write(f"📌 Data Formatada: **{data}**")

# 📌 Nome do cliente
cliente = st.text_input("Nome do Cliente")

# 📌 Telefone
telefone = st.text_input("Telefone", max_chars=11)

# Validar telefone: deve conter apenas números e ter 10 ou 11 dígitos
if telefone and not telefone.isdigit():
    st.error("⚠️ O telefone deve conter apenas números!")

elif telefone and len(telefone) not in [10, 11]:
    st.error("⚠️ O telefone deve ter 10 ou 11 dígitos!")

else:
    telefone_formatado = formatar_telefone(telefone)
    st.write(f"📌 Telefone formatado: **{telefone_formatado}**")

# 📌 Estado e Cidade
estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
           "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
estado = st.selectbox("📍 Estado", estados)
cidade = st.text_input("🏙️ Cidade")

# 📌 Seção de Itens
st.subheader("📦 Itens do Recibo")
num_itens = st.number_input("Número de itens", min_value=1, step=1)

tabela = []
total = 0.00

for i in range(int(num_itens)):
    qtd = st.number_input(f"🔢 Qtd item {i+1}", min_value=1, step=1)
    
    # Campo de descrição com contador
    descricao = st.text_input(f"📝 Descrição item {i+1} (Máx: 500 caracteres)", max_chars=500)
    
    if len(descricao) > 500:
        st.warning(f"⚠️ Você digitou {len(descricao)} caracteres. Máximo permitido: 500.")
        descricao = descricao[:500]  # Garante que o backend receba apenas 500 caracteres válidos

    v_unit = st.number_input(f"💲 V. Unit item {i+1}", min_value=0.00, format="%.2f", value=0.00)
    valor = qtd * v_unit
    total += valor
    tabela.append({"Qtd": qtd, "Descrição": descricao, "V. Unit": v_unit, "Valor": valor})

    st.write(f"💰 Valor item {i+1}: R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Mensagem de aviso se alguma descrição ultrapassar o limite
if any(len(item["Descrição"]) > 500 for item in tabela):
    st.warning("⚠️ A descrição dos itens não pode ultrapassar 500 caracteres.")

# 📌 Exibir total formatado corretamente
st.write(f"### 🏷️ Total R$: {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# 📌 Entrada
entrada = st.number_input("💳 Entrada R$", min_value=0.00, max_value=total, format="%.2f")

# 📌 Escolher tipo de desconto
tipo_desconto = st.radio("🛒 Tipo de Desconto", ("Valor R$", "Percentual (%)"))

desconto = 0.00
percentual = 0.00

if tipo_desconto == "Valor R$":
    desconto = st.number_input("💰 Desconto R$", min_value=0.00, max_value=total, format="%.2f")
elif tipo_desconto == "Percentual (%)":
    percentual = st.number_input("📊 Desconto %", min_value=0.00, max_value=100.00, format="%.2f")

# 📌 Calcular o valor restante corretamente após a entrada e o desconto
valor_pos_entrada = total - entrada  # Primeiro subtrai a entrada
desconto_aplicado = (percentual / 100) * valor_pos_entrada if tipo_desconto == "Percentual (%)" else desconto
resta = valor_pos_entrada - desconto_aplicado  # Agora aplica o desconto no valor restante

# 📌 Exibir o valor restante formatado
st.write(f"### 🏷️ Resta R$: {resta:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# 📌 Alterar Data e Mostrar Alerta ao selecionar "Orçamento"
if tipo == "Orçamento":
    st.markdown("**⚠️ Atenção: O valor do orçamento está sujeito a alterações a qualquer momento.**", unsafe_allow_html=True)
    data_label = "📅 Data de Validade (Orçamento)"
    data_key = "data_validade"  # 🔑 Chave única para Data de Validade
else:
    data_label = "📅 Data de Entrega"
    data_key = "data_entrega"  # 🔑 Chave única para Data de Entrega

# 📌 Criar campo de data com chave única para evitar erro de elementos duplicados
data_entrega = st.date_input(data_label, key=data_key).strftime('%d/%m/%Y')

# 📌 Exibir a data formatada corretamente
st.write(f"📌 Data Formatada: **{data_entrega}**")

# 📌 Verificar se todas as descrições estão preenchidas corretamente
descricao_vazia = any(item["Descrição"].strip() == "" for item in tabela)
descricao_longas = any(len(item["Descrição"]) > 500 for item in tabela)

# 📌 Verificar se os campos obrigatórios estão preenchidos corretamente
if not cliente or not telefone or not estado or not cidade or total <= 0 or not data_entrega or descricao_vazia or not telefone.isdigit() or len(telefone) not in [10, 11]:
    st.error("⚠️ Todos os campos são obrigatórios, incluindo a descrição de todos os itens! O telefone deve conter apenas números e ter 10 ou 11 dígitos.")
elif descricao_longas:
    st.error("⚠️ Cada descrição de item deve ter no máximo 500 caracteres. Ajuste e tente novamente.")
else:
    if st.button("📄 Gerar PDF"):
        dados = {
        "numero_pedido": st.session_state.numero_pedido,
        "tipo": tipo,
        "data": data,
        "cliente": cliente,
        "telefone": telefone_formatado,
        "estado": estado,
        "cidade": cidade,
        "itens": tabela,
        "total": total,
        "entrada": entrada,
        "resta": resta,
        "data_entrega": data_entrega,
        "desconto": desconto,  # 🔥 Agora o desconto será passado para o PDF!
        "tipo_desconto": tipo_desconto,  # 🔥 Agora o tipo do desconto será passado!
        "percentual": percentual if tipo_desconto == "Percentual (%)" else 0  # 🔥 Se for percentual, envia o valor, senão, mantém 0
    }

        pdf_file = gerar_pdf(dados)  # Gera o PDF normalmente

        # Gerar um novo número do pedido
        novo_numero = random.randint(1000, 9999)
        st.session_state.numero_pedido = novo_numero

        # Criar o nome do arquivo PDF
        primeiro_nome = cliente.split()[0] if cliente else "Recibo"
        data_formatada = data.replace("/", "_")
        pdf_file_name = f"{primeiro_nome}_{data_formatada}.pdf"
        
        # Pegando o primeiro nome do cliente
        primeiro_nome = cliente.split()[0] if cliente else "Recibo"

        # Formatando a data para o nome do arquivo (02/02/2025 → 02_02_2025)
        data_formatada = data.replace("/", "_")

        # Criando o nome do arquivo com o nome do cliente + data
        pdf_file_name = f"{primeiro_nome}_{data_formatada}.pdf"

        st.success(f"✅ PDF Gerado com Sucesso! Nome do arquivo: {pdf_file_name}")
        
        # Botão de download com o nome correto
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Baixar PDF", f, file_name=pdf_file_name, mime="application/pdf")

