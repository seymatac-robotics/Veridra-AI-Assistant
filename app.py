import streamlit as st
import google.generativeai as genai
import time
import json
import os
from PIL import Image

# ==========================================
# 1. TEMEL AYARLAR VE TASARIM (CSS)
# ==========================================
st.set_page_config(page_title="Veridra - Gerçek Asistan", page_icon="🟣", layout="centered")

custom_css = """
<style>
    footer {visibility: hidden;}
    header {visibility: visible !important; background: transparent !important;}
    [data-testid="collapsedControl"] {visibility: visible !important;}
    header svg {fill: #f0e0ff !important; color: #f0e0ff !important;}
    
    .stApp {background: linear-gradient(135deg, #1e0b36 0%, #3d1b66 100%); color: #e0d0f0;}
    h1, h2, h3, h4, .stSubheader {color: #f0e0ff !important;}
    .stTextInput>div>div>input {background-color: #2a114f; color: #e0d0f0; border: 1px solid #6a3ab2;}
    .stButton>button {background-color: #6a3ab2; color: white; border-radius: 20px; border: none; transition: all 0.3s;}
    .stButton>button:hover {background-color: #8a5ad2; transform: scale(1.05);}
    
    [data-testid="stChatMessageUser"] {background-color: #f0e0ff; border-radius: 15px 15px 0px 15px; color: #1e0b36 !important; padding: 10px; margin-bottom: 10px;}
    [data-testid="stChatMessageAssistant"] {background-color: #4a217f; border-radius: 15px 15px 15px 0px; color: #e0d0f0 !important; padding: 10px; margin-bottom: 10px;}
    .slogan {font-style: italic; color: #bfa0df; font-size: 1.1em; margin-bottom: 20px; border-left: 3px solid #6a3ab2; padding-left: 10px;}
    
    [data-testid="stSidebar"] {background-color: #16072b !important;}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ==========================================
# 2. JSON HAFIZA FONKSİYONLARI 
# ==========================================
DOSYA_ADI = "veridra_hafiza.json"

def hafizayi_yukle():
    if os.path.exists(DOSYA_ADI):
        try:
            with open(DOSYA_ADI, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return None
    return None

def hafizayi_kaydet(chats):
    temiz_chats = {}
    for cid, chat in chats.items():
        temiz_mesajlar = []
        for msg in chat["messages"]:
            temiz_mesajlar.append({"role": msg["role"], "content": msg["content"]})
        
        temiz_chats[cid] = {
            "name": chat["name"],
            "is_hidden": chat["is_hidden"],
            "messages": temiz_mesajlar
        }
    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(temiz_chats, f, ensure_ascii=False, indent=4)

# ==========================================
# 3. API BAĞLANTISI VE MODEL
# ==========================================
API_KEY = "BURAYA_KENDI_API_ANAHTARINIZI_YAZIN" 
genai.configure(api_key=API_KEY)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except Exception as e:
    st.error(f"Model yüklenirken sorun oldu: {e}")

# ==========================================
# 4. VERİ YAPISI VE HAFIZA YÜKLEME
# ==========================================
if "authenticated" not in st.session_state: st.session_state.authenticated = False

if "chats" not in st.session_state:
    kayitli_veri = hafizayi_yukle()
    if kayitli_veri:
        st.session_state.chats = kayitli_veri
        st.session_state.current_chat_id = list(kayitli_veri.keys())[0]
    else:
        ilk_id = str(time.time())
        st.session_state.chats = {ilk_id: {"name": "Yeni Sohbet 1", "messages": [], "is_hidden": False}}
        st.session_state.current_chat_id = ilk_id

# ==========================================
# 5. GİRİŞ EKRANI
# ==========================================
if not st.session_state.authenticated:
    st.title("Veridra'ya Hoş Geldin")
    st.markdown('<div class="slogan">“Ben Veridra. Sana duymak istediklerini değil, bilmen gerekenleri söylerim.”</div>', unsafe_allow_html=True)
    pwd = st.text_input("Özel şifreni gir:", type="password")
    if st.button("Veridra'yı Aç"):
        if pwd == "robotik2026": 
            st.session_state.authenticated = True
            st.rerun()
        else: st.error("Hatalı şifre!")
else:
    # ==========================================
    # 6. YAN MENÜ 
    # ==========================================
    with st.sidebar:
        st.header("⚙️ Veridra Ayarları")
        secilen_mod = st.radio("Kişilik Modu:", ("👯‍♀️ Arkadaş Modu", "👩‍🏫 Hoca Modu"))
        st.divider()

        if st.button("➕ Yeni Sohbet Başlat"):
            yeni_id = str(time.time())
            st.session_state.chats[yeni_id] = {"name": f"Yeni Sohbet {len(st.session_state.chats) + 1}", "messages": [], "is_hidden": False}
            st.session_state.current_chat_id = yeni_id
            hafizayi_kaydet(st.session_state.chats)
            st.rerun()
            
        st.subheader("💬 Açık Sohbetler")
        for cid, chat_data in st.session_state.chats.items():
            if not chat_data["is_hidden"]:
                btn_label = f"▶ {chat_data['name']}" if cid == st.session_state.current_chat_id else chat_data["name"]
                if st.button(btn_label, key=f"btn_{cid}"):
                    st.session_state.current_chat_id = cid
                    st.rerun()

        st.divider()
        st.subheader("🕵️‍♀️ Gizli Kasa")
        kasa_sifre = st.text_input("Kasa Şifresi:", type="password", key="kasa_pwd")
        
        if kasa_sifre == "vdr05":
            st.success("Kasa Açıldı!")
            gizli_yok = True
            for cid, chat_data in st.session_state.chats.items():
                if chat_data["is_hidden"]:
                    gizli_yok = False
                    btn_label = f"🔒 {chat_data['name']}"
                    if st.button(btn_label, key=f"btn_hidden_{cid}"):
                        st.session_state.current_chat_id = cid
                        st.rerun()
            if gizli_yok:
                st.caption("Şu an kasada sohbet yok.")

    # ==========================================
    # 7. ANA SOHBET EKRANI
    # ==========================================
    current_id = st.session_state.current_chat_id
    current_chat = st.session_state.chats[current_id]

    st.title("🟣 Veridra")
    st.markdown('<div class="slogan">“Ben Veridra. Sana duymak istediklerini değil, bilmen gerekenleri söylerim.”</div>', unsafe_allow_html=True)

    with st.expander("⚙️ Bu Sohbetin Ayarları"):
        col1, col2 = st.columns(2)
        with col1:
            yeni_isim = st.text_input("Sohbet İsmi:", value=current_chat["name"])
            if st.button("İsmi Kaydet"):
                st.session_state.chats[current_id]["name"] = yeni_isim
                hafizayi_kaydet(st.session_state.chats)
                st.rerun()
        with col2:
            if not current_chat["is_hidden"]:
                if st.button("👁️‍🗨️ Bu Sohbeti Gizle"):
                    st.session_state.chats[current_id]["is_hidden"] = True
                    hafizayi_kaydet(st.session_state.chats)
                    st.rerun()
            else:
                if st.button("🔓 Açık Listeye Çıkar"):
                    st.session_state.chats[current_id]["is_hidden"] = False
                    hafizayi_kaydet(st.session_state.chats)
                    st.rerun()

    for message in current_chat["messages"]:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "image" in message:
                    st.image(message["image"], width=250)

    uploaded_file = st.file_uploader("Veridra'ya fotoğraf gönder (İsteğe bağlı)", type=["png", "jpg", "jpeg"])

    if prompt := st.chat_input("Veridra'ya yaz..."):
        img = None
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            
        user_msg_data = {"role": "user", "content": prompt}
        if img:
            user_msg_data["image"] = img 
            
        current_chat["messages"].append(user_msg_data)
        hafizayi_kaydet(st.session_state.chats)
        
        with st.chat_message("user"):
            st.markdown(prompt)
            if img:
                st.image(img, width=250)

        with st.chat_message("assistant"):
            try:
                # KARAKTER GÜNCELLEMESİ: Soru sorma yeteneği eklendi!
                if secilen_mod == "👯‍♀️ Arkadaş Modu":
                    system_instruction = (
                        "Senin adın Veridra. Kullanıcıya karşı sıcakkanlı ve seviyeli bir arkadaşsın. KESİNLİKLE laubali, cıvık veya argo bir dil kullanma. "
                        "Saygılı bir samimiyetin olsun. 'Dost acı söyler' felsefesiyle gerçekleri eğip bükmeden, net ve dürüst bir şekilde söyle. "
                        "ÖNEMLİ: Her cevabının en sonunda, sohbeti ilerletmek veya kullanıcıya yardımcı olmak için mutlaka ilgili bir soru sor (Örn: 'İstersen bu konunun şu kısmına da bakalım mı?', 'Sen bu konuda ne düşünüyorsun?' gibi)."
                    )
                else:
                    system_instruction = (
                        "Senin adın Veridra. Uzman, ciddi ve akademik bir eğitmensin. "
                        "ÖNEMLİ: Her açıklamanın en sonunda, öğrencinin konuyu kavradığından emin olmak veya pratik yapmasını sağlamak için pedagojik bir soru yönelt (Örn: 'Bu anlattıklarım doğrultusunda sence şu nasıl olurdu?', 'İstersen bu konuyla ilgili küçük bir örnek çözebiliriz, ne dersin?' gibi)."
                    )
                
                contents = [system_instruction, "Kullanıcı Mesajı:", prompt]
                if img:
                    contents.append(img) 
                
                response = model.generate_content(contents)
                st.markdown(response.text)
                
                current_chat["messages"].append({"role": "assistant", "content": response.text})
                hafizayi_kaydet(st.session_state.chats)
            except Exception as e:
                st.error(f"Veridra bir sorunla karşılaştı: {e}")