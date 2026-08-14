"""
translations.py
Central place for every user-facing string in 3 languages:
  en = English, hi = Hindi (हिंदी), mr = Marathi (मराठी)

Adding a language later = add one more key to LANGS + fill in the same
dictionary shape. Everything in app.py reads from here so the whole UI,
the offline AI knowledge base, the "how it works" explainer and the
"doctor challenges" section all switch language together.
"""

LANGS = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "mr": "मराठी (Marathi)",
}

# ---------------------------------------------------------------------------
# Diagnosis class names shown to the user (kept bilingual: clinical term +
# plain-language translation) so a doctor or patient in any of the 3
# languages instantly understands what the label means.
# ---------------------------------------------------------------------------
CLASS_LABELS = {
    "en": {
        "Esophagitis": "Esophagitis (inflammation of the food pipe)",
        "Normal Z-line": "Normal Z-line (no abnormality detected)",
    },
    "hi": {
        "Esophagitis": "इसोफेजाइटिस (भोजन-नली में सूजन)",
        "Normal Z-line": "सामान्य Z-लाइन (कोई असामान्यता नहीं मिली)",
    },
    "mr": {
        "Esophagitis": "इसोफेजायटिस (अन्ननलिकेत दाह/सूज)",
        "Normal Z-line": "सामान्य Z-रेषा (कोणतीही असामान्यता आढळली नाही)",
    },
}

# ---------------------------------------------------------------------------
# UI STRINGS
# ---------------------------------------------------------------------------
UI = {
    "en": {
        "hero_title": "🩺 Esophageal Cancer AI Screening",
        "hero_sub": "Upload • Detect • Ask AI Assistant • Manage Patients • Export PDF Report",
        "lang_label": "🌐 App Language",
        "sidebar_patient_header": "👤 Active Patient",
        "select_patient_label": "Select patient for this session",
        "none_selected": "— None selected —",
        "sidebar_live_chat_header": "🔑 Optional: Live AI Chat",
        "sidebar_live_chat_caption": (
            "Add an API key from any supported provider (Anthropic, OpenAI, or "
            "Mistral) to upgrade the AI Assistant tab from offline knowledge-base "
            "answers to live, more conversational chat that can read and reply "
            "fluently in ANY language you type in — Hindi, Marathi, English, "
            "Hinglish, or anything else."
        ),
        "provider_label": "AI Provider",
        "provider_auto": "Auto-detect from key",
        "api_key_label": "API Key",
        "assistant_thinking": "Thinking...",
        "sidebar_disclaimer": (
            "⚠️ Educational demo only — not a certified medical device. "
            "Always confirm results with a licensed physician."
        ),
        "tab_detect": "🔬 Upload & Detect",
        "tab_assistant": "🤖 AI Assistant",
        "tab_about": "🧠 How the AI Works",
        "tab_patients": "🗂️ Patient Management",
        "tab_reports": "📄 Reports",
        "detect_header": "Upload an endoscopic image to screen for esophagitis",
        "detect_tip": (
            "Tip: select or add a patient in the sidebar / Patient Management tab "
            "so this result can be saved to their history."
        ),
        "upload_label": "Upload Image",
        "loading_model": "Loading model...",
        "original_image": "Original Image",
        "deblurred_image": "Deblurred Image",
        "running_analysis": "Running AI analysis...",
        "diagnosis_result": "Diagnosis Result",
        "confidence": "Confidence",
        "gradcam_header": "Grad-CAM — Model Attention Map",
        "gradcam_caption": "Highlighted regions show what most influenced the AI's prediction.",
        "save_result_header": "Save this result",
        "notes_label": "Optional clinician notes to attach to this diagnosis",
        "save_button": "💾 Save diagnosis to patient record",
        "save_success": "Saved diagnosis #{id} to patient record. Go to the Reports tab to export a PDF.",
        "save_warning": "Select a patient in the sidebar to save this result to their history.",
        "assistant_header": "🤖 Ask the AI Health Assistant",
        "assistant_caption": (
            "Trained on esophageal cancer, esophagitis, Barrett's esophagus and "
            "reflux-related knowledge. Type in English, Hindi, Marathi, or a mix — "
            "the assistant will try to understand and reply in the same language. "
            "Ask about symptoms, risk factors, prevention, treatment overview, or "
            "what your latest scan result means."
        ),
        "quick_qs": [
            "What is esophagitis?",
            "What are the symptoms?",
            "How can I prevent it?",
            "What does my result mean?",
        ],
        "chat_placeholder": "Type your question about esophageal health...",
        "patients_header": "🗂️ Patient Management",
        "add_patient_expander": "➕ Add a new patient",
        "name_label": "Full name *",
        "age_label": "Age",
        "gender_label": "Gender",
        "contact_label": "Contact (phone / email)",
        "general_notes_label": "General medical notes (history, allergies, etc.)",
        "add_patient_button": "Add patient",
        "name_required_error": "Name is required.",
        "patient_added_success": "Patient '{name}' added with ID {id}.",
        "all_patients_header": "All Patients",
        "no_patients_info": "No patients yet. Add one above.",
        "contact_prefix": "Contact",
        "added_prefix": "Added",
        "notes_prefix": "Notes",
        "set_active_button": "Set active",
        "delete_button": "🗑️ Delete",
        "diagnosis_history_label": "📋 Diagnosis history ({n})",
        "reports_header": "📄 Generate PDF Report",
        "no_diagnoses_info": "No saved diagnoses yet. Run a detection and save it to a patient record first.",
        "select_diagnosis_label": "Select a saved diagnosis to export",
        "patient_label": "Patient",
        "result_label": "Result",
        "confidence_label": "Confidence",
        "ai_summary_label": "AI Assistant summary to include in report (optional)",
        "generate_pdf_button": "📄 Generate PDF Report",
        "download_pdf_button": "⬇️ Download PDF Report",
        "report_generated_success": "Report generated!",
        "footer_text": (
            "Esophageal Cancer AI Screening Demo · For educational/research purposes "
            "only · Not a substitute for professional medical advice"
        ),
    },
    "hi": {
        "hero_title": "🩺 इसोफेजियल कैंसर AI स्क्रीनिंग",
        "hero_sub": "अपलोड करें • जांच करें • AI सहायक से पूछें • मरीज़ों को मैनेज करें • PDF रिपोर्ट निकालें",
        "lang_label": "🌐 ऐप की भाषा",
        "sidebar_patient_header": "👤 सक्रिय मरीज़",
        "select_patient_label": "इस सेशन के लिए मरीज़ चुनें",
        "none_selected": "— कोई नहीं चुना गया —",
        "sidebar_live_chat_header": "🔑 वैकल्पिक: लाइव AI चैट",
        "sidebar_live_chat_caption": (
            "किसी भी सपोर्टेड प्रोवाइडर (Anthropic, OpenAI, या Mistral) की API key डालने "
            "पर AI सहायक टैब ऑफ़लाइन नॉलेज-बेस जवाबों से अपग्रेड होकर लाइव, ज़्यादा बातचीत "
            "जैसी चैट बन जाता है, जो आपकी टाइप की गई किसी भी भाषा — हिंदी, मराठी, अंग्रेज़ी, "
            "या हिंग्लिश — को समझकर उसी भाषा में जवाब दे सकता है।"
        ),
        "provider_label": "AI प्रोवाइडर",
        "provider_auto": "Key से अपने-आप पहचानें",
        "api_key_label": "API Key",
        "assistant_thinking": "सोच रहा हूं...",
        "sidebar_disclaimer": (
            "⚠️ यह केवल एक शैक्षणिक (educational) डेमो है — यह कोई प्रमाणित मेडिकल डिवाइस "
            "नहीं है। कृपया परिणामों की पुष्टि हमेशा एक लाइसेंस-प्राप्त डॉक्टर से करवाएं।"
        ),
        "tab_detect": "🔬 अपलोड और जांच",
        "tab_assistant": "🤖 AI सहायक",
        "tab_about": "🧠 AI कैसे काम करता है",
        "tab_patients": "🗂️ मरीज़ प्रबंधन",
        "tab_reports": "📄 रिपोर्ट्स",
        "detect_header": "इसोफेगाइटिस की जांच के लिए एंडोस्कोपिक इमेज अपलोड करें",
        "detect_tip": (
            "सुझाव: साइडबार या 'मरीज़ प्रबंधन' टैब में मरीज़ चुनें/जोड़ें ताकि यह परिणाम "
            "उनकी हिस्ट्री में सेव हो सके।"
        ),
        "upload_label": "इमेज अपलोड करें",
        "loading_model": "मॉडल लोड हो रहा है...",
        "original_image": "मूल छवि (Original Image)",
        "deblurred_image": "डीब्लर की गई छवि (Deblurred)",
        "running_analysis": "AI विश्लेषण चल रहा है...",
        "diagnosis_result": "जांच परिणाम",
        "confidence": "विश्वास स्तर (Confidence)",
        "gradcam_header": "Grad-CAM — मॉडल ध्यान मानचित्र",
        "gradcam_caption": "हाइलाइट किए गए हिस्से दिखाते हैं कि AI के फैसले पर सबसे ज़्यादा किस चीज़ का असर पड़ा।",
        "save_result_header": "यह परिणाम सेव करें",
        "notes_label": "इस जांच के साथ जोड़ने के लिए डॉक्टर के नोट्स (वैकल्पिक)",
        "save_button": "💾 जांच को मरीज़ के रिकॉर्ड में सेव करें",
        "save_success": "जांच #{id} मरीज़ के रिकॉर्ड में सेव हो गई। PDF निकालने के लिए 'रिपोर्ट्स' टैब में जाएं।",
        "save_warning": "इस परिणाम को हिस्ट्री में सेव करने के लिए साइडबार में एक मरीज़ चुनें।",
        "assistant_header": "🤖 AI हेल्थ असिस्टेंट से पूछें",
        "assistant_caption": (
            "यह असिस्टेंट इसोफेजियल कैंसर, इसोफेजाइटिस, बैरेट्स इसोफेगस और रिफ्लक्स "
            "से जुड़ी जानकारी पर आधारित है। अंग्रेज़ी, हिंदी, मराठी या मिली-जुली भाषा "
            "में टाइप करें — असिस्टेंट उसी भाषा में समझकर जवाब देने की कोशिश करेगा। "
            "लक्षण, जोखिम कारक, बचाव, इलाज या अपने स्कैन परिणाम का मतलब पूछ सकते हैं।"
        ),
        "quick_qs": [
            "इसोफेजाइटिस क्या है?",
            "इसके लक्षण क्या हैं?",
            "मैं इसे कैसे रोक सकता/सकती हूँ?",
            "मेरे परिणाम का क्या मतलब है?",
        ],
        "chat_placeholder": "इसोफेजियल स्वास्थ्य के बारे में अपना सवाल टाइप करें...",
        "patients_header": "🗂️ मरीज़ प्रबंधन",
        "add_patient_expander": "➕ नया मरीज़ जोड़ें",
        "name_label": "पूरा नाम *",
        "age_label": "उम्र",
        "gender_label": "लिंग",
        "contact_label": "संपर्क (फ़ोन / ईमेल)",
        "general_notes_label": "सामान्य मेडिकल नोट्स (इतिहास, एलर्जी आदि)",
        "add_patient_button": "मरीज़ जोड़ें",
        "name_required_error": "नाम भरना आवश्यक है।",
        "patient_added_success": "मरीज़ '{name}' को ID {id} के साथ जोड़ा गया।",
        "all_patients_header": "सभी मरीज़",
        "no_patients_info": "अभी कोई मरीज़ नहीं है। ऊपर से एक जोड़ें।",
        "contact_prefix": "संपर्क",
        "added_prefix": "जोड़ा गया",
        "notes_prefix": "नोट्स",
        "set_active_button": "सक्रिय करें",
        "delete_button": "🗑️ हटाएं",
        "diagnosis_history_label": "📋 जांच इतिहास ({n})",
        "reports_header": "📄 PDF रिपोर्ट बनाएं",
        "no_diagnoses_info": "अभी कोई सेव की गई जांच नहीं है। पहले एक जांच करें और उसे मरीज़ के रिकॉर्ड में सेव करें।",
        "select_diagnosis_label": "एक्सपोर्ट के लिए सेव की गई जांच चुनें",
        "patient_label": "मरीज़",
        "result_label": "परिणाम",
        "confidence_label": "विश्वास स्तर",
        "ai_summary_label": "रिपोर्ट में शामिल करने के लिए AI सहायक सारांश (वैकल्पिक)",
        "generate_pdf_button": "📄 PDF रिपोर्ट बनाएं",
        "download_pdf_button": "⬇️ PDF रिपोर्ट डाउनलोड करें",
        "report_generated_success": "रिपोर्ट बन गई!",
        "footer_text": (
            "इसोफेजियल कैंसर AI स्क्रीनिंग डेमो · केवल शैक्षणिक/शोध उद्देश्यों के लिए · "
            "यह पेशेवर मेडिकल सलाह का विकल्प नहीं है"
        ),
    },
    "mr": {
        "hero_title": "🩺 इसोफेजियल कॅन्सर AI स्क्रीनिंग",
        "hero_sub": "अपलोड करा • तपासा • AI सहाय्यकाला विचारा • रुग्ण व्यवस्थापन • PDF अहवाल डाउनलोड करा",
        "lang_label": "🌐 अ‍ॅपची भाषा",
        "sidebar_patient_header": "👤 सक्रिय रुग्ण",
        "select_patient_label": "या सत्रासाठी रुग्ण निवडा",
        "none_selected": "— कोणीही निवडलेले नाही —",
        "sidebar_live_chat_header": "🔑 पर्यायी: लाइव्ह AI चॅट",
        "sidebar_live_chat_caption": (
            "कोणत्याही सपोर्टेड प्रोवायडरची (Anthropic, OpenAI, किंवा Mistral) API key "
            "दिल्यास AI सहाय्यक टॅब ऑफलाइन नॉलेज-बेस उत्तरांऐवजी लाइव्ह, अधिक संवादात्मक "
            "चॅटमध्ये अपग्रेड होतो, जो तुम्ही टाइप केलेली कोणतीही भाषा — मराठी, हिंदी, इंग्रजी "
            "किंवा मिश्र भाषा — समजून त्याच भाषेत उत्तर देऊ शकतो."
        ),
        "provider_label": "AI प्रोवायडर",
        "provider_auto": "Key वरून आपोआप ओळखा",
        "api_key_label": "API Key",
        "assistant_thinking": "विचार करत आहे...",
        "sidebar_disclaimer": (
            "⚠️ हे फक्त एक शैक्षणिक डेमो आहे — हे प्रमाणित वैद्यकीय उपकरण नाही. "
            "कृपया निकालाची खात्री नेहमी परवानाधारक डॉक्टरांकडून करून घ्या."
        ),
        "tab_detect": "🔬 अपलोड आणि तपासणी",
        "tab_assistant": "🤖 AI सहाय्यक",
        "tab_about": "🧠 AI कसे काम करते",
        "tab_patients": "🗂️ रुग्ण व्यवस्थापन",
        "tab_reports": "📄 अहवाल",
        "detect_header": "इसोफेजायटिसच्या तपासणीसाठी एंडोस्कोपिक इमेज अपलोड करा",
        "detect_tip": (
            "टीप: साइडबार किंवा 'रुग्ण व्यवस्थापन' टॅबमध्ये रुग्ण निवडा/जोडा, "
            "जेणेकरून हा निकाल त्यांच्या इतिहासात जतन करता येईल."
        ),
        "upload_label": "इमेज अपलोड करा",
        "loading_model": "मॉडेल लोड होत आहे...",
        "original_image": "मूळ प्रतिमा (Original Image)",
        "deblurred_image": "स्पष्ट केलेली प्रतिमा (Deblurred)",
        "running_analysis": "AI विश्लेषण सुरू आहे...",
        "diagnosis_result": "निदान निकाल",
        "confidence": "विश्वासार्हता (Confidence)",
        "gradcam_header": "Grad-CAM — मॉडेल लक्ष नकाशा",
        "gradcam_caption": "हायलाइट केलेले भाग दाखवतात की AI च्या निर्णयावर कशाचा सर्वाधिक परिणाम झाला.",
        "save_result_header": "हा निकाल जतन करा",
        "notes_label": "या निदानासोबत जोडण्यासाठी डॉक्टरांच्या नोंदी (पर्यायी)",
        "save_button": "💾 निदान रुग्णाच्या नोंदीत जतन करा",
        "save_success": "निदान #{id} रुग्णाच्या नोंदीत जतन झाले. PDF काढण्यासाठी 'अहवाल' टॅबवर जा.",
        "save_warning": "हा निकाल इतिहासात जतन करण्यासाठी साइडबारमध्ये रुग्ण निवडा.",
        "assistant_header": "🤖 AI आरोग्य सहाय्यकाला विचारा",
        "assistant_caption": (
            "हा सहाय्यक इसोफेजियल कॅन्सर, इसोफेजायटिस, बॅरेट्स इसोफॅगस आणि रिफ्लक्सशी "
            "संबंधित माहितीवर आधारित आहे. इंग्रजी, हिंदी, मराठी किंवा मिश्र भाषेत टाइप करा — "
            "सहाय्यक तीच भाषा समजून त्याच भाषेत उत्तर देण्याचा प्रयत्न करेल. लक्षणे, जोखीम "
            "घटक, प्रतिबंध, उपचार किंवा तुमच्या स्कॅन निकालाचा अर्थ विचारू शकता."
        ),
        "quick_qs": [
            "इसोफेजायटिस म्हणजे काय?",
            "याची लक्षणे काय आहेत?",
            "मी हे कसे टाळू शकतो/शकते?",
            "माझ्या निकालाचा अर्थ काय आहे?",
        ],
        "chat_placeholder": "इसोफेजियल आरोग्याविषयी तुमचा प्रश्न टाइप करा...",
        "patients_header": "🗂️ रुग्ण व्यवस्थापन",
        "add_patient_expander": "➕ नवीन रुग्ण जोडा",
        "name_label": "पूर्ण नाव *",
        "age_label": "वय",
        "gender_label": "लिंग",
        "contact_label": "संपर्क (फोन / ईमेल)",
        "general_notes_label": "सामान्य वैद्यकीय नोंदी (इतिहास, अ‍ॅलर्जी इ.)",
        "add_patient_button": "रुग्ण जोडा",
        "name_required_error": "नाव भरणे आवश्यक आहे.",
        "patient_added_success": "रुग्ण '{name}' ID {id} सह जोडला गेला.",
        "all_patients_header": "सर्व रुग्ण",
        "no_patients_info": "अजून कोणताही रुग्ण नाही. वर एक जोडा.",
        "contact_prefix": "संपर्क",
        "added_prefix": "जोडले",
        "notes_prefix": "नोंदी",
        "set_active_button": "सक्रिय करा",
        "delete_button": "🗑️ काढून टाका",
        "diagnosis_history_label": "📋 निदान इतिहास ({n})",
        "reports_header": "📄 PDF अहवाल तयार करा",
        "no_diagnoses_info": "अजून कोणतेही जतन केलेले निदान नाही. आधी एक तपासणी करा आणि रुग्णाच्या नोंदीत जतन करा.",
        "select_diagnosis_label": "एक्सपोर्टसाठी जतन केलेले निदान निवडा",
        "patient_label": "रुग्ण",
        "result_label": "निकाल",
        "confidence_label": "विश्वासार्हता",
        "ai_summary_label": "अहवालात समाविष्ट करण्यासाठी AI सहाय्यक सारांश (पर्यायी)",
        "generate_pdf_button": "📄 PDF अहवाल तयार करा",
        "download_pdf_button": "⬇️ PDF अहवाल डाउनलोड करा",
        "report_generated_success": "अहवाल तयार झाला!",
        "footer_text": (
            "इसोफेजियल कॅन्सर AI स्क्रीनिंग डेमो · केवळ शैक्षणिक/संशोधन हेतूंसाठी · "
            "हा व्यावसायिक वैद्यकीय सल्ल्याचा पर्याय नाही"
        ),
    },
}


def t(lang, key, **kwargs):
    """Fetch a UI string in the given language, falling back to English."""
    s = UI.get(lang, UI["en"]).get(key, UI["en"].get(key, key))
    if kwargs:
        try:
            return s.format(**kwargs)
        except Exception:
            return s
    return s


# ---------------------------------------------------------------------------
# "HOW THE AI WORKS" — explains the detection pipeline step by step, in
# plain language, in each supported language.
# ---------------------------------------------------------------------------
HOW_IT_WORKS = {
    "en": {
        "title": "🧠 How does this AI actually detect esophagitis?",
        "intro": (
            "This isn't a black box — here is the exact step-by-step pipeline that "
            "runs every time you upload an image, from pixels to prediction."
        ),
        "steps": [
            ("1. Image Upload", "You upload an endoscopic image (JPG/PNG) captured during an upper GI endoscopy."),
            ("2. Deblurring / Sharpening", "Endoscopy images are often slightly blurry due to camera motion, mucus, or low light. A sharpening filter (an OpenCV convolution kernel) is applied to enhance edges and tissue texture before analysis, so faint patterns aren't missed."),
            ("3. Preprocessing & Normalization", "The (deblurred) image is resized to 224×224 pixels and normalized using EfficientNet's standard preprocessing, matching the exact format the model was trained on."),
            ("4. CNN Model Inference", "A convolutional neural network (an EfficientNet-based binary classifier, saved as best_cancer_model.h5) scans the image for visual patterns — redness, mucosal breaks, irregular texture — associated with esophagitis vs. a normal Z-line."),
            ("5. Confidence Score", "The model outputs a probability between 0 and 1. This is converted into a percentage confidence for whichever class (Esophagitis / Normal Z-line) it predicts — so you see both the label AND how sure the model is."),
            ("6. Grad-CAM Explainability", "Grad-CAM (Gradient-weighted Class Activation Mapping) traces the gradients back through the last convolutional layer to produce a heatmap showing exactly which pixels most influenced the decision. Warm colors (red/yellow) = high influence. This turns the AI from a 'black box' into something a doctor can visually cross-check."),
            ("7. Result + Save", "The label, confidence and Grad-CAM overlay are shown together. If a patient is selected, the doctor can attach clinical notes and save the full result (images + prediction) into that patient's permanent history."),
            ("8. PDF Report", "A one-click PDF report bundles the patient details, the images, the AI result, and a plain-language AI-generated summary — ready to hand to the patient or file in their chart."),
        ],
        "limitations_title": "⚠️ Honest limitations of this AI",
        "limitations": [
            "It is a binary screening classifier (Esophagitis vs. Normal Z-line only) — it does NOT stage cancer, grade severity, or detect every GI condition.",
            "Accuracy depends entirely on the training dataset; performance can drop on image types, scopes, or populations very different from what it was trained on.",
            "A high confidence score is a statistical measure, not medical certainty — it can still be wrong, especially near the 50% boundary.",
            "It cannot replace biopsy, histopathology, or a gastroenterologist's clinical judgement — it is a triage/screening aid only.",
        ],
    },
    "hi": {
        "title": "🧠 यह AI वास्तव में इसोफेजाइटिस कैसे पहचानता है?",
        "intro": (
            "यह कोई 'ब्लैक बॉक्स' नहीं है — जब भी आप कोई इमेज अपलोड करते हैं, "
            "तो पिक्सल से लेकर परिणाम तक ठीक यही पूरी प्रक्रिया चलती है।"
        ),
        "steps": [
            ("1. इमेज अपलोड", "आप ऊपरी GI एंडोस्कोपी के दौरान ली गई एक एंडोस्कोपिक इमेज (JPG/PNG) अपलोड करते हैं।"),
            ("2. डीब्लरिंग / शार्पनिंग", "कैमरे की हलचल, बलगम या कम रोशनी की वजह से एंडोस्कोपी इमेज अक्सर थोड़ी धुंधली होती है। विश्लेषण से पहले एक शार्पनिंग फ़िल्टर (OpenCV convolution kernel) लगाया जाता है ताकि किनारे और टिशू की बनावट साफ़ दिखे और कोई हल्का पैटर्न छूट न जाए।"),
            ("3. प्रीप्रोसेसिंग और नॉर्मलाइज़ेशन", "डीब्लर की गई इमेज को 224×224 पिक्सल में बदला जाता है और EfficientNet के मानक तरीके से नॉर्मलाइज़ किया जाता है, ठीक वैसे ही जैसे मॉडल को ट्रेन करते समय किया गया था।"),
            ("4. CNN मॉडल इन्फ़रेंस", "एक कन्वोल्यूशनल न्यूरल नेटवर्क (EfficientNet-आधारित बाइनरी क्लासिफ़ायर, फ़ाइल best_cancer_model.h5) इमेज में लालिमा, म्यूकोसल टूट-फूट और असामान्य बनावट जैसे पैटर्न ढूंढता है, जो इसोफेजाइटिस बनाम सामान्य Z-लाइन को अलग करते हैं।"),
            ("5. विश्वास स्तर (Confidence Score)", "मॉडल 0 से 1 के बीच एक प्रोबेबिलिटी देता है, जिसे प्रतिशत विश्वास स्तर में बदला जाता है — यानी आपको लेबल के साथ-साथ यह भी पता चलता है कि मॉडल कितना आश्वस्त है।"),
            ("6. Grad-CAM व्याख्या (Explainability)", "Grad-CAM आखिरी convolutional लेयर तक ग्रेडिएंट्स को वापस ट्रेस करके एक हीटमैप बनाता है, जो दिखाता है कि किस हिस्से ने फैसले को सबसे ज़्यादा प्रभावित किया। गर्म रंग (लाल/पीला) = ज़्यादा प्रभाव। इससे डॉक्टर AI के फैसले को अपनी आंखों से भी जांच सकते हैं।"),
            ("7. परिणाम + सेव", "लेबल, विश्वास स्तर और Grad-CAM एक साथ दिखाए जाते हैं। मरीज़ चुना गया हो तो डॉक्टर नोट्स जोड़कर पूरा परिणाम मरीज़ की स्थायी हिस्ट्री में सेव कर सकते हैं।"),
            ("8. PDF रिपोर्ट", "एक क्लिक में मरीज़ की जानकारी, इमेज, AI परिणाम और एक आसान भाषा में AI-जनित सारांश वाली PDF रिपोर्ट तैयार होती है — मरीज़ को देने या फ़ाइल में रखने के लिए तैयार।"),
        ],
        "limitations_title": "⚠️ इस AI की ईमानदार सीमाएं",
        "limitations": [
            "यह केवल एक बाइनरी स्क्रीनिंग क्लासिफ़ायर है (इसोफेजाइटिस बनाम सामान्य Z-लाइन) — यह कैंसर की स्टेज या गंभीरता नहीं बताता, और हर GI बीमारी नहीं पकड़ता।",
            "इसकी सटीकता पूरी तरह ट्रेनिंग डेटा पर निर्भर है; अलग तरह की इमेज, स्कोप या मरीज़ आबादी पर प्रदर्शन कम हो सकता है।",
            "ऊंचा विश्वास स्तर सांख्यिकीय माप है, मेडिकल निश्चितता नहीं — यह गलत भी हो सकता है, खासकर 50% के आसपास।",
            "यह बायोप्सी, हिस्टोपैथोलॉजी या गैस्ट्रोएंटरोलॉजिस्ट के क्लिनिकल फैसले की जगह नहीं ले सकता — यह सिर्फ़ एक स्क्रीनिंग/ट्राइएज सहायक है।",
        ],
    },
    "mr": {
        "title": "🧠 हे AI प्रत्यक्षात इसोफेजायटिस कसे ओळखते?",
        "intro": (
            "हे कोणतेही 'ब्लॅक बॉक्स' नाही — तुम्ही इमेज अपलोड करता तेव्हा पिक्सेलपासून "
            "निकालापर्यंत नेमकी हीच प्रक्रिया चालते."
        ),
        "steps": [
            ("१. इमेज अपलोड", "तुम्ही अप्पर GI एंडोस्कोपीदरम्यान घेतलेली एंडोस्कोपिक इमेज (JPG/PNG) अपलोड करता."),
            ("२. डीब्लरिंग / शार्पनिंग", "कॅमेऱ्याची हालचाल, चिकट स्राव किंवा कमी प्रकाशामुळे एंडोस्कोपी इमेज बऱ्याचदा थोडी अस्पष्ट असते. विश्लेषणापूर्वी एक शार्पनिंग फिल्टर (OpenCV convolution kernel) वापरला जातो, ज्यामुळे कडा आणि उतींची रचना स्पष्ट दिसते आणि बारीक नमुना निसटत नाही."),
            ("३. प्रीप्रोसेसिंग आणि नॉर्मलायझेशन", "स्पष्ट केलेली इमेज 224×224 पिक्सेलमध्ये रीसाइझ केली जाते आणि EfficientNet च्या प्रमाणित पद्धतीने नॉर्मलाइझ केली जाते — मॉडेल प्रशिक्षित करताना वापरलेल्या स्वरूपाशी अगदी जुळणारी."),
            ("४. CNN मॉडेल इन्फरन्स", "एक कन्व्होल्यूशनल न्यूरल नेटवर्क (EfficientNet-आधारित बायनरी क्लासिफायर, फाइल best_cancer_model.h5) इमेजमध्ये लालसरपणा, म्युकोसल तुटणे आणि असामान्य पोत यासारखे नमुने शोधते, जे इसोफेजायटिस विरुद्ध सामान्य Z-रेषा वेगळे करतात."),
            ("५. विश्वासार्हता (Confidence Score)", "मॉडेल ० ते १ दरम्यान एक संभाव्यता देते, जी टक्केवारीत रूपांतरित केली जाते — म्हणजे तुम्हाला लेबलसोबतच मॉडेल किती खात्रीशीर आहे हेही कळते."),
            ("६. Grad-CAM स्पष्टीकरण", "Grad-CAM शेवटच्या convolutional थरापर्यंत ग्रेडियंट्स मागे शोधून एक हीटमॅप तयार करते, जो दाखवतो की कोणत्या भागाने निर्णयावर सर्वाधिक प्रभाव टाकला. उष्ण रंग (लाल/पिवळा) = जास्त प्रभाव. यामुळे डॉक्टर AI च्या निर्णयाची स्वतःच्या डोळ्यांनी पडताळणी करू शकतात."),
            ("७. निकाल + जतन", "लेबल, विश्वासार्हता आणि Grad-CAM एकत्र दाखवले जातात. रुग्ण निवडलेला असल्यास, डॉक्टर नोंदी जोडून संपूर्ण निकाल त्या रुग्णाच्या कायम इतिहासात जतन करू शकतात."),
            ("८. PDF अहवाल", "एका क्लिकवर रुग्णाची माहिती, प्रतिमा, AI निकाल आणि सोप्या भाषेतील AI-निर्मित सारांश असलेला PDF अहवाल तयार होतो — रुग्णाला देण्यासाठी किंवा नोंदीत ठेवण्यासाठी तयार."),
        ],
        "limitations_title": "⚠️ या AI च्या प्रामाणिक मर्यादा",
        "limitations": [
            "हे फक्त एक बायनरी स्क्रीनिंग क्लासिफायर आहे (इसोफेजायटिस विरुद्ध सामान्य Z-रेषा) — हे कॅन्सरचा टप्पा किंवा तीव्रता सांगत नाही आणि प्रत्येक GI आजार ओळखत नाही.",
            "याची अचूकता पूर्णपणे प्रशिक्षण डेटावर अवलंबून आहे; वेगळ्या प्रकारच्या प्रतिमा, स्कोप किंवा रुग्ण गटांवर कामगिरी कमी होऊ शकते.",
            "उच्च विश्वासार्हता ही सांख्यिकीय मोजमाप आहे, वैद्यकीय निश्चितता नाही — विशेषतः ५०% च्या जवळ ती चुकीचीही असू शकते.",
            "हे बायोप्सी, हिस्टोपॅथोलॉजी किंवा गॅस्ट्रोएन्टेरोलॉजिस्टच्या क्लिनिकल निर्णयाची जागा घेऊ शकत नाही — हे फक्त स्क्रीनिंग/ट्रायएज सहाय्यक आहे.",
        ],
    },
}

# ---------------------------------------------------------------------------
# UNIQUE FEATURES — what makes this build different from a plain classifier
# ---------------------------------------------------------------------------
UNIQUE_FEATURES = {
    "en": {
        "title": "✨ What's unique in this project",
        "items": [
            "Automatic image deblurring before analysis — most demo classifiers skip this, but it directly improves prediction quality on real, imperfect endoscopy footage.",
            "Grad-CAM visual explainability overlay on every prediction, not just a bare label — builds clinical trust.",
            "Dual-mode AI assistant: works fully offline with a curated medical knowledge base, and optionally upgrades to live Claude-powered chat with an API key.",
            "True multilingual support: full UI + AI assistant in English, Hindi and Marathi, with the live-chat mode able to understand and reply in virtually any language typed.",
            "Built-in patient management with longitudinal diagnosis history, not just a single one-shot prediction.",
            "One-click, ready-to-share PDF report generation combining images, AI result and a plain-language summary.",
            "Everything (patient data, images, database) stays local on the machine running the app — nothing is uploaded to the cloud unless you explicitly enable live AI chat.",
            "Clear, repeated ethical disclaimers embedded directly into the workflow — designed for responsible, assistive use rather than replacing a doctor.",
        ],
    },
    "hi": {
        "title": "✨ इस प्रोजेक्ट में क्या खास (unique) है",
        "items": [
            "विश्लेषण से पहले खुद-ब-खुद इमेज डीब्लरिंग — ज़्यादातर डेमो क्लासिफ़ायर यह नहीं करते, लेकिन असली, थोड़ी अपूर्ण एंडोस्कोपी इमेज पर यह सीधे परिणाम की गुणवत्ता सुधारता है।",
            "हर परिणाम के साथ सिर्फ़ एक लेबल नहीं, बल्कि Grad-CAM विज़ुअल एक्सप्लेनेबिलिटी ओवरले — जिससे क्लिनिकल भरोसा बनता है।",
            "डुअल-मोड AI सहायक: बिना इंटरनेट के भी काम करता है (क्यूरेटेड मेडिकल नॉलेज-बेस से), और चाहें तो API key से लाइव Claude-पावर्ड चैट में अपग्रेड हो जाता है।",
            "सच्चा बहुभाषी समर्थन: पूरा UI + AI सहायक अंग्रेज़ी, हिंदी और मराठी में; लाइव-चैट मोड लगभग किसी भी टाइप की गई भाषा को समझकर उसी में जवाब दे सकता है।",
            "सिर्फ़ एक बार का परिणाम नहीं, बल्कि हर मरीज़ के लिए समय के साथ पूरी जांच-हिस्ट्री वाला बिल्ट-इन मरीज़ प्रबंधन।",
            "एक क्लिक में इमेज, AI परिणाम और आसान भाषा में सारांश वाली, तुरंत साझा करने लायक PDF रिपोर्ट।",
            "मरीज़ का डेटा, इमेज और डेटाबेस — सब कुछ उसी कंप्यूटर पर स्थानीय रहता है जहां ऐप चल रहा है; जब तक आप खुद लाइव AI चैट चालू न करें, कुछ भी क्लाउड पर नहीं जाता।",
            "पूरे वर्कफ़्लो में साफ़, बार-बार दिखने वाले नैतिक अस्वीकरण (disclaimers) — ताकि यह डॉक्टर की जगह नहीं, बल्कि उनकी ज़िम्मेदार सहायता के लिए बना है।",
        ],
    },
    "mr": {
        "title": "✨ या प्रकल्पात काय वेगळे (unique) आहे",
        "items": [
            "विश्लेषणापूर्वी आपोआप इमेज डीब्लरिंग — बहुतेक डेमो क्लासिफायर हे करत नाहीत, पण खऱ्या, थोड्या अपूर्ण एंडोस्कोपी फुटेजवर हे थेट निकालाची गुणवत्ता सुधारते.",
            "प्रत्येक निकालासोबत फक्त लेबल नाही, तर Grad-CAM व्हिज्युअल स्पष्टीकरण ओव्हरले — ज्यामुळे क्लिनिकल विश्वास निर्माण होतो.",
            "ड्युअल-मोड AI सहाय्यक: इंटरनेटशिवायही क्युरेटेड वैद्यकीय नॉलेज-बेसने काम करतो, आणि हवे असल्यास API key ने लाइव्ह Claude-आधारित चॅटमध्ये अपग्रेड होतो.",
            "खरा बहुभाषिक आधार: संपूर्ण UI + AI सहाय्यक इंग्रजी, हिंदी आणि मराठीत; लाइव्ह-चॅट मोड जवळपास कोणतीही टाइप केलेली भाषा समजून त्याच भाषेत उत्तर देऊ शकतो.",
            "फक्त एकदाचा निकाल नाही, तर प्रत्येक रुग्णासाठी कालांतराने संपूर्ण निदान-इतिहास असलेले अंगभूत रुग्ण व्यवस्थापन.",
            "एका क्लिकवर प्रतिमा, AI निकाल आणि सोप्या भाषेतील सारांश असलेला, लगेच शेअर करता येणारा PDF अहवाल.",
            "रुग्णाचा डेटा, प्रतिमा आणि डेटाबेस — सर्व काही अ‍ॅप चालणाऱ्या संगणकावरच स्थानिक राहते; तुम्ही स्वतः लाइव्ह AI चॅट सुरू केल्याशिवाय काहीही क्लाउडवर जात नाही.",
            "संपूर्ण वर्कफ्लोमध्ये स्पष्ट, वारंवार दिसणारे नैतिक disclaimers — हे डॉक्टरांची जागा घेण्यासाठी नाही तर त्यांना जबाबदारीने मदत करण्यासाठी बनवले आहे.",
        ],
    },
}

# ---------------------------------------------------------------------------
# DOCTOR CHALLENGES & SOLUTIONS — real-world problems doctors face with
# endoscopy/AI screening tools, and how this project addresses each one.
# ---------------------------------------------------------------------------
DOCTOR_CHALLENGES = {
    "en": {
        "title": "🩺 Problems doctors commonly face — and how this project solves them",
        "items": [
            ("Blurry / poor-quality endoscopy images",
             "Motion, mucus, and low light in real procedures (especially in low-resource clinics) blur images and hide subtle findings.",
             "An automatic deblurring/sharpening step runs before every prediction, and the app shows the original vs. deblurred image side by side so the doctor can see exactly what the model saw."),
            ("Not trusting an unexplained AI verdict",
             "A plain label like 'Esophagitis: 83%' with no reasoning is hard to trust in a clinical setting.",
             "Every prediction comes with a Grad-CAM heatmap showing exactly which regions of the image drove the decision, so the doctor can visually verify it against the actual tissue findings."),
            ("Too little time for paperwork",
             "Busy doctors, especially in high-volume or rural clinics, don't have time to maintain detailed paper records for every patient.",
             "Built-in patient management automatically keeps a running diagnosis history per patient, and a full PDF report is generated in one click."),
            ("Language barrier with patients and junior staff",
             "Many patients and even junior staff are more comfortable in Hindi or Marathi than in English medical terminology.",
             "The entire interface and AI assistant support English, Hindi and Marathi, and the live-chat mode can understand and respond in virtually any language the user types."),
            ("Explaining medical/technical terms on the spot",
             "Terms like 'Barrett's esophagus' or 'Grad-CAM' need quick, reliable explanations without leaving the workflow to search online.",
             "A built-in offline knowledge assistant instantly explains medical and technical terms — works with zero internet, and gets richer with an optional live AI upgrade."),
            ("Risk of over-trusting AI (false positives/negatives)",
             "Any AI model can be wrong, and overconfidence in automated tools is a genuine patient-safety risk.",
             "The confidence percentage is always shown transparently next to the label, and every result and chat response carries a clear disclaimer to confirm findings with a licensed physician (usually via biopsy)."),
            ("Unreliable or no internet in the clinic",
             "Many clinics, especially in rural areas, have limited or no internet access, which breaks cloud-only AI tools.",
             "Core detection (deblurring, model prediction, Grad-CAM) and the offline knowledge assistant work with zero internet connection. Live Claude chat is an optional add-on only, used when a key + internet are available."),
            ("Patient data privacy",
             "Uploading patient scans to third-party cloud services raises real privacy and compliance concerns.",
             "All patient records, images and the database are stored locally on the machine running the app — nothing leaves the device unless the optional live AI chat is explicitly turned on."),
            ("Explaining results to patients in simple terms",
             "Patients often don't understand clinical wording like 'esophagitis' or 'Z-line' at all.",
             "Each diagnosis label is shown with a plain-language translation, and the PDF report includes an AI-generated summary in everyday language that's easy to hand to the patient."),
        ],
    },
    "hi": {
        "title": "🩺 डॉक्टरों की आम समस्याएं — और यह प्रोजेक्ट उन्हें कैसे हल करता है",
        "items": [
            ("धुंधली / खराब गुणवत्ता की एंडोस्कोपी इमेज",
             "असली प्रक्रियाओं में (खासकर संसाधन-सीमित क्लीनिकों में) हलचल, बलगम और कम रोशनी की वजह से इमेज धुंधली आ जाती है और बारीक निशान छिप जाते हैं।",
             "हर जांच से पहले खुद-ब-खुद डीब्लरिंग/शार्पनिंग होती है, और ऐप मूल व डीब्लर की गई इमेज साथ-साथ दिखाता है ताकि डॉक्टर देख सकें कि मॉडल ने वास्तव में क्या देखा।"),
            ("बिना वजह वाले AI फैसले पर भरोसा न होना",
             "बिना किसी कारण के सिर्फ़ 'इसोफेजाइटिस: 83%' जैसा लेबल क्लिनिकल सेटिंग में भरोसा करना मुश्किल बनाता है।",
             "हर परिणाम के साथ Grad-CAM हीटमैप आता है, जो साफ़ दिखाता है कि इमेज के किस हिस्से ने फैसले को प्रभावित किया, ताकि डॉक्टर इसे असली टिशू निष्कर्षों से मिलाकर जांच सकें।"),
            ("कागज़ी काम के लिए बहुत कम समय",
             "व्यस्त डॉक्टरों, खासकर ज़्यादा मरीज़ों वाले या ग्रामीण क्लीनिकों में, हर मरीज़ का विस्तृत रिकॉर्ड रखने का समय नहीं होता।",
             "बिल्ट-इन मरीज़ प्रबंधन हर मरीज़ की जांच-हिस्ट्री खुद-ब-खुद रखता है, और एक क्लिक में पूरी PDF रिपोर्ट बन जाती है।"),
            ("मरीज़ों और जूनियर स्टाफ़ के साथ भाषा की दीवार",
             "कई मरीज़ और जूनियर स्टाफ़ भी अंग्रेज़ी मेडिकल शब्दावली से ज़्यादा हिंदी या मराठी में सहज होते हैं।",
             "पूरा इंटरफ़ेस और AI सहायक अंग्रेज़ी, हिंदी और मराठी सपोर्ट करता है, और लाइव-चैट मोड लगभग किसी भी टाइप की गई भाषा को समझकर जवाब दे सकता है।"),
            ("तुरंत मेडिकल/तकनीकी शब्द समझाना",
             "'बैरेट्स इसोफेगस' या 'Grad-CAM' जैसे शब्दों को काम बीच में छोड़े बिना, जल्दी और भरोसेमंद तरीके से समझाना ज़रूरी होता है।",
             "बिल्ट-इन ऑफ़लाइन नॉलेज असिस्टेंट तुरंत मेडिकल और तकनीकी शब्द समझाता है — बिना इंटरनेट के भी काम करता है, और चाहें तो लाइव AI अपग्रेड से और भी विस्तृत जवाब देता है।"),
            ("AI पर ज़रूरत से ज़्यादा भरोसा करने का खतरा",
             "कोई भी AI मॉडल गलत हो सकता है, और ऑटोमेटेड टूल पर ज़्यादा भरोसा मरीज़ की सुरक्षा के लिए असली जोखिम है।",
             "लेबल के साथ हमेशा विश्वास प्रतिशत साफ़ दिखाया जाता है, और हर परिणाम व चैट जवाब में यह स्पष्ट अस्वीकरण होता है कि निष्कर्षों की पुष्टि लाइसेंस-प्राप्त डॉक्टर (आमतौर पर बायोप्सी से) से करवाएं।"),
            ("क्लीनिक में इंटरनेट न होना या अस्थिर होना",
             "कई क्लीनिकों, खासकर ग्रामीण इलाकों में, इंटरनेट सीमित होता है या बिल्कुल नहीं होता, जिससे सिर्फ़-क्लाउड वाले AI टूल काम नहीं करते।",
             "मुख्य जांच (डीब्लरिंग, मॉडल परिणाम, Grad-CAM) और ऑफ़लाइन नॉलेज असिस्टेंट बिना इंटरनेट के भी काम करते हैं। लाइव Claude चैट सिर्फ़ एक वैकल्पिक ऐड-ऑन है, जो key और इंटरनेट होने पर इस्तेमाल होता है।"),
            ("मरीज़ के डेटा की गोपनीयता",
             "मरीज़ के स्कैन थर्ड-पार्टी क्लाउड सेवाओं पर अपलोड करने से गोपनीयता और अनुपालन (compliance) की असली चिंताएं होती हैं।",
             "सभी मरीज़ रिकॉर्ड, इमेज और डेटाबेस उसी कंप्यूटर पर स्थानीय रूप से सेव होते हैं जहां ऐप चल रहा है — जब तक आप खुद लाइव AI चैट चालू न करें, कुछ भी डिवाइस से बाहर नहीं जाता।"),
            ("मरीज़ों को परिणाम आसान भाषा में समझाना",
             "मरीज़ अक्सर 'इसोफेजाइटिस' या 'Z-लाइन' जैसे क्लिनिकल शब्द बिल्कुल नहीं समझते।",
             "हर निदान लेबल के साथ आसान भाषा में अनुवाद दिखाया जाता है, और PDF रिपोर्ट में रोज़मर्रा की भाषा में AI-जनित सारांश होता है जो मरीज़ को देना आसान होता है।"),
        ],
    },
    "mr": {
        "title": "🩺 डॉक्टरांना येणाऱ्या सामान्य अडचणी — आणि हा प्रकल्प त्या कशा सोडवतो",
        "items": [
            ("अस्पष्ट / कमी दर्जाच्या एंडोस्कोपी प्रतिमा",
             "प्रत्यक्ष प्रक्रियांमध्ये (विशेषतः मर्यादित साधने असलेल्या क्लिनिकमध्ये) हालचाल, चिकट स्राव आणि कमी प्रकाशामुळे प्रतिमा अस्पष्ट येतात आणि बारीक चिन्हे लपतात.",
             "प्रत्येक तपासणीपूर्वी आपोआप डीब्लरिंग/शार्पनिंग होते, आणि अ‍ॅप मूळ व स्पष्ट केलेली प्रतिमा एकत्र दाखवतो, जेणेकरून डॉक्टरांना मॉडेलने नेमके काय पाहिले ते कळते."),
            ("कारणाशिवाय AI निर्णयावर विश्वास नसणे",
             "कोणतेही कारण न देता फक्त 'इसोफेजायटिस: ८३%' असे लेबल क्लिनिकल परिस्थितीत विश्वास ठेवणे कठीण करते.",
             "प्रत्येक निकालासोबत Grad-CAM हीटमॅप येतो, जो स्पष्टपणे दाखवतो की प्रतिमेच्या कोणत्या भागाने निर्णयावर प्रभाव टाकला, जेणेकरून डॉक्टर हे प्रत्यक्ष उतींच्या निष्कर्षांशी जुळवून पाहू शकतात."),
            ("कागदपत्रांसाठी खूप कमी वेळ",
             "व्यस्त डॉक्टरांना, विशेषतः जास्त रुग्ण असलेल्या किंवा ग्रामीण क्लिनिकमध्ये, प्रत्येक रुग्णाची तपशीलवार नोंद ठेवायला वेळ नसतो.",
             "अंगभूत रुग्ण व्यवस्थापन प्रत्येक रुग्णाचा निदान-इतिहास आपोआप ठेवते, आणि एका क्लिकवर संपूर्ण PDF अहवाल तयार होतो."),
            ("रुग्ण आणि कनिष्ठ कर्मचाऱ्यांसोबत भाषेचा अडथळा",
             "अनेक रुग्ण आणि कनिष्ठ कर्मचारीसुद्धा इंग्रजी वैद्यकीय शब्दांपेक्षा हिंदी किंवा मराठीत जास्त सहज असतात.",
             "संपूर्ण इंटरफेस आणि AI सहाय्यक इंग्रजी, हिंदी आणि मराठीला आधार देतो, आणि लाइव्ह-चॅट मोड जवळपास कोणतीही टाइप केलेली भाषा समजून उत्तर देऊ शकतो."),
            ("वैद्यकीय/तांत्रिक शब्द लगेच समजावणे",
             "'बॅरेट्स इसोफॅगस' किंवा 'Grad-CAM' सारखे शब्द काम मध्येच न सोडता, पटकन आणि विश्वासार्हपणे समजावणे गरजेचे असते.",
             "अंगभूत ऑफलाइन नॉलेज सहाय्यक वैद्यकीय आणि तांत्रिक शब्द लगेच समजावतो — इंटरनेटशिवायही काम करतो, आणि हवे असल्यास लाइव्ह AI अपग्रेडने अधिक तपशीलवार उत्तर देतो."),
            ("AI वर गरजेपेक्षा जास्त विश्वास ठेवण्याचा धोका",
             "कोणतेही AI मॉडेल चुकू शकते, आणि स्वयंचलित साधनांवर अतिविश्वास ठेवणे रुग्णाच्या सुरक्षिततेसाठी खरा धोका आहे.",
             "लेबलसोबत नेहमी विश्वासार्हता टक्केवारी स्पष्टपणे दाखवली जाते, आणि प्रत्येक निकाल व चॅट उत्तरात हे स्पष्ट disclaimer असते की निष्कर्षांची खात्री परवानाधारक डॉक्टरांकडून (सहसा बायोप्सीद्वारे) करून घ्यावी."),
            ("क्लिनिकमध्ये इंटरनेट नसणे किंवा अस्थिर असणे",
             "अनेक क्लिनिकमध्ये, विशेषतः ग्रामीण भागात, इंटरनेट मर्यादित किंवा अजिबात नसते, ज्यामुळे फक्त-क्लाउडवर चालणारी AI साधने काम करत नाहीत.",
             "मुख्य तपासणी (डीब्लरिंग, मॉडेल निकाल, Grad-CAM) आणि ऑफलाइन नॉलेज सहाय्यक इंटरनेटशिवायही काम करतात. लाइव्ह Claude चॅट हे फक्त एक पर्यायी अ‍ॅड-ऑन आहे, जे key आणि इंटरनेट उपलब्ध असल्यासच वापरले जाते."),
            ("रुग्णाच्या डेटाची गोपनीयता",
             "रुग्णाचे स्कॅन थर्ड-पार्टी क्लाउड सेवांवर अपलोड केल्याने गोपनीयता आणि अनुपालनाच्या खऱ्या चिंता निर्माण होतात.",
             "सर्व रुग्ण नोंदी, प्रतिमा आणि डेटाबेस अ‍ॅप चालणाऱ्या संगणकावरच स्थानिक पातळीवर साठवले जातात — तुम्ही स्वतः लाइव्ह AI चॅट सुरू केल्याशिवाय काहीही डिव्हाइसबाहेर जात नाही."),
            ("रुग्णांना निकाल सोप्या भाषेत समजावणे",
             "रुग्णांना बऱ्याचदा 'इसोफेजायटिस' किंवा 'Z-रेषा' सारखे क्लिनिकल शब्द अजिबात समजत नाहीत.",
             "प्रत्येक निदान लेबलसोबत सोप्या भाषेतील भाषांतर दाखवले जाते, आणि PDF अहवालात रोजच्या भाषेतील AI-निर्मित सारांश असतो जो रुग्णाला देणे सोपे असते."),
        ],
    },
}
