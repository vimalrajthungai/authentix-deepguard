from pathlib import Path
import base64
import streamlit as st
from PIL import Image

st.set_page_config(page_title="AUTHENTIX | DeepGuard v8", page_icon="◉", layout="wide")

st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@500;600;700&display=swap');
.stApp{background:radial-gradient(circle at 10% 10%,rgba(0,120,255,.30),transparent 28%),radial-gradient(circle at 90% 20%,rgba(255,0,130,.18),transparent 28%),linear-gradient(135deg,#02040c,#071a35 52%,#02040b);color:#eefaff}
.block-container{max-width:1150px;padding-top:2.5rem;padding-bottom:1.5rem}
*{font-family:'Rajdhani',sans-serif}
.brand{font-family:'Orbitron',sans-serif;font-size:clamp(2rem,5vw,4rem);font-weight:800;letter-spacing:4px;color:#f4fbff;text-shadow:0 0 12px #17cfff,0 0 28px #145bff}
.subtitle{font-family:'Orbitron',sans-serif;color:#19ddff;letter-spacing:6px;font-size:clamp(.65rem,1.4vw,1rem);font-weight:700}
.ready{text-align:right;color:#55eaff;font-family:'Orbitron',sans-serif;font-size:.9rem;line-height:1.8;letter-spacing:1px;padding-top:1rem}
.ready span{border:1px solid #20d9ff;padding:10px 14px;box-shadow:0 0 18px rgba(0,210,255,.3)}
.panel{position:relative;margin-top:2rem;padding:2.4rem 2rem;border:1px solid #1bdcff;border-radius:25px;background:rgba(3,17,42,.84);box-shadow:0 0 30px rgba(0,170,255,.18),inset 0 0 30px rgba(0,100,255,.12);overflow:hidden}
.panel:before{content:"";position:absolute;top:0;left:35px;width:100px;height:24px;border-top:3px solid #19ddff;border-left:3px solid #19ddff;animation:glow 3s ease-in-out infinite}
.panel:after{content:"";position:absolute;right:35px;bottom:0;width:100px;height:24px;border-right:3px solid #19ddff;border-bottom:3px solid #19ddff;animation:glow 3s ease-in-out infinite}.panel:global{position:relative}.panel .scan-dot{position:absolute;width:7px;height:7px;border-radius:50%;background:#22e6ff;box-shadow:0 0 14px #22e6ff;animation:scan 5s linear infinite}@keyframes scan{0%{left:8%;top:18%;opacity:.15}25%{left:88%;top:18%;opacity:1}50%{left:88%;top:82%;opacity:.35}75%{left:8%;top:82%;opacity:1}100%{left:8%;top:18%;opacity:.15}}
@keyframes glow{50%{filter:drop-shadow(0 0 12px #19ddff)}}
.heading{font-family:'Orbitron',sans-serif;text-align:center;font-size:clamp(1.3rem,3vw,2.3rem);font-weight:800;letter-spacing:1px}
.desc{text-align:center;color:#b0d4f2;font-size:1.15rem;margin:.6rem 0 1.2rem}
.detecting{text-align:center;color:#36eaff;font-family:'Orbitron',sans-serif;letter-spacing:3px;font-size:.9rem;margin:1rem 0 1.2rem}
.detecting:before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:10px;background:#19e6ff;box-shadow:0 0 14px #19e6ff;animation:pulse 1.4s infinite}
@keyframes pulse{50%{opacity:.35;transform:scale(.65)}}
div[data-testid="stFileUploader"]{background:rgba(5,29,62,.45);border:1px dashed #24ddff;border-radius:16px;padding:12px;box-shadow:inset 0 0 25px rgba(0,170,255,.08)}
div.stButton, div[data-testid="stButton"]{width:100% !important;display:flex !important;justify-content:center !important;align-items:center !important;margin:1.8rem auto !important}
div[data-testid="stButton"] > button{display:block !important;margin:0 auto !important;min-width:0 !important}
div.stButton>button, div[data-testid="stButton"] button{width:520px !important;max-width:100% !important;min-height:3.5rem;border-radius:14px;border:1px solid #24e5ff;background:linear-gradient(90deg,#078dff,#214bff 48%,#8424ff);color:white;font-family:'Orbitron',sans-serif;font-weight:800;font-size:1.08rem;letter-spacing:1px;box-shadow:0 0 25px rgba(0,160,255,.42)}
div.stButton>button:hover{box-shadow:0 0 38px rgba(0,220,255,.85);transform:translateY(-2px)}
.result{margin-top:1.8rem;padding:2rem;border:1px solid #21dcff;border-radius:22px;background:rgba(3,18,42,.9);text-align:center;box-shadow:0 0 25px rgba(0,180,255,.16)}
.result-title{font-family:'Orbitron',sans-serif;color:#b4efff;letter-spacing:2px}.result-value{font-family:'Orbitron',sans-serif;font-size:3rem;font-weight:800;margin:.6rem 0 1.5rem}.real{color:#75ffd6;text-shadow:0 0 16px rgba(0,255,180,.55)}.fake{color:#ff6baf;text-shadow:0 0 16px rgba(255,30,130,.55)}
.score{max-width:850px;margin:1rem auto;text-align:left}.score-head{display:flex;justify-content:space-between;color:#e4f5ff;font-weight:700;font-size:1.05rem;margin-bottom:6px}.bar{height:18px;border-radius:30px;background:rgba(255,255,255,.10);overflow:hidden;border:1px solid rgba(150,220,255,.25)}.fill{height:100%;border-radius:30px;animation:fill .8s ease-out}.real-fill{background:linear-gradient(90deg,#00b894,#85ffe0);box-shadow:0 0 15px rgba(0,255,180,.6)}.fake-fill{background:linear-gradient(90deg,#ff267d,#ff9bc4);box-shadow:0 0 15px rgba(255,40,130,.6)}
@keyframes fill{from{width:0}}
.footer{text-align:center;color:#7598bd;letter-spacing:2px;margin-top:2rem;font-size:.8rem}
</style>
""", unsafe_allow_html=True)

# Fast, safe logo lookup: only common locations; no recursive full-folder scan.
base = Path(__file__).resolve().parent
logo_candidates = [
    base / "authentix_logo.png", base / "authentix-logo.png", base / "logo.png", base / "authentix.png",
    base / "DeepGuard" / "authentix_logo.png", base / "DeepGuard" / "logo.png",
]
logo_path = next((p for p in logo_candidates if p.is_file()), None)

left, right = st.columns([4, 1.6], gap="large")
with left:
    if logo_path:
        try:
            encoded = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
            logo_html = f'<img src="data:image/png;base64,{encoded}" style="width:58px;height:58px;object-fit:contain;filter:drop-shadow(0 0 12px #18dfff);margin-right:12px;">'
        except Exception:
            logo_html = '<span style="font-size:2.5rem;color:#20ddff">◉</span>'
    else:
        logo_html = '<span style="font-size:2.5rem;color:#20ddff;text-shadow:0 0 15px #20ddff">◉</span>'
    st.markdown(f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">{logo_html}<div><div class="brand">AUTHENTIX</div><div class="subtitle">DEEPFAKE DETECTION</div></div></div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="ready"><span>DEEPGUARD<br>ENGINE IS READY</span></div>', unsafe_allow_html=True)

st.markdown('<div class="panel"><span class="scan-dot"></span><div class="heading">DEEPGUARD DETECTING</div><div class="desc">Upload an image to check for deepfake.</div><div class="detecting">SYSTEM READY</div>', unsafe_allow_html=True)

uploaded = st.file_uploader("Image Upload • Supports JPG, PNG, WEBP", type=["jpg", "jpeg", "png", "webp"])
image = None
if uploaded is not None:
    try:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded image", use_container_width=True)
    except Exception as exc:
        st.error(f"Image error: {exc}")

@st.cache_resource(show_spinner=False)
def load_detector():
    import torch
    import torch.nn as nn
    import os
    import timm
    from torchvision import transforms
    from huggingface_hub import hf_hub_download

    class DeepfakeDetector(nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = timm.create_model("efficientnet_b4", pretrained=False, num_classes=0)
            self.head = nn.Sequential(
                nn.Linear(self.backbone.num_features, 512), nn.ReLU(), nn.Dropout(0.3),
                nn.Linear(512, 128), nn.ReLU(), nn.Dropout(0.3), nn.Linear(128, 1)
            )
        def forward(self, x):
            return self.head(self.backbone(x)).squeeze(-1)

    path = hf_hub_download(repo_id="Sowaiba01/deepguard-ai", filename="efficientnet_b4_deepguard_v2.pth")
    model = DeepfakeDetector()
    state = torch.load(path, map_location="cpu")
    if isinstance(state, dict) and "state_dict" in state:
        state = state["state_dict"]
    state = {k.replace("module.", "", 1): v for k, v in state.items()}
    result = model.load_state_dict(state, strict=False)
    if result.missing_keys or result.unexpected_keys:
        raise RuntimeError(f"Weights mismatch. Missing: {result.missing_keys}; Unexpected: {result.unexpected_keys}")
    model.eval()
    try:
        torch.set_num_threads(max(1, min(4, (os.cpu_count() or 2))))
    except Exception:
        pass
    transform = transforms.Compose([
        transforms.Resize((224, 224)), transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    return model, transform, torch

button_left, button_center, button_right = st.columns([1, 4, 1])
with button_center:
    run_analysis = st.button("▶  DEEPGUARD ANALYSIS", use_container_width=False)

if run_analysis:
    if image is None:
        st.warning("Please upload an image first.")
    else:
        with st.spinner("Analyzing with DeepGuard..."):
            # The cached model is loaded only once; later analyses reuse it.
            try:
                model, transform, torch = load_detector()
                tensor = transform(image).unsqueeze(0)
                with torch.inference_mode():
                    fake = float(torch.sigmoid(model(tensor)).item()) * 100.0
                fake = max(0.0, min(100.0, fake))
                real = 100.0 - fake
                # Classification rule: fake percentage >= 35% must display FAKE.
                threshold = 35.0
                label = "FAKE" if fake >= threshold else "REAL"
                css = "fake" if label == "FAKE" else "real"
                st.markdown(f'''<div class="result"><div class="result-title">DEEPGUARD RESULT</div><div class="result-value {css}">{label}</div><div class="score"><div class="score-head"><span>Real Percentage</span><span>{real:.2f}%</span></div><div class="bar"><div class="fill real-fill" style="width:{real:.2f}%"></div></div></div><div class="score"><div class="score-head"><span>Fake Percentage</span><span>{fake:.2f}%</span></div><div class="bar"><div class="fill fake-fill" style="width:{fake:.2f}%"></div></div></div></div>''', unsafe_allow_html=True)
            except Exception as exc:
                st.error("DeepGuard could not complete the analysis.")
                st.exception(exc)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="footer">AUTHENTIX | DEEPGUARD • INTELLIGENT IMAGE SECURITY ANALYSIS</div>', unsafe_allow_html=True)
