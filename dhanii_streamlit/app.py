import streamlit as st
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image, ImageDraw, ImageFont
import io

# ── Page config ──
st.set_page_config(
    page_title="🎀 Happy Birthday Dhanii!",
    page_icon="🎂",
    layout="centered"
)

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=DM+Sans:wght@400;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #fff5ee;
    }

    .stApp {
        background: linear-gradient(160deg, #fff0f5 0%, #f3e8ff 50%, #fff5ee 100%);
    }

    /* Hide streamlit default elements */
    #MainMenu, footer, header { visibility: hidden; }

    .title-text {
        font-family: 'Caveat', cursive;
        font-size: 3.2rem;
        color: #ff6b8a;
        text-align: center;
        line-height: 1.2;
        margin-bottom: 0;
    }
    .sub-text {
        font-family: 'Caveat', cursive;
        font-size: 1.6rem;
        color: #b09ab8;
        text-align: center;
        margin-top: 4px;
    }
    .card {
        background: white;
        border-radius: 24px;
        padding: 28px 24px;
        box-shadow: 0 12px 40px rgba(255,107,138,.15);
        border: 2px solid rgba(255,107,138,.12);
        margin: 16px 0;
        text-align: center;
    }
    .card p {
        color: #7a5c80;
        font-size: 1.05rem;
        line-height: 1.8;
    }
    .card em { color: #ff6b8a; font-style: normal; font-weight: 700; }
    .pink-link {
        color: #ff6b8a !important;
        font-weight: 700;
        font-size: 1.1rem;
        text-decoration: none;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #ff6b8a, #ff9a8b) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 36px !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        width: 100%;
        box-shadow: 0 8px 24px rgba(255,107,138,.35) !important;
        transition: transform .2s !important;
    }
    .stDownloadButton > button:hover {
        transform: translateY(-3px) !important;
    }
    .emoji-row {
        font-size: 2rem;
        text-align: center;
        letter-spacing: 8px;
        margin: 12px 0;
    }
    .url-box {
        background: #fff0f5;
        border: 2px dashed #ff6b8a;
        border-radius: 14px;
        padding: 14px 20px;
        font-family: monospace;
        font-size: .95rem;
        color: #4a3050;
        word-break: break-all;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── URL ──
BDAY_URL = "https://aditya5123.github.io/bday"

# ── Header ──
st.markdown('<div class="title-text">🎀 Happy Birthday Dhanii! 🎂</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Her special surprise is one scan away ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="emoji-row">🌸 💕 ✨ 💗 🌷</div>', unsafe_allow_html=True)

st.divider()

# ── Generate QR ──
def make_qr(url):
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    try:
        # Styled QR with rounded modules
        img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer(),
        )
    except Exception:
        img = qr.make_image(fill_color="#2b1d2e", back_color="white")

    img = img.convert("RGB")

    # Add decorative border
    W, H = img.size
    PAD = 30
    BOTTOM = 90
    canvas = Image.new("RGB", (W + PAD*2, H + PAD + BOTTOM), "#fff5ee")
    draw = ImageDraw.Draw(canvas)

    # Gradient bg
    for y in range(canvas.height):
        t = y / canvas.height
        draw.line([(0,y),(canvas.width,y)], fill=(
            int(255 - t*8), int(245 - t*18), int(238 - t*12)
        ))

    # Soft blobs
    draw.ellipse([-40,-40,130,130], fill="#ffd6e7")
    draw.ellipse([canvas.width-110,-40,canvas.width+30,130], fill="#ffe4ec")
    draw.ellipse([-30,canvas.height-110,110,canvas.height+30], fill="#ffd6e7")
    draw.ellipse([canvas.width-100,canvas.height-100,canvas.width+30,canvas.height+30], fill="#ffe4ec")

    # White card behind QR
    draw.rounded_rectangle([PAD-10, PAD-10, PAD+W+10, PAD+H+10], radius=16, fill="white")

    # Paste QR
    canvas.paste(img, (PAD, PAD))

    # Border rings
    draw.rounded_rectangle([PAD-16, PAD-16, PAD+W+16, PAD+H+16], radius=20, outline="#ff6b8a", width=5)
    draw.rounded_rectangle([PAD-22, PAD-22, PAD+W+22, PAD+H+22], radius=26, outline="#ffb347", width=3)

    # Bottom text
    mid = canvas.width // 2
    ty  = PAD + H + 18
    draw.text((mid, ty),    "🎀  For Dhanii  🎀",          fill="#ff6b8a", anchor="mm", font_size=26)
    draw.text((mid, ty+40), "Scan to open her surprise ✨",  fill="#a07890", anchor="mm", font_size=16)
    draw.text((mid, ty+66), "🌸  Happy Birthday  🌸",        fill="#ffb347", anchor="mm", font_size=16)

    return canvas

# Generate
with st.spinner("✨ Making her QR..."):
    qr_img = make_qr(BDAY_URL)

# Convert to bytes
buf = io.BytesIO()
qr_img.save(buf, format="PNG", quality=98)
buf.seek(0)

# ── Show QR ──
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.image(buf, use_container_width=True, caption="Scan this 🎀")

buf.seek(0)

# ── Download button ──
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.download_button(
        label="⬇️ Download QR Code",
        data=buf,
        file_name="dhanii_birthday_qr.png",
        mime="image/png",
    )

# ── Info card ──
st.markdown("""
<div class="card">
  <p>📲 When she scans this QR, it opens her <em>special birthday surprise</em> right in her browser.</p>
  <p>No app needed. Just her phone camera 🌸</p>
</div>
""", unsafe_allow_html=True)

# ── URL display ──
st.markdown("**🔗 Direct link (if she can't scan):**")
st.markdown(f'<div class="url-box">{BDAY_URL}</div>', unsafe_allow_html=True)
st.markdown(f'<a class="pink-link" href="{BDAY_URL}" target="_blank">👉 Open link directly</a>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#d4a0c0; font-family:'Caveat',cursive; font-size:1.3rem; margin-top:20px;">
    Made with 💕 for someone very special
</div>
""", unsafe_allow_html=True)
