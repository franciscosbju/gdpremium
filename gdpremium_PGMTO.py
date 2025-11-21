import streamlit as st
import streamlit.components.v1 as components

# ---------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------
st.set_page_config(
    page_title="GD PREMIUM - Acesso ao Sistema",
    page_icon="💎",
    layout="centered"
)

# ---------------------------------------------
# ESTILOS (CSS ELEGANTE)
# ---------------------------------------------
st.markdown("""
<style>
.card {
    background-color: #ffffff;
    padding: 25px 30px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    max-width: 750px;
    margin: 0 auto;
    font-family: "Segoe UI", sans-serif;
}

.titulo {
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 10px;
    color: #1a1a1a;
}

.subtitulo {
    font-size: 17px;
    text-align: center;
    color: #555555;
    margin-bottom: 20px;
}

.pix-box {
    background-color: #f5f7fb;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #e0e3f0;
    margin-top: 20px;
}

.pix-codigo {
    font-family: Consolas, monospace;
    background: #fff;
    padding: 12px;
    border-radius: 6px;
    border: 1px solid #ddd;
    word-break: break-all;
    font-size: 14px;
}

.valor-box {
    background: #fff7c2;
    border-left: 6px solid #c40000;
    padding: 14px 20px;
    border-radius: 8px;
    margin: 25px 0;
}

.valor-texto {
    font-size: 24px;
    font-weight: 800;
    color: #c40000;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# PIX COPIA E COLA
# ---------------------------------------------
PIX_CODE = (
    "00020126360014br.gov.bcb.pix0114+55889997627405204000053039865802BR5925Francisco Das Chagas Carn"
    "6009Sao Paulo62290525REC6920A338147CD6088403276304D93C"
)

# SCRIPT DO BOTÃO COPIAR
copy_button_html = f"""
<script>
function copyText() {{
  navigator.clipboard.writeText("{PIX_CODE}");
  alert("Código PIX copiado com sucesso!");
}}
</script>

<button onclick="copyText()" 
style="
background:#1c8c5f;
color:white;
padding:10px 22px;
border:none;
border-radius:6px;
cursor:pointer;
font-size:15px;
font-weight:700;">
📋 Copiar código PIX
</button>
"""

# ---------------------------------------------
# LAYOUT
# ---------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("""
<div class="titulo">💎 GD PREMIUM – Acesso ao Sistema</div>
<div class="subtitulo">Olá! Para acesso ao sistema, é necessário efetuar o pagamento da assinatura mensal.</div>
""", unsafe_allow_html=True)

# VALOR DESTACADO
st.markdown("""
<div class="valor-box">
    <div class="valor-texto">⚠️ O valor de acesso mensal é de R$ 400,00.</div>
</div>
""", unsafe_allow_html=True)

# INSTRUÇÕES
st.write("""
O pagamento deverá ser realizado via **PIX**, podendo ser feito de duas formas:

- Escaneando o **QR Code** abaixo;  
- Utilizando o **código Pix Copia e Cola**.

""")

st.markdown("---")

# ---------------------------------------------
# QR CODE NOVO
# ---------------------------------------------
st.markdown("<div style='text-align:center; font-weight:600; font-size:16px;'>QR Code para pagamento via PIX</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center;'>
    <img src="https://i.imgur.com/XcDbNoT.jpeg" width="260">
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------
# PIX COPIA E COLA + BOTÃO
# ---------------------------------------------
st.markdown('<div class="pix-box">', unsafe_allow_html=True)
st.markdown("**Pix Copia e Cola:**")

st.markdown(f'<div class="pix-codigo">{PIX_CODE}</div>', unsafe_allow_html=True)

components.html(copy_button_html, height=70)

st.markdown("</div>", unsafe_allow_html=True)

# ORIENTAÇÕES FINAIS
st.write("""
Após realizar o pagamento, entre em contato via  
📱 **WhatsApp: (88) 99976-2740**, enviando o **comprovante ou o código da transferência**.

Após a confirmação, o acesso será liberado.  
Obrigado pela confiança! 💎
""")

st.markdown("</div>", unsafe_allow_html=True)
