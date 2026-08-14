import os
import uuid
import datetime

import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
import cv2

import db
import ai_assistant
from report_generator import build_pdf_report
from translations import LANGS, UI, t, CLASS_LABELS, HOW_IT_WORKS, UNIQUE_FEATURES, DOCTOR_CHALLENGES

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Esophageal Cancer AI Screening",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_DIR, "patient_data", "images")
REPORT_DIR = os.path.join(BASE_DIR, "patient_data", "reports")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

db.init_db()

# =========================
# LOAD CSS
# =========================
def load_css():
    css_path = os.path.join(BASE_DIR, "assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# =========================
# SETTINGS
# =========================
MODEL_PATH = os.path.join(BASE_DIR, "best_cancer_model.h5")
IMG_SIZE = (224, 224)
DISPLAY_WIDTH = 380
CLASS_NAMES = ["Esophagitis", "Normal Z-line"]

# =========================
# SESSION STATE
# =========================
if "last_diagnosis" not in st.session_state:
    st.session_state.last_diagnosis = None
if "current_patient_id" not in st.session_state:
    st.session_state.current_patient_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "lang" not in st.session_state:
    st.session_state.lang = "en"

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)

# =========================
# IMAGE PROCESSING
# =========================
def deblur_pil_image(pil_img):
    img_np = np.array(pil_img.convert("RGB"))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharp_bgr = cv2.filter2D(img_bgr, -1, kernel)
    sharp_rgb = cv2.cvtColor(sharp_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(sharp_rgb)

def preprocess_img_pil(pil_img):
    pil_img = pil_img.convert("RGB").resize(IMG_SIZE)
    img_array = image.img_to_array(pil_img)
    img_array = np.expand_dims(img_array, axis=0)
    return preprocess_input(img_array)

def get_last_conv_layer(model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer
    return None

def make_gradcam_heatmap(img_array, model):
    last_conv = get_last_conv_layer(model)
    if last_conv is None:
        return None
    grad_model = tf.keras.models.Model([model.inputs], [last_conv.output, model.output])
    with tf.GradientTape() as tape:
        conv_outputs, preds = grad_model(img_array)
        loss = preds[:, 0]
    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()

def overlay_gradcam_on_image(pil_img, heatmap):
    if heatmap is None:
        return None
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    base_img = np.array(pil_img.convert("RGB"))
    heatmap = cv2.resize(heatmap, (base_img.shape[1], base_img.shape[0]))
    cam = cv2.addWeighted(base_img, 0.6, heatmap, 0.4, 0)
    return cam

def save_pil(pil_img, prefix):
    fname = f"{prefix}_{uuid.uuid4().hex[:8]}.png"
    fpath = os.path.join(IMG_DIR, fname)
    pil_img.save(fpath)
    return fpath

def save_cv(cv_img, prefix):
    fname = f"{prefix}_{uuid.uuid4().hex[:8]}.png"
    fpath = os.path.join(IMG_DIR, fname)
    cv2.imwrite(fpath, cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR))
    return fpath

# =========================
# HERO / HEADER
# =========================
def render_hero(lang):
    st.markdown(f"""
    <div class="hero-wrap">
        <div>
            <div class="hero-title">{t(lang, "hero_title")}</div>
            <div class="hero-sub">{t(lang, "hero_sub")}</div>
        </div>
        <div class="model3d-scene">
            <div class="model3d-cube">
                <div class="f1"></div><div class="f2"></div><div class="f3"></div>
                <div class="f4"></div><div class="f5"></div><div class="f6"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR - LANGUAGE + PATIENT CONTEXT
# =========================
with st.sidebar:
    lang_code_list = list(LANGS.keys())
    lang_labels = [LANGS[c] for c in lang_code_list]
    default_idx = lang_code_list.index(st.session_state.lang)
    chosen_label = st.selectbox(t(st.session_state.lang, "lang_label"), lang_labels, index=default_idx)
    st.session_state.lang = lang_code_list[lang_labels.index(chosen_label)]

lang = st.session_state.lang

with st.sidebar:
    st.markdown(f"### {t(lang, 'sidebar_patient_header')}")
    patients = db.get_all_patients()
    patient_options = {t(lang, "none_selected"): None}
    for p in patients:
        patient_options[f"{p['name']} (ID {p['id']}, {p['age'] or '?'}y)"] = p["id"]

    selected_label = st.selectbox(t(lang, "select_patient_label"), list(patient_options.keys()))
    st.session_state.current_patient_id = patient_options[selected_label]

    st.markdown("---")
    st.markdown(f"### {t(lang, 'sidebar_live_chat_header')}")
    st.caption(t(lang, "sidebar_live_chat_caption"))

    provider_options = {
        t(lang, "provider_auto"): "auto",
        "Anthropic (Claude)": "anthropic",
        "OpenAI": "openai",
        "Mistral AI": "mistral",
    }
    provider_choice_label = st.selectbox(t(lang, "provider_label"), list(provider_options.keys()))
    st.session_state["llm_provider"] = provider_options[provider_choice_label]

    api_key_input = st.text_input(
        t(lang, "api_key_label"), type="password", placeholder="Paste any supported provider's API key"
    )
    st.session_state["anthropic_api_key"] = api_key_input

    st.markdown("---")
    st.caption(t(lang, "sidebar_disclaimer"))

render_hero(lang)

# =========================
# TABS
# =========================
tab_detect, tab_assistant, tab_about, tab_patients, tab_reports = st.tabs([
    t(lang, "tab_detect"), t(lang, "tab_assistant"), t(lang, "tab_about"),
    t(lang, "tab_patients"), t(lang, "tab_reports"),
])

# =========================
# TAB 1: UPLOAD & DETECT
# =========================
with tab_detect:
    st.markdown(f"#### {t(lang, 'detect_header')}")

    if st.session_state.current_patient_id is None:
        st.info(t(lang, "detect_tip"))

    uploaded_file = st.file_uploader(t(lang, "upload_label"), type=["jpg", "jpeg", "png"])

    if uploaded_file:
        with st.spinner(t(lang, "loading_model")):
            model = load_model()

        original_img = Image.open(uploaded_file)
        deblurred_img = deblur_pil_image(original_img)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(t(lang, "original_image"))
            st.image(original_img, width=DISPLAY_WIDTH)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(t(lang, "deblurred_image"))
            st.image(deblurred_img, width=DISPLAY_WIDTH)
            st.markdown('</div>', unsafe_allow_html=True)

        with st.spinner(t(lang, "running_analysis")):
            img_array = preprocess_img_pil(deblurred_img)
            preds = model.predict(img_array)
            prob = float(preds[0][0])
            pred_idx = 1 if prob >= 0.5 else 0
            pred_name = CLASS_NAMES[pred_idx]
            confidence = prob if pred_idx == 1 else (1 - prob)

            heatmap = make_gradcam_heatmap(img_array, model)
            grad_img = overlay_gradcam_on_image(deblurred_img, heatmap)

        st.markdown(f"#### {t(lang, 'diagnosis_result')}")
        chip_class = "chip-danger" if pred_name == "Esophagitis" else "chip-safe"
        icon = "⚠️" if pred_name == "Esophagitis" else "✅"
        display_label = CLASS_LABELS.get(lang, CLASS_LABELS["en"]).get(pred_name, pred_name)
        st.markdown(f"""
        <div class="glass-card">
            <span class="metric-chip {chip_class}">{icon} {display_label}</span>
            <span class="metric-chip chip-info">{t(lang, "confidence")}: {confidence*100:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

        if grad_img is not None:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader(t(lang, "gradcam_header"))
            st.image(grad_img, width=700)
            st.caption(t(lang, "gradcam_caption"))
            st.markdown('</div>', unsafe_allow_html=True)

        st.session_state.last_diagnosis = {
            "prediction": pred_name,
            "confidence": confidence,
        }

        # Save to patient record
        st.markdown(f"#### {t(lang, 'save_result_header')}")
        if st.session_state.current_patient_id:
            notes = st.text_area(t(lang, "notes_label"))
            if st.button(t(lang, "save_button")):
                orig_path = save_pil(original_img, "orig")
                deblur_path = save_pil(deblurred_img, "deblur")
                grad_path = save_cv(grad_img, "gradcam") if grad_img is not None else None
                diag_id = db.add_diagnosis(
                    st.session_state.current_patient_id,
                    pred_name, confidence,
                    orig_path, deblur_path, grad_path,
                    doctor_notes=notes,
                )
                st.success(t(lang, "save_success", id=diag_id))
        else:
            st.warning(t(lang, "save_warning"))

# =========================
# TAB 2: AI ASSISTANT
# =========================
with tab_assistant:
    st.markdown(f"#### {t(lang, 'assistant_header')}")
    st.caption(t(lang, "assistant_caption"))

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    quick_cols = st.columns(4)
    quick_qs = t(lang, "quick_qs")
    for c, q in zip(quick_cols, quick_qs):
        if c.button(q):
            st.session_state["_pending_chat"] = q

    user_msg = st.chat_input(t(lang, "chat_placeholder"))
    pending = st.session_state.pop("_pending_chat", None)
    final_msg = user_msg or pending

    if final_msg:
        st.session_state.chat_history.append({"role": "user", "content": final_msg})
        api_key = st.session_state.get("anthropic_api_key", "")
        provider = st.session_state.get("llm_provider", "auto")
        if api_key:
            with st.spinner(t(lang, "assistant_thinking")):
                reply = ai_assistant.get_llm_response(
                    final_msg, api_key, provider=provider,
                    last_diagnosis=st.session_state.last_diagnosis,
                    history=[{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_history[:-1]],
                    ui_lang=lang,
                )
        else:
            reply = ai_assistant.get_offline_response(final_msg, st.session_state.last_diagnosis, ui_lang=lang)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

# =========================
# TAB 3: ABOUT / HOW THE AI WORKS
# =========================
with tab_about:
    hiw = HOW_IT_WORKS.get(lang, HOW_IT_WORKS["en"])
    st.markdown(f"### {hiw['title']}")
    st.caption(hiw["intro"])

    for step_title, step_desc in hiw["steps"]:
        st.markdown(f"""
        <div class="glass-card">
            <b>{step_title}</b><br>{step_desc}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"#### {hiw['limitations_title']}")
    for lim in hiw["limitations"]:
        st.markdown(f"- {lim}")

    st.markdown("---")
    uf = UNIQUE_FEATURES.get(lang, UNIQUE_FEATURES["en"])
    st.markdown(f"### {uf['title']}")
    for item in uf["items"]:
        st.markdown(f"- {item}")

    st.markdown("---")
    dc = DOCTOR_CHALLENGES.get(lang, DOCTOR_CHALLENGES["en"])
    st.markdown(f"### {dc['title']}")
    for problem, detail, solution in dc["items"]:
        with st.expander(f"❗ {problem}"):
            st.markdown(detail)
            st.markdown(f"✅ **{solution}**")

# =========================
# TAB 4: PATIENT MANAGEMENT
# =========================
with tab_patients:
    st.markdown(f"#### {t(lang, 'patients_header')}")

    with st.expander(t(lang, "add_patient_expander"), expanded=(len(db.get_all_patients()) == 0)):
        with st.form("add_patient_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            name = c1.text_input(t(lang, "name_label"))
            age = c2.number_input(t(lang, "age_label"), min_value=0, max_value=120, value=40)
            gender = c3.selectbox(t(lang, "gender_label"), ["Female", "Male", "Other"])
            contact = st.text_input(t(lang, "contact_label"))
            notes = st.text_area(t(lang, "general_notes_label"))
            submitted = st.form_submit_button(t(lang, "add_patient_button"))
            if submitted:
                if name.strip():
                    pid = db.add_patient(name.strip(), int(age), gender, contact, notes)
                    st.success(t(lang, "patient_added_success", name=name, id=pid))
                    st.rerun()
                else:
                    st.error(t(lang, "name_required_error"))

    st.markdown("---")
    st.markdown(f"#### {t(lang, 'all_patients_header')}")
    patients = db.get_all_patients()
    if not patients:
        st.info(t(lang, "no_patients_info"))
    else:
        for p in patients:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"**{p['name']}**  ·  {p['age']}y  ·  {p['gender']}")
                st.caption(f"{t(lang, 'contact_prefix')}: {p['contact'] or '—'}  |  {t(lang, 'added_prefix')}: {p['created_at'][:19].replace('T',' ')}")
                if p["notes"]:
                    st.caption(f"{t(lang, 'notes_prefix')}: {p['notes']}")
            with c2:
                if st.button(t(lang, "set_active_button"), key=f"active_{p['id']}"):
                    st.session_state.current_patient_id = p["id"]
                    st.rerun()
                if st.button(t(lang, "delete_button"), key=f"del_{p['id']}"):
                    db.delete_patient(p["id"])
                    st.rerun()

            diagnoses = db.get_diagnoses_for_patient(p["id"])
            if diagnoses:
                with st.expander(t(lang, "diagnosis_history_label", n=len(diagnoses))):
                    for d in diagnoses:
                        chip_class = "chip-danger" if d["prediction"] == "Esophagitis" else "chip-safe"
                        d_label = CLASS_LABELS.get(lang, CLASS_LABELS["en"]).get(d["prediction"], d["prediction"])
                        st.markdown(
                            f"<span class='metric-chip {chip_class}'>{d_label}</span> "
                            f"<span class='metric-chip chip-info'>{d['confidence']*100:.1f}%</span> "
                            f"&nbsp; <small>{d['created_at'][:19].replace('T',' ')}</small>",
                            unsafe_allow_html=True,
                        )
                        if d["doctor_notes"]:
                            st.caption(f"{t(lang, 'notes_prefix')}: {d['doctor_notes']}")
            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 5: REPORTS
# =========================
with tab_reports:
    st.markdown(f"#### {t(lang, 'reports_header')}")

    all_diag = db.get_all_diagnoses_with_patient()
    if not all_diag:
        st.info(t(lang, "no_diagnoses_info"))
    else:
        options = {
            f"#{d['id']} — {d['patient_name']} — {d['prediction']} ({d['created_at'][:19].replace('T',' ')})": d["id"]
            for d in all_diag
        }
        chosen_diag_label = st.selectbox(t(lang, "select_diagnosis_label"), list(options.keys()))
        chosen_id = options[chosen_diag_label]
        diagnosis = db.get_diagnosis(chosen_id)
        patient = db.get_patient(diagnosis["patient_id"])

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{t(lang, 'patient_label')}:** {patient['name']} ({patient['age']}y, {patient['gender']})")
            st.markdown(f"**{t(lang, 'result_label')}:** {diagnosis['prediction']}")
            st.markdown(f"**{t(lang, 'confidence_label')}:** {diagnosis['confidence']*100:.2f}%")
        with c2:
            if diagnosis["gradcam_image_path"] and os.path.exists(diagnosis["gradcam_image_path"]):
                st.image(diagnosis["gradcam_image_path"], width=260, caption="Grad-CAM")
        st.markdown('</div>', unsafe_allow_html=True)

        ai_summary = st.text_area(
            t(lang, "ai_summary_label"),
            value=ai_assistant.get_offline_response(
                "what does my result mean my result",
                {"prediction": diagnosis["prediction"], "confidence": diagnosis["confidence"]},
                ui_lang=lang,
            ),
            height=120,
        )

        if st.button(t(lang, "generate_pdf_button")):
            out_path = os.path.join(REPORT_DIR, f"report_{patient['id']}_{diagnosis['id']}.pdf")
            build_pdf_report(out_path, patient, diagnosis, ai_summary=ai_summary)
            with open(out_path, "rb") as f:
                st.download_button(
                    t(lang, "download_pdf_button"),
                    data=f.read(),
                    file_name=f"{patient['name'].replace(' ', '_')}_report.pdf",
                    mime="application/pdf",
                )
            st.success(t(lang, "report_generated_success"))

# =========================
# FOOTER
# =========================
st.markdown(
    f'<div class="app-footer">{t(lang, "footer_text")}</div>',
    unsafe_allow_html=True,
)
