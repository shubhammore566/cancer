"""
ai_assistant.py
A lightweight, offline knowledge-based "AI Doctor Assistant" specialised in
esophageal cancer / esophagitis education. Works with no external API key.

MULTILINGUAL: the offline assistant can match a question typed in English,
Hindi (हिंदी) or Marathi (मराठी) — including Hinglish / romanised Hindi —
to the right topic, and replies in whichever language it detected (or the
app's currently selected language if detection is unclear).

If the user supplies an Anthropic API key (via the sidebar), the assistant
automatically upgrades to a live Claude-powered chat which can understand
and reply fluently in literally any language the user types in.
"""
import re

# ---------------------------------------------------------------------------
# KNOWLEDGE BASE — canonical topic keys (English) -> answer text per language.
# Keep this in sync with translations.py topic ids used for matching.
# ---------------------------------------------------------------------------
KNOWLEDGE_BASE = {
    "en": {
        "what is esophageal cancer": (
            "Esophageal cancer begins in the cells lining the esophagus, the tube that "
            "carries food from the throat to the stomach. The two main types are "
            "squamous cell carcinoma (usually in the upper/middle esophagus) and "
            "adenocarcinoma (usually in the lower esophagus, often linked to Barrett's "
            "esophagus)."
        ),
        "what is esophagitis": (
            "Esophagitis is inflammation of the esophageal lining. It can be caused by "
            "acid reflux (GERD), infections, medications, allergies (eosinophilic "
            "esophagitis), or irritants. Chronic, untreated esophagitis — especially "
            "from long-term acid reflux — can lead to Barrett's esophagus, which "
            "carries an increased risk of esophageal adenocarcinoma over time."
        ),
        "symptoms": (
            "Common warning symptoms include: difficulty or painful swallowing "
            "(dysphagia/odynophagia), unintentional weight loss, chest pain or "
            "burning behind the breastbone, chronic heartburn/acid reflux, "
            "hoarseness or chronic cough, and vomiting or regurgitating food. "
            "Persistent or worsening symptoms should always be evaluated by a doctor."
        ),
        "risk factors": (
            "Key risk factors include long-standing GERD/acid reflux, Barrett's "
            "esophagus, smoking, heavy alcohol use, obesity, a diet low in fruits and "
            "vegetables, very hot beverages, and certain rare conditions like "
            "achalasia or tylosis. Squamous cell carcinoma is additionally linked to "
            "smoking and alcohol, while adenocarcinoma is more linked to reflux and "
            "obesity."
        ),
        "prevention": (
            "While not all cases are preventable, risk can be lowered by managing "
            "acid reflux, avoiding tobacco and limiting alcohol, maintaining a "
            "healthy weight, eating a diet rich in fruits and vegetables, and getting "
            "regular check-ups if you have chronic GERD or Barrett's esophagus, since "
            "early detection greatly improves outcomes."
        ),
        "treatment": (
            "Treatment depends on the stage and type of cancer, and typically "
            "involves a combination of endoscopic therapy (for very early lesions), "
            "surgery, chemotherapy, radiation therapy, targeted therapy, or "
            "immunotherapy. A multidisciplinary oncology team decides the best plan "
            "for each patient — this assistant cannot recommend a specific treatment."
        ),
        "diet": (
            "General reflux-friendly habits include eating smaller meals, avoiding "
            "trigger foods (spicy, fatty, acidic, caffeine, alcohol), not lying down "
            "right after eating, and maintaining a healthy weight. A registered "
            "dietitian or gastroenterologist can give personalised dietary guidance."
        ),
        "when to see a doctor": (
            "See a doctor promptly if you have trouble swallowing, unexplained "
            "weight loss, persistent heartburn (more than twice a week), chest pain, "
            "vomiting blood, or black/tarry stools. Early evaluation — often with an "
            "upper endoscopy — leads to much better outcomes."
        ),
        "barrett": (
            "Barrett's esophagus is a condition where the normal lining of the lower "
            "esophagus changes to resemble intestinal lining, usually due to chronic "
            "acid reflux. It is a precursor condition that modestly raises the risk "
            "of esophageal adenocarcinoma, so it is usually monitored with periodic "
            "endoscopic surveillance."
        ),
        "grad-cam": (
            "The Grad-CAM (Gradient-weighted Class Activation Mapping) overlay "
            "highlights the image regions that most influenced the AI model's "
            "prediction. Warmer colors (red/yellow) indicate regions the model "
            "weighted most heavily. It's a visual aid for interpretability, not a "
            "clinical finding by itself."
        ),
        "how does this model work": (
            "This tool uses a convolutional neural network (based on an EfficientNet "
            "architecture) trained on endoscopic images to classify the esophageal "
            "lining as either showing signs of esophagitis or appearing as a normal "
            "Z-line. The image is first deblurred/sharpened, then resized and "
            "normalized, run through the model to get a confidence score, and a "
            "Grad-CAM heatmap is generated to show which regions influenced the "
            "result. Check the 'How the AI Works' tab for the full step-by-step "
            "pipeline. It is a screening aid, not a diagnostic device."
        ),
    },
    "hi": {
        "what is esophageal cancer": (
            "इसोफेजियल कैंसर उस ट्यूब (इसोफेगस/भोजन-नली) की कोशिकाओं में शुरू होता है जो "
            "गले से पेट तक भोजन पहुंचाती है। इसके दो मुख्य प्रकार हैं — स्क्वैमस सेल "
            "कार्सिनोमा (आमतौर पर ऊपरी/मध्य हिस्से में) और एडेनोकार्सिनोमा (आमतौर पर "
            "निचले हिस्से में, अक्सर बैरेट्स इसोफेगस से जुड़ा हुआ)।"
        ),
        "what is esophagitis": (
            "इसोफेजाइटिस भोजन-नली की परत में होने वाली सूजन है। इसकी वजह एसिड रिफ्लक्स "
            "(GERD), संक्रमण, दवाएं, एलर्जी (ईओसिनोफिलिक इसोफेजाइटिस), या जलन पैदा करने "
            "वाली चीज़ें हो सकती हैं। लंबे समय तक इलाज न किया गया इसोफेजाइटिस — खासकर "
            "लगातार एसिड रिफ्लक्स से — बैरेट्स इसोफेगस बन सकता है, जिससे भविष्य में "
            "एडेनोकार्सिनोमा का खतरा बढ़ जाता है।"
        ),
        "symptoms": (
            "सामान्य चेतावनी संकेतों में शामिल हैं: निगलने में कठिनाई या दर्द (dysphagia), "
            "बिना वजह वज़न कम होना, छाती में दर्द या जलन, लगातार सीने में जलन (heartburn), "
            "आवाज़ बैठना या पुरानी खांसी, और भोजन उल्टी होना या वापस आना। लगातार बने "
            "रहने वाले या बढ़ते लक्षणों की हमेशा डॉक्टर से जांच करवानी चाहिए।"
        ),
        "risk factors": (
            "मुख्य जोखिम कारकों में शामिल हैं: लंबे समय से GERD/एसिड रिफ्लक्स, बैरेट्स "
            "इसोफेगस, धूम्रपान, अधिक शराब पीना, मोटापा, फल-सब्ज़ियों की कमी वाला आहार, "
            "बहुत गर्म पेय पदार्थ, और achalasia या tylosis जैसी दुर्लभ स्थितियां। "
            "स्क्वैमस सेल कार्सिनोमा धूम्रपान और शराब से ज़्यादा जुड़ा है, जबकि "
            "एडेनोकार्सिनोमा रिफ्लक्स और मोटापे से ज़्यादा जुड़ा है।"
        ),
        "prevention": (
            "हर मामला रोका नहीं जा सकता, लेकिन खतरा कम किया जा सकता है — एसिड रिफ्लक्स "
            "को नियंत्रित रखकर, तंबाकू से बचकर और शराब सीमित करके, स्वस्थ वज़न बनाए रखकर, "
            "फल-सब्ज़ी युक्त आहार लेकर, और अगर आपको पुराना GERD या बैरेट्स इसोफेगस है तो "
            "नियमित जांच करवाकर — क्योंकि जल्दी पता चलने पर परिणाम काफ़ी बेहतर होते हैं।"
        ),
        "treatment": (
            "इलाज कैंसर की स्टेज और प्रकार पर निर्भर करता है, और आमतौर पर इसमें "
            "एंडोस्कोपिक थेरेपी (बहुत शुरुआती स्थिति के लिए), सर्जरी, कीमोथेरेपी, "
            "रेडिएशन थेरेपी, टार्गेटेड थेरेपी, या इम्यूनोथेरेपी का मिश्रण शामिल होता है। "
            "हर मरीज़ के लिए सबसे अच्छा प्लान एक मल्टी-डिसिप्लिनरी ऑन्कोलॉजी टीम तय करती "
            "है — यह असिस्टेंट कोई खास इलाज सुझा नहीं सकता।"
        ),
        "diet": (
            "रिफ्लक्स को कम करने वाली सामान्य आदतों में शामिल हैं: छोटे-छोटे भोजन करना, "
            "ट्रिगर फूड्स (तीखा, तला-भुना, खट्टा, कैफीन, शराब) से बचना, खाने के तुरंत "
            "बाद लेटना नहीं, और स्वस्थ वज़न बनाए रखना। व्यक्तिगत आहार सलाह के लिए किसी "
            "रजिस्टर्ड डाइटिशियन या गैस्ट्रोएंटरोलॉजिस्ट से मिलें।"
        ),
        "when to see a doctor": (
            "अगर आपको निगलने में परेशानी, बिना वजह वज़न कम होना, लगातार सीने में जलन "
            "(हफ़्ते में दो बार से ज़्यादा), छाती में दर्द, खून की उल्टी, या काला/चिपचिपा "
            "मल हो, तो तुरंत डॉक्टर से मिलें। जल्दी जांच — अक्सर ऊपरी एंडोस्कोपी से — "
            "परिणाम बहुत बेहतर बनाती है।"
        ),
        "barrett": (
            "बैरेट्स इसोफेगस एक ऐसी स्थिति है जिसमें निचली भोजन-नली की सामान्य परत बदलकर "
            "आंत की परत जैसी दिखने लगती है, आमतौर पर लंबे समय तक एसिड रिफ्लक्स की वजह से। "
            "यह एक शुरुआती स्थिति है जो इसोफेजियल एडेनोकार्सिनोमा का खतरा थोड़ा बढ़ा देती "
            "है, इसलिए इसकी समय-समय पर एंडोस्कोपिक निगरानी की जाती है।"
        ),
        "grad-cam": (
            "Grad-CAM (Gradient-weighted Class Activation Mapping) ओवरले उन हिस्सों को "
            "हाइलाइट करता है जिन्होंने AI मॉडल के फैसले को सबसे ज़्यादा प्रभावित किया। "
            "गर्म रंग (लाल/पीला) उन हिस्सों को दिखाते हैं जिन्हें मॉडल ने सबसे ज़्यादा "
            "महत्व दिया। यह समझने में मदद करने वाला एक विज़ुअल टूल है, अपने आप में कोई "
            "क्लिनिकल निष्कर्ष नहीं।"
        ),
        "how does this model work": (
            "यह टूल एक कन्वोल्यूशनल न्यूरल नेटवर्क (EfficientNet आर्किटेक्चर पर आधारित) "
            "इस्तेमाल करता है, जो एंडोस्कोपिक इमेज को इसोफेजाइटिस या सामान्य Z-लाइन में "
            "वर्गीकृत करने के लिए ट्रेन किया गया है। इमेज को पहले डीब्लर/शार्प किया जाता "
            "है, फिर रीसाइज़ और नॉर्मलाइज़ किया जाता है, मॉडल से विश्वास स्तर निकाला "
            "जाता है, और Grad-CAM हीटमैप बनाया जाता है जो दिखाता है कि किन हिस्सों ने "
            "परिणाम को प्रभावित किया। पूरी प्रक्रिया के लिए 'AI कैसे काम करता है' टैब "
            "देखें। यह एक स्क्रीनिंग सहायक है, कोई निदान डिवाइस नहीं।"
        ),
    },
    "mr": {
        "what is esophageal cancer": (
            "इसोफेजियल कॅन्सर त्या नळीच्या (अन्ननलिका) पेशींमध्ये सुरू होतो जी घशापासून "
            "पोटापर्यंत अन्न घेऊन जाते. याचे दोन मुख्य प्रकार आहेत — स्क्वॅमस सेल "
            "कार्सिनोमा (सहसा वरच्या/मधल्या भागात) आणि अ‍ॅडेनोकार्सिनोमा (सहसा खालच्या "
            "भागात, अनेकदा बॅरेट्स इसोफॅगसशी संबंधित)."
        ),
        "what is esophagitis": (
            "इसोफेजायटिस म्हणजे अन्ननलिकेच्या आतील थराला येणारी सूज. याचे कारण अ‍ॅसिड "
            "रिफ्लक्स (GERD), संसर्ग, औषधे, अ‍ॅलर्जी (इओसिनोफिलिक इसोफेजायटिस), किंवा "
            "त्रासदायक घटक असू शकतात. दीर्घकाळ उपचार न केलेला इसोफेजायटिस — विशेषतः "
            "सतत अ‍ॅसिड रिफ्लक्समुळे — बॅरेट्स इसोफॅगस होऊ शकतो, ज्यामुळे पुढे "
            "अ‍ॅडेनोकार्सिनोमाचा धोका वाढतो."
        ),
        "symptoms": (
            "सामान्य इशारा देणाऱ्या लक्षणांमध्ये समाविष्ट आहे: गिळताना त्रास किंवा वेदना "
            "(dysphagia), अनपेक्षित वजन कमी होणे, छातीत दुखणे किंवा जळजळ, सतत छातीत "
            "जळजळ (heartburn), आवाज बसणे किंवा जुनाट खोकला, आणि उलटी होणे किंवा अन्न "
            "परत येणे. सतत राहणारी किंवा वाढणारी लक्षणे नेहमी डॉक्टरांकडून तपासून घ्यावीत."
        ),
        "risk factors": (
            "मुख्य जोखीम घटकांमध्ये समाविष्ट आहे: दीर्घकालीन GERD/अ‍ॅसिड रिफ्लक्स, बॅरेट्स "
            "इसोफॅगस, धूम्रपान, जास्त मद्यपान, लठ्ठपणा, फळे-भाज्यांची कमतरता असलेला आहार, "
            "खूप गरम पेये, आणि achalasia किंवा tylosis सारख्या दुर्मिळ स्थिती. स्क्वॅमस "
            "सेल कार्सिनोमा धूम्रपान आणि मद्यपानाशी जास्त संबंधित आहे, तर अ‍ॅडेनोकार्सिनोमा "
            "रिफ्लक्स आणि लठ्ठपणाशी जास्त संबंधित आहे."
        ),
        "prevention": (
            "प्रत्येक केस टाळता येत नाही, पण धोका कमी करता येतो — अ‍ॅसिड रिफ्लक्स "
            "नियंत्रणात ठेवून, तंबाखू टाळून आणि मद्यपान मर्यादित करून, निरोगी वजन राखून, "
            "फळे-भाज्यायुक्त आहार घेऊन, आणि दीर्घकालीन GERD किंवा बॅरेट्स इसोफॅगस असल्यास "
            "नियमित तपासणी करून — कारण लवकर निदान झाल्यास परिणाम खूप चांगले होतात."
        ),
        "treatment": (
            "उपचार कॅन्सरचा टप्पा आणि प्रकारावर अवलंबून असतो, आणि सहसा यात एंडोस्कोपिक "
            "थेरपी (अगदी सुरुवातीच्या जखमांसाठी), शस्त्रक्रिया, केमोथेरपी, रेडिएशन थेरपी, "
            "टार्गेटेड थेरपी, किंवा इम्युनोथेरपीचे मिश्रण असते. प्रत्येक रुग्णासाठी सर्वोत्तम "
            "योजना एक बहुविद्याशाखीय ऑन्कोलॉजी टीम ठरवते — हा सहाय्यक विशिष्ट उपचार सुचवू "
            "शकत नाही."
        ),
        "diet": (
            "रिफ्लक्स कमी करणाऱ्या सामान्य सवयींमध्ये समाविष्ट आहे: लहान-लहान जेवण घेणे, "
            "ट्रिगर पदार्थ (तिखट, तेलकट, आंबट, कॅफीन, मद्य) टाळणे, जेवणानंतर लगेच न "
            "झोपणे, आणि निरोगी वजन राखणे. वैयक्तिक आहार सल्ल्यासाठी नोंदणीकृत आहारतज्ज्ञ "
            "किंवा गॅस्ट्रोएन्टेरोलॉजिस्टला भेटा."
        ),
        "when to see a doctor": (
            "जर तुम्हाला गिळताना त्रास, अनपेक्षित वजन कमी होणे, सतत छातीत जळजळ "
            "(आठवड्यातून दोनदा जास्त), छातीत दुखणे, रक्ताची उलटी, किंवा काळी/चिकट "
            "विष्ठा होत असेल, तर लगेच डॉक्टरांना भेटा. लवकर तपासणी — सहसा अप्पर "
            "एंडोस्कोपीद्वारे — खूप चांगले परिणाम देते."
        ),
        "barrett": (
            "बॅरेट्स इसोफॅगस ही अशी स्थिती आहे ज्यात खालच्या अन्ननलिकेचा सामान्य थर बदलून "
            "आतड्याच्या थरासारखा दिसू लागतो, सहसा दीर्घकालीन अ‍ॅसिड रिफ्लक्समुळे. ही एक "
            "पूर्वस्थिती आहे जी इसोफेजियल अ‍ॅडेनोकार्सिनोमाचा धोका थोडा वाढवते, त्यामुळे "
            "हिचे वेळोवेळी एंडोस्कोपिक निरीक्षण केले जाते."
        ),
        "grad-cam": (
            "Grad-CAM (Gradient-weighted Class Activation Mapping) ओव्हरले त्या भागांना "
            "हायलाइट करतो ज्यांनी AI मॉडेलच्या निर्णयावर सर्वाधिक प्रभाव टाकला. उष्ण रंग "
            "(लाल/पिवळा) ते भाग दाखवतात ज्यांना मॉडेलने सर्वाधिक महत्त्व दिले. हे समजून "
            "घेण्यासाठी मदत करणारे एक व्हिज्युअल साधन आहे, स्वतःहून कोणताही क्लिनिकल "
            "निष्कर्ष नाही."
        ),
        "how does this model work": (
            "हे साधन एक कन्व्होल्यूशनल न्यूरल नेटवर्क (EfficientNet आर्किटेक्चरवर आधारित) "
            "वापरते, जे एंडोस्कोपिक प्रतिमेला इसोफेजायटिस किंवा सामान्य Z-रेषा म्हणून "
            "वर्गीकृत करण्यासाठी प्रशिक्षित आहे. प्रतिमा आधी डीब्लर/शार्प केली जाते, मग "
            "रीसाइझ आणि नॉर्मलाइझ केली जाते, मॉडेलमधून विश्वासार्हता काढली जाते, आणि "
            "Grad-CAM हीटमॅप तयार होतो जो दाखवतो की कोणत्या भागांनी निकालावर प्रभाव "
            "टाकला. संपूर्ण प्रक्रियेसाठी 'AI कसे काम करते' टॅब पाहा. हे एक स्क्रीनिंग "
            "सहाय्यक आहे, निदान उपकरण नाही."
        ),
    },
}

GREETINGS = {
    "en": ["hi", "hello", "hey", "helo"],
    "hi": ["namaste", "namaskar", "नमस्ते", "नमस्कार", "hii"],
    "mr": ["namaskar", "नमस्कार"],
}

GREETING_REPLY = {
    "en": "Hello! I'm your AI health assistant for this esophageal screening tool. Ask me about symptoms, risk factors, Barrett's esophagus, prevention, or what your scan result means.",
    "hi": "नमस्ते! मैं इस इसोफेजियल स्क्रीनिंग टूल का AI हेल्थ असिस्टेंट हूं। मुझसे लक्षण, जोखिम कारक, बैरेट्स इसोफेगस, बचाव, या अपने स्कैन परिणाम के बारे में पूछें।",
    "mr": "नमस्कार! मी या इसोफेजियल स्क्रीनिंग साधनाचा AI आरोग्य सहाय्यक आहे. मला लक्षणे, जोखीम घटक, बॅरेट्स इसोफॅगस, प्रतिबंध, किंवा तुमच्या स्कॅन निकालाबद्दल विचारा.",
}

DISCLAIMER = {
    "en": (
        "⚠️ I'm an educational AI assistant, not a licensed physician. I can explain "
        "general information about esophageal conditions, but any diagnosis or "
        "treatment decision must come from a qualified doctor after a proper clinical "
        "evaluation."
    ),
    "hi": (
        "⚠️ मैं एक शैक्षणिक AI सहायक हूं, कोई लाइसेंस-प्राप्त डॉक्टर नहीं। मैं इसोफेजियल "
        "स्थितियों के बारे में सामान्य जानकारी समझा सकता हूं, लेकिन कोई भी निदान या "
        "इलाज का फैसला सही क्लिनिकल जांच के बाद एक योग्य डॉक्टर से ही आना चाहिए।"
    ),
    "mr": (
        "⚠️ मी एक शैक्षणिक AI सहाय्यक आहे, परवानाधारक डॉक्टर नाही. मी इसोफेजियल "
        "स्थितींबद्दल सामान्य माहिती समजावू शकतो, पण कोणताही निदान किंवा उपचाराचा "
        "निर्णय योग्य क्लिनिकल तपासणीनंतर एका पात्र डॉक्टरांकडूनच यायला हवा."
    ),
}

NO_MATCH = {
    "en": "I don't have specific information on that yet. I can help with: symptoms, risk factors, prevention, Barrett's esophagus, esophagitis, treatment overview, diet tips, Grad-CAM explanation, or your latest result.",
    "hi": "मुझे इस बारे में अभी विशेष जानकारी नहीं है। मैं इनमें मदद कर सकता हूं: लक्षण, जोखिम कारक, बचाव, बैरेट्स इसोफेगस, इसोफेजाइटिस, इलाज का सार, आहार सुझाव, Grad-CAM की व्याख्या, या आपका नवीनतम परिणाम।",
    "mr": "याबद्दल माझ्याकडे सध्या विशिष्ट माहिती नाही. मी यात मदत करू शकतो: लक्षणे, जोखीम घटक, प्रतिबंध, बॅरेट्स इसोफॅगस, इसोफेजायटिस, उपचारांचा आढावा, आहार सूचना, Grad-CAM स्पष्टीकरण, किंवा तुमचा नवीनतम निकाल.",
}

EMPTY_PROMPT = {
    "en": "Please type a question about esophageal health, symptoms, or your results.",
    "hi": "कृपया इसोफेजियल स्वास्थ्य, लक्षणों या अपने परिणामों के बारे में कोई सवाल टाइप करें।",
    "mr": "कृपया इसोफेजियल आरोग्य, लक्षणे किंवा तुमच्या निकालांबद्दल एखादा प्रश्न टाइप करा.",
}

NO_SAVED_RESULT = {
    "en": "I don't see a saved diagnosis yet — please run a detection first in the Detect tab.",
    "hi": "मुझे अभी कोई सेव किया गया परिणाम नहीं दिख रहा — कृपया पहले 'अपलोड और जांच' टैब में एक जांच करें।",
    "mr": "मला अजून कोणताही जतन केलेला निकाल दिसत नाही — कृपया आधी 'अपलोड आणि तपासणी' टॅबमध्ये एक तपासणी करा.",
}

RESULT_TEMPLATES = {
    "en": {
        "Esophagitis": (
            "Your most recent scan was flagged as **{pred}** with {conf:.1f}% model "
            "confidence. This means the AI detected visual patterns consistent with "
            "inflammation of the esophageal lining. Please discuss this result with a "
            "gastroenterologist for confirmation (usually via biopsy) and next steps."
        ),
        "Normal Z-line": (
            "Your most recent scan was classified as **{pred}** with {conf:.1f}% model "
            "confidence, meaning no abnormal pattern was detected by the AI. Continue "
            "routine check-ups, especially if you have reflux symptoms or other risk "
            "factors."
        ),
    },
    "hi": {
        "Esophagitis": (
            "आपके नवीनतम स्कैन को **{pred}** के रूप में चिह्नित किया गया, जिसमें मॉडल "
            "का विश्वास स्तर {conf:.1f}% है। इसका मतलब है कि AI ने भोजन-नली की परत में "
            "सूजन जैसे पैटर्न देखे हैं। कृपया इसकी पुष्टि (आमतौर पर बायोप्सी से) और अगले "
            "कदमों के लिए किसी गैस्ट्रोएंटरोलॉजिस्ट से चर्चा करें।"
        ),
        "Normal Z-line": (
            "आपके नवीनतम स्कैन को **{pred}** के रूप में वर्गीकृत किया गया, जिसमें मॉडल "
            "का विश्वास स्तर {conf:.1f}% है, यानी AI को कोई असामान्य पैटर्न नहीं मिला। "
            "फिर भी नियमित जांच जारी रखें, खासकर अगर आपको रिफ्लक्स के लक्षण या अन्य "
            "जोखिम कारक हैं।"
        ),
    },
    "mr": {
        "Esophagitis": (
            "तुमच्या नवीनतम स्कॅनला **{pred}** म्हणून चिन्हांकित केले गेले, ज्यात "
            "मॉडेलची विश्वासार्हता {conf:.1f}% आहे. याचा अर्थ AI ला अन्ननलिकेच्या "
            "आतील थरात सूज दर्शवणारे नमुने आढळले. कृपया याची खात्री (सहसा बायोप्सीद्वारे) "
            "आणि पुढील पावलांसाठी गॅस्ट्रोएन्टेरोलॉजिस्टशी चर्चा करा."
        ),
        "Normal Z-line": (
            "तुमच्या नवीनतम स्कॅनचे **{pred}** असे वर्गीकरण झाले, ज्यात मॉडेलची "
            "विश्वासार्हता {conf:.1f}% आहे, म्हणजे AI ला कोणताही असामान्य नमुना आढळला "
            "नाही. तरीही नियमित तपासणी सुरू ठेवा, विशेषतः जर तुम्हाला रिफ्लक्सची लक्षणे "
            "किंवा इतर जोखीम घटक असतील."
        ),
    },
}

MY_RESULT_TRIGGERS = [
    "my result", "my diagnosis", "my report", "my scan",
    "मेरा परिणाम", "मेरा निदान", "मेरी रिपोर्ट", "मेरा स्कैन",
    "माझा निकाल", "माझे निदान", "माझा अहवाल", "माझा स्कॅन",
]

# ---------------------------------------------------------------------------
# Keyword sets per topic, per language (used for matching AND for guessing
# which language the user is typing in).
# ---------------------------------------------------------------------------
_TOPIC_KEYWORDS = {
    "what is esophageal cancer": {
        "en": ["esophageal", "cancer", "oesophageal"],
        "hi": ["इसोफेजियल", "कैंसर", "कैंसर क्या"],
        "mr": ["इसोफेजियल", "कॅन्सर", "कर्करोग"],
    },
    "what is esophagitis": {
        "en": ["esophagitis", "oesophagitis"],
        "hi": ["इसोफेजाइटिस", "सूजन"],
        "mr": ["इसोफेजायटिस", "सूज", "दाह"],
    },
    "symptoms": {
        "en": ["symptom", "symptoms", "sign", "signs", "warning"],
        "hi": ["लक्षण", "संकेत", "symptom", "sanket", "lakshan"],
        "mr": ["लक्षण", "लक्षणे", "symptom", "lakshan"],
    },
    "risk factors": {
        "en": ["risk factor", "risk factors", "risks"],
        "hi": ["जोखिम", "risk", "khatra", "khatare"],
        "mr": ["जोखीम", "धोका", "risk"],
    },
    "prevention": {
        "en": ["prevent", "prevention", "avoid"],
        "hi": ["बचाव", "रोकथाम", "prevent", "bachav"],
        "mr": ["प्रतिबंध", "टाळणे", "prevent"],
    },
    "treatment": {
        "en": ["treatment", "cure", "therapy"],
        "hi": ["इलाज", "उपचार", "treatment"],
        "mr": ["उपचार", "इलाज", "treatment"],
    },
    "diet": {
        "en": ["diet", "food", "eat"],
        "hi": ["आहार", "खाना", "diet", "khana"],
        "mr": ["आहार", "जेवण", "diet"],
    },
    "when to see a doctor": {
        "en": ["see a doctor", "see doctor", "when should i"],
        "hi": ["डॉक्टर से कब", "डॉक्टर को कब", "doctor se kab"],
        "mr": ["डॉक्टरांना कधी", "डॉक्टरकडे कधी"],
    },
    "barrett": {
        "en": ["barrett"],
        "hi": ["बैरेट्स", "barrett"],
        "mr": ["बॅरेट्स", "barrett"],
    },
    "grad-cam": {
        "en": ["grad-cam", "gradcam", "heatmap", "attention map"],
        "hi": ["ग्रेड-कैम", "हीटमैप", "gradcam"],
        "mr": ["ग्रॅड-कॅम", "हीटमॅप", "gradcam"],
    },
    "how does this model work": {
        "en": ["how does this model work", "how does the ai work", "how does it detect",
               "how does it work", "how it works", "pipeline", "algorithm", "detect"],
        "hi": ["यह कैसे काम करता है", "मॉडल कैसे काम", "कैसे पता चलता है", "kaise kaam",
               "kaise detect", "ai kaise", "kaam karta", "detect kaise", "kaise pata"],
        "mr": ["हे कसे काम करते", "मॉडेल कसे काम", "कसे ओळखते", "kase kaam", "ai kase",
               "kaam karte", "olakhte kase"],
    },
}

_STOPWORDS_EN = {"what", "is", "are", "the", "of", "a", "an", "to", "for", "and", "does", "do", "my"}


def _script_lang(text: str) -> str:
    """Guess language purely from Unicode script. Devanagari covers both
    Hindi and Marathi, so this only narrows to 'devanagari' vs 'latin'."""
    if re.search(r"[\u0900-\u097F]", text):
        return "devanagari"
    return "latin"


def detect_language(text: str, ui_lang: str = "en") -> str:
    """
    Best-effort language detection for the offline assistant:
    1. If the text contains Devanagari script, prefer the UI-selected
       language if it's Hindi or Marathi (since we can't tell them apart
       from script alone); otherwise default to Hindi.
    2. If it's Latin script, check for romanised Hindi/Marathi keyword hits;
       otherwise fall back to the UI-selected language, then English.
    """
    text_l = text.lower()
    script = _script_lang(text)
    if script == "devanagari":
        return ui_lang if ui_lang in ("hi", "mr") else "hi"

    # Romanised Hindi/Marathi hint words (very common chat words)
    hinglish_hints = ["kya", "hai", "kaise", "kyun", "mujhe", "mera", "meri", "bhi", "nahi", "karu", "kro"]
    marathi_hints = ["mala", "tumhi", "kai", "kase", "mi", "ahe", "nahi", "karto", "kara"]
    if any(w in text_l.split() for w in hinglish_hints):
        return "hi"
    if any(w in text_l.split() for w in marathi_hints):
        return "mr"
    return ui_lang if ui_lang in ("en", "hi", "mr") else "en"


def _match_topic(user_text: str):
    """Match the user's text against topic keywords across ALL languages at
    once (so Hindi keywords, Marathi keywords and English keywords can all
    trigger the same topic id, regardless of which language the UI is set to).
    """
    text = user_text.lower()

    priority_overrides = [
        ("grad-cam", "grad-cam"), ("gradcam", "grad-cam"), ("ग्रेड-कैम", "grad-cam"), ("ग्रॅड-कॅम", "grad-cam"),
        ("barrett", "barrett"), ("बैरेट्स", "barrett"), ("बॅरेट्स", "barrett"),
        ("symptom", "symptoms"), ("लक्षण", "symptoms"),
        ("risk factor", "risk factors"), ("जोखिम", "risk factors"), ("जोखीम", "risk factors"),
        ("prevent", "prevention"), ("बचाव", "prevention"), ("रोकथाम", "prevention"), ("प्रतिबंध", "prevention"),
        ("treatment", "treatment"), ("इलाज", "treatment"), ("उपचार", "treatment"),
        ("how does", "how does this model work"), ("how it works", "how does this model work"),
        ("kaise kaam", "how does this model work"), ("kase kaam", "how does this model work"),
        ("kaam karta", "how does this model work"), ("kaam karte", "how does this model work"),
        ("कैसे काम", "how does this model work"), ("कसे काम", "how does this model work"),
        ("kaise detect", "how does this model work"), ("kase olakhte", "how does this model work"),
        ("detect kaise", "how does this model work"), ("kaise pata", "how does this model work"),
        ("detect karta", "how does this model work"), ("kaam karta hai detect", "how does this model work"),
    ]
    for trigger, topic in priority_overrides:
        if trigger in text:
            return topic

    scores = {}
    for topic, lang_kws in _TOPIC_KEYWORDS.items():
        weight = 0
        for lang, kws in lang_kws.items():
            for kw in kws:
                if kw.lower() in text:
                    weight += 1
        if weight:
            scores[topic] = weight

    if not scores:
        return None
    return max(scores, key=scores.get)


def get_offline_response(user_text: str, last_diagnosis: dict = None, ui_lang: str = "en") -> str:
    text = user_text.strip()
    if not text:
        return EMPTY_PROMPT.get(ui_lang, EMPTY_PROMPT["en"])

    lang = detect_language(text, ui_lang)
    text_l = text.lower()

    all_greetings = sum(GREETINGS.values(), [])
    if any(g.lower() == text_l or text_l.startswith(g.lower() + " ") for g in all_greetings):
        return GREETING_REPLY.get(lang, GREETING_REPLY["en"]) + " " + DISCLAIMER.get(lang, DISCLAIMER["en"])

    if any(trigger in text_l for trigger in MY_RESULT_TRIGGERS):
        if last_diagnosis:
            pred = last_diagnosis.get("prediction", "Normal Z-line")
            conf = last_diagnosis.get("confidence", 0) * 100
            templates = RESULT_TEMPLATES.get(lang, RESULT_TEMPLATES["en"])
            template = templates.get(pred, templates["Normal Z-line"])
            return template.format(pred=pred, conf=conf) + " " + DISCLAIMER.get(lang, DISCLAIMER["en"])
        return NO_SAVED_RESULT.get(lang, NO_SAVED_RESULT["en"])

    topic = _match_topic(text)
    if topic:
        kb = KNOWLEDGE_BASE.get(lang, KNOWLEDGE_BASE["en"])
        answer = kb.get(topic) or KNOWLEDGE_BASE["en"].get(topic)
        return answer + "\n\n" + DISCLAIMER.get(lang, DISCLAIMER["en"])

    return NO_MATCH.get(lang, NO_MATCH["en"]) + " " + DISCLAIMER.get(lang, DISCLAIMER["en"])


def _build_system_prompt(last_diagnosis: dict = None, ui_lang: str = "en") -> str:
    context = ""
    if last_diagnosis:
        context = (
            f"\n\nContext: The patient's latest AI screening result was "
            f"'{last_diagnosis.get('prediction')}' with "
            f"{last_diagnosis.get('confidence', 0) * 100:.1f}% confidence."
        )

    return (
        "You are a careful, warm AI health-education assistant embedded in an "
        "esophageal cancer screening demo app. Explain medical concepts about "
        "esophageal cancer, esophagitis, and Barrett's esophagus in plain "
        "language. Always make clear you are not a substitute for a licensed "
        "doctor and encourage professional consultation for diagnosis or "
        "treatment. Keep answers concise (under 150 words). "
        "IMPORTANT LANGUAGE RULE: Detect the language (or mix of languages, "
        "e.g. Hindi+English 'Hinglish') the user is typing in, and reply in "
        "that same language/script. The app's currently selected UI language "
        f"is '{ui_lang}' — use it only as a hint if the user's message itself "
        "is ambiguous (e.g. a single short word)." + context
    )


def detect_provider(api_key: str) -> str:
    """Best-effort guess of which LLM provider an API key belongs to, purely
    from its prefix, so the user doesn't have to pick a provider manually."""
    key = (api_key or "").strip()
    if key.startswith("sk-ant-"):
        return "anthropic"
    if key.startswith("sk-proj-") or key.startswith("sk-"):
        return "openai"
    # Mistral keys have no fixed public prefix convention, so this is the
    # fallback bucket for anything that isn't clearly Anthropic/OpenAI.
    return "mistral"


def get_claude_response(user_text: str, api_key: str, last_diagnosis: dict = None,
                         history=None, ui_lang: str = "en") -> str:
    """Live response via the Anthropic Messages API (Claude)."""
    import json
    import urllib.request

    system_prompt = _build_system_prompt(last_diagnosis, ui_lang)
    messages = (history or []) + [{"role": "user", "content": user_text}]

    payload = json.dumps({
        "model": "claude-sonnet-4-6",
        "max_tokens": 400,
        "system": system_prompt,
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
    if not text_blocks:
        raise ValueError("Empty response from Anthropic API")
    return "\n".join(text_blocks)


def get_openai_response(user_text: str, api_key: str, last_diagnosis: dict = None,
                         history=None, ui_lang: str = "en") -> str:
    """Live response via the OpenAI Chat Completions API (e.g. gpt-4o-mini)."""
    import json
    import urllib.request

    system_prompt = _build_system_prompt(last_diagnosis, ui_lang)
    messages = [{"role": "system", "content": system_prompt}]
    messages += (history or [])
    messages.append({"role": "user", "content": user_text})

    payload = json.dumps({
        "model": "gpt-4o-mini",
        "max_tokens": 400,
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Empty response from OpenAI API")
    return choices[0]["message"]["content"]


def get_mistral_response(user_text: str, api_key: str, last_diagnosis: dict = None,
                          history=None, ui_lang: str = "en") -> str:
    """Live response via the Mistral AI Chat Completions API."""
    import json
    import urllib.request

    system_prompt = _build_system_prompt(last_diagnosis, ui_lang)
    messages = [{"role": "system", "content": system_prompt}]
    messages += (history or [])
    messages.append({"role": "user", "content": user_text})

    payload = json.dumps({
        "model": "mistral-small-latest",
        "max_tokens": 400,
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.mistral.ai/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Empty response from Mistral API")
    return choices[0]["message"]["content"]


_PROVIDER_FUNCS = {
    "anthropic": get_claude_response,
    "openai": get_openai_response,
    "mistral": get_mistral_response,
}


def get_llm_response(user_text: str, api_key: str, provider: str = "auto",
                      last_diagnosis: dict = None, history=None,
                      ui_lang: str = "en") -> str:
    """Single entry point the app should call. Works with ANY of the
    supported providers' API keys — Anthropic, OpenAI, or Mistral.

    - If `provider` is "auto" (default), the provider is guessed from the
      key's prefix.
    - If the live call fails for any reason (bad key, network, rate limit,
      wrong provider guess), it transparently falls back to the offline
      knowledge-base answer instead of showing an error, so the chat box
      always returns a correct, usable reply.
    """
    if not api_key:
        return get_offline_response(user_text, last_diagnosis, ui_lang)

    chosen = provider if provider in _PROVIDER_FUNCS else detect_provider(api_key)
    func = _PROVIDER_FUNCS.get(chosen, get_claude_response)

    try:
        return func(user_text, api_key, last_diagnosis, history, ui_lang)
    except Exception:
        # If we guessed the provider (or the user's choice) wrong, try the
        # other two before giving up and falling back to offline mode.
        for name, other_func in _PROVIDER_FUNCS.items():
            if name == chosen:
                continue
            try:
                return other_func(user_text, api_key, last_diagnosis, history, ui_lang)
            except Exception:
                continue
        return get_offline_response(user_text, last_diagnosis, ui_lang)
