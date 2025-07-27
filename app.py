import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Environment variables yükle
load_dotenv()

# Global değişkenler
dietary_plan = ""
fitness_plan = ""

def create_llm(api_key):
    """Google Gemini LLM modelini oluşturur"""
    try:
        if not api_key or api_key.strip() == "":
            raise Exception("API key boş!")
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=2048
        )
        
        # Test bağlantısı
        test_response = llm.invoke("Test")
        print(f"API bağlantı testi başarılı: {test_response}")
        
        return llm
    except Exception as e:
        print(f"LLM oluşturma hatası: {e}")
        raise Exception(f"LLM oluşturulurken hata: {e}")

# Bağırsak hastalıkları veritabanı (local storage)
INTESTINAL_DISEASES_DB = {
    "crohn": {
        "name": "Crohn Hastalığı",
        "description": "Kronik inflamatuar bağırsak hastalığı",
        "recommended_foods": [
            "Muz", "Pirinç", "Haşlanmış patates", "Yoğurt", "Tavuk eti", 
            "Balık", "Yumurta", "Ekmek", "Makarna", "Elma püresi"
        ],
        "avoid_foods": [
            "Baharatlı yiyecekler", "Kafein", "Alkol", "Süt ürünleri", 
            "Çiğ sebzeler", "Kuruyemiş", "Tohumlar", "Mısır", "Karnabahar"
        ],
        "diet_tips": [
            "Küçük, sık öğünler yiyin",
            "Yavaş yavaş yiyin ve iyi çiğneyin",
            "Bol su için",
            "Günlük semptom günlüğü tutun"
        ]
    },
    "ulcerative_colitis": {
        "name": "Ülseratif Kolit",
        "description": "Kolon ve rektumda inflamasyon",
        "recommended_foods": [
            "Muz", "Pirinç", "Haşlanmış patates", "Yoğurt", "Tavuk eti",
            "Balık", "Yumurta", "Ekmek", "Makarna", "Elma püresi",
            "Probiyotik yoğurt", "Omega-3 açısından zengin balıklar"
        ],
        "avoid_foods": [
            "Baharatlı yiyecekler", "Kafein", "Alkol", "Süt ürünleri",
            "Çiğ sebzeler", "Kuruyemiş", "Tohumlar", "Mısır", "Karnabahar",
            "Kırmızı et", "İşlenmiş gıdalar"
        ],
        "diet_tips": [
            "Anti-inflamatuar diyet uygulayın",
            "Probiyotik açısından zengin besinler tüketin",
            "Omega-3 açısından zengin besinler yiyin",
            "Günlük semptom günlüğü tutun"
        ]
    },
    "ibs": {
        "name": "İrritabl Bağırsak Sendromu (İBS)",
        "description": "Fonksiyonel bağırsak bozukluğu",
        "recommended_foods": [
            "Muz", "Pirinç", "Haşlanmış patates", "Yoğurt", "Tavuk eti",
            "Balık", "Yumurta", "Ekmek", "Makarna", "Elma püresi",
            "Zencefil", "Nane çayı", "Probiyotik yoğurt"
        ],
        "avoid_foods": [
            "Baharatlı yiyecekler", "Kafein", "Alkol", "Süt ürünleri",
            "Çiğ sebzeler", "Kuruyemiş", "Tohumlar", "Mısır", "Karnabahar",
            "Soğan", "Sarımsak", "Baklagiller", "Lahana"
        ],
        "diet_tips": [
            "FODMAP diyeti uygulayın",
            "Küçük, sık öğünler yiyin",
            "Stres yönetimi yapın",
            "Günlük semptom günlüğü tutun"
        ]
    }
}

# Local storage için basit dosya sistemi
import json
import datetime

def save_to_local_storage(data, filename):
    """Veriyi local storage'a kaydet"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Kaydetme hatası: {e}")
        return False

def load_from_local_storage(filename):
    """Local storage'dan veri yükle"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception as e:
        print(f"Yükleme hatası: {e}")
        return {}

# Prompt template'leri tanımla
DIETARY_PROMPT = PromptTemplate(
    input_variables=["age", "weight", "height", "sex", "activity_level", "dietary_preferences", "fitness_goals"],
    template="""Sen bir beslenme uzmanısın. Aşağıdaki bilgilere göre kişiselleştirilmiş bir beslenme planı oluştur:

Yaş: {age}
Kilo: {weight}kg
Boy: {height}cm
Cinsiyet: {sex}
Aktivite Seviyesi: {activity_level}
Diyet Tercihleri: {dietary_preferences}
Fitness Hedefleri: {fitness_goals}

Lütfen şunları içeren detaylı bir beslenme planı hazırla:
- Kahvaltı önerileri
- Öğle yemeği önerileri  
- Akşam yemeği önerileri
- Ara öğün önerileri
- Günlük su tüketimi
- Kalori hedefleri

Planı Türkçe olarak, anlaşılır ve uygulanabilir şekilde hazırla."""
)

FITNESS_PROMPT = PromptTemplate(
    input_variables=["age", "weight", "height", "sex", "activity_level", "fitness_goals"],
    template="""Sen bir fitness uzmanısın. Aşağıdaki bilgilere göre kişiselleştirilmiş bir egzersiz planı oluştur:

Yaş: {age}
Kilo: {weight}kg
Boy: {height}cm
Cinsiyet: {sex}
Aktivite Seviyesi: {activity_level}
Fitness Hedefleri: {fitness_goals}

Lütfen şunları içeren detaylı bir egzersiz planı hazırla:
- Isınma egzersizleri (5-10 dakika)
- Ana egzersiz rutini (30-45 dakika)
- Soğuma egzersizleri (5-10 dakika)
- Haftalık program önerisi
- Egzersiz yoğunluğu ve set/tekrar sayıları
- Güvenlik önerileri

Planı Türkçe olarak, anlaşılır ve uygulanabilir şekilde hazırla."""
)

QA_PROMPT = PromptTemplate(
    input_variables=["question", "dietary_plan", "fitness_plan"],
    template="""Aşağıdaki beslenme ve fitness planlarına göre kullanıcının sorusunu yanıtla:

BESLENME PLANI:
{dietary_plan}

FITNESS PLANI:
{fitness_plan}

KULLANICI SORUSU: {question}

Lütfen soruyu Türkçe olarak, planlarla tutarlı şekilde yanıtla. Eğer planlarda yeterli bilgi yoksa, genel sağlık ve fitness önerileri ver."""
)

# Bağırsak hastalıkları için özel prompt template
INTESTINAL_PROMPT = PromptTemplate(
    input_variables=["disease_type", "age", "weight", "height", "sex", "activity_level", "symptoms"],
    template="""Sen bir gastroenteroloji uzmanısın. Aşağıdaki bilgilere göre kişiselleştirilmiş bir bağırsak sağlığı planı oluştur:

Hastalık Türü: {disease_type}
Yaş: {age}
Kilo: {weight}kg
Boy: {height}cm
Cinsiyet: {sex}
Aktivite Seviyesi: {activity_level}
Semptomlar: {symptoms}

Lütfen şunları içeren detaylı bir bağırsak sağlığı planı hazırla:
- Özel beslenme önerileri
- Kaçınılması gereken besinler
- Günlük yaşam önerileri
- Semptom yönetimi
- İlaç hatırlatıcıları
- Doktor kontrolü önerileri

Planı Türkçe olarak, anlaşılır ve uygulanabilir şekilde hazırla."""
)

def generate_plans(api_key, age, weight, height, sex, activity_level, dietary_preferences, fitness_goals):
    """Kişiselleştirilmiş beslenme ve fitness planlarını üretir"""
    global dietary_plan, fitness_plan
    
    try:
        # LLM oluştur
        llm = create_llm(api_key)
        
        # Chain'leri oluştur
        dietary_chain = LLMChain(llm=llm, prompt=DIETARY_PROMPT)
        fitness_chain = LLMChain(llm=llm, prompt=FITNESS_PROMPT)
        
        # Planları üret
        dietary_response = dietary_chain.invoke({
            "age": age, "weight": weight, "height": height, "sex": sex,
            "activity_level": activity_level, "dietary_preferences": dietary_preferences,
            "fitness_goals": fitness_goals
        })
        
        fitness_response = fitness_chain.invoke({
            "age": age, "weight": weight, "height": height, "sex": sex,
            "activity_level": activity_level, "fitness_goals": fitness_goals
        })
        
        # Global değişkenleri güncelle
        dietary_plan = dietary_response["text"]
        fitness_plan = fitness_response["text"]
        
        # AI çıktılarını formatla
        formatted_dietary = format_dietary_plan(dietary_plan)
        formatted_fitness = format_fitness_plan(fitness_plan)
        
        return formatted_dietary, formatted_fitness, "✅ Planlar başarıyla oluşturuldu!"
        
    except Exception as e:
        return "", "", f"❌ Hata oluştu: {e}"

def format_dietary_plan(text):
    """Beslenme planını formatla"""
    if not text:
        return "❌ Beslenme planı oluşturulamadı."
    
    formatted = "🍽️ **Kişiselleştirilmiş Beslenme Planı**\n\n"
    
    # Metni paragraflara böl
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if paragraph.startswith('**') and paragraph.endswith('**'):
            formatted += f"📋 {paragraph}\n\n"
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            parts = paragraph.split(':', 1)
            if len(parts) == 2:
                title, content = parts
                formatted += f"🔹 **{title.strip()}:** {content.strip()}\n\n"
            else:
                formatted += f"• {paragraph}\n\n"
        else:
            formatted += f"📝 {paragraph}\n\n"
    
    formatted += "---\n"
    formatted += "💡 **Beslenme İpuçları:**\n"
    formatted += "• Günde 8-10 bardak su için\n"
    formatted += "• Öğün atlamayın\n"
    formatted += "• Porsiyon kontrolü yapın\n"
    formatted += "• Düzenli beslenin\n\n"
    formatted += "🌟 Sağlıklı beslenme yolculuğunuzda başarılar!"
    
    return formatted

def format_fitness_plan(text):
    """Fitness planını formatla"""
    if not text:
        return "❌ Fitness planı oluşturulamadı."
    
    formatted = "💪 **Kişiselleştirilmiş Fitness Planı**\n\n"
    
    # Metni paragraflara böl
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if paragraph.startswith('**') and paragraph.endswith('**'):
            formatted += f"📋 {paragraph}\n\n"
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            parts = paragraph.split(':', 1)
            if len(parts) == 2:
                title, content = parts
                formatted += f"🔹 **{title.strip()}:** {content.strip()}\n\n"
            else:
                formatted += f"• {paragraph}\n\n"
        else:
            formatted += f"📝 {paragraph}\n\n"
    
    formatted += "---\n"
    formatted += "💡 **Fitness İpuçları:**\n"
    formatted += "• Isınma yapmadan egzersize başlamayın\n"
    formatted += "• Düzenli egzersiz yapın\n"
    formatted += "• Vücudunuzu dinleyin\n"
    formatted += "• Su tüketimini artırın\n\n"
    formatted += "🌟 Fitness hedeflerinize ulaşmanızda başarılar!"
    
    return formatted

def answer_question(api_key, question):
    """Kullanıcının sorusunu yanıtlar"""
    global dietary_plan, fitness_plan
    
    if not dietary_plan or not fitness_plan:
        return "⚠️ Önce bir plan oluşturmanız gerekiyor!"
    
    if not question.strip():
        return "⚠️ Lütfen bir soru sorun!"
    
    try:
        # LLM oluştur
        llm = create_llm(api_key)
        
        # QA chain oluştur
        qa_chain = LLMChain(llm=llm, prompt=QA_PROMPT)
        
        # Soruyu yanıtla
        response = qa_chain.invoke({
            "question": question,
            "dietary_plan": dietary_plan,
            "fitness_plan": fitness_plan
        })
        
        # AI çıktısını formatla
        formatted_answer = format_qa_response(response["text"], question)
        
        return formatted_answer
        
    except Exception as e:
        return f"❌ Hata oluştu: {e}"

def format_qa_response(text, question):
    """Q&A cevabını formatla"""
    if not text:
        return "❌ Cevap oluşturulamadı."
    
    formatted = f"🤖 **Soru:** {question}\n\n"
    formatted += "💡 **Cevap:**\n\n"
    
    # Metni paragraflara böl
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if paragraph.startswith('**') and paragraph.endswith('**'):
            formatted += f"📋 {paragraph}\n\n"
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            parts = paragraph.split(':', 1)
            if len(parts) == 2:
                title, content = parts
                formatted += f"🔹 **{title.strip()}:** {content.strip()}\n\n"
            else:
                formatted += f"• {paragraph}\n\n"
        else:
            formatted += f"📝 {paragraph}\n\n"
    
    formatted += "---\n"
    formatted += "💡 **İpucu:** Başka sorularınız varsa sormaktan çekinmeyin!"
    
    return formatted

def generate_intestinal_plan(api_key, disease_type, age, weight, height, sex, activity_level, symptoms):
    """Bağırsak hastalıkları için özel plan üretir"""
    try:
        # LLM oluştur
        llm = create_llm(api_key)
        
        # Intestinal chain oluştur
        intestinal_chain = LLMChain(llm=llm, prompt=INTESTINAL_PROMPT)
        
        # Plan üret
        response = intestinal_chain.invoke({
            "disease_type": disease_type,
            "age": age,
            "weight": weight,
            "height": height,
            "sex": sex,
            "activity_level": activity_level,
            "symptoms": symptoms
        })
        
        # AI çıktısını formatla
        formatted_plan = format_ai_response(response["text"])
        
        return formatted_plan, "✅ Bağırsak sağlığı planı başarıyla oluşturuldu!"
        
    except Exception as e:
        return "", f"❌ Hata oluştu: {e}"

def format_ai_response(text):
    """AI çıktısını güzel formatla"""
    if not text:
        return "❌ Plan oluşturulamadı."
    
    # Başlık ekle
    formatted = "🏥 **Bağırsak Sağlığı Planı**\n\n"
    
    # Metni paragraflara böl
    paragraphs = text.split('\n\n')
    
    for i, paragraph in enumerate(paragraphs):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Başlıkları formatla
        if paragraph.startswith('**') and paragraph.endswith('**'):
            formatted += f"📋 {paragraph}\n\n"
        elif ':' in paragraph and len(paragraph.split(':')[0]) < 50:
            # Alt başlık formatı
            parts = paragraph.split(':', 1)
            if len(parts) == 2:
                title, content = parts
                formatted += f"🔹 **{title.strip()}:** {content.strip()}\n\n"
            else:
                formatted += f"• {paragraph}\n\n"
        else:
            # Normal paragraf
            formatted += f"📝 {paragraph}\n\n"
    
    # Sonuç ekle
    formatted += "---\n"
    formatted += "💡 **Önemli Notlar:**\n"
    formatted += "• Bu plan genel bir rehberdir\n"
    formatted += "• Doktorunuzla paylaşın\n"
    formatted += "• Semptomlarınızı takip edin\n"
    formatted += "• Düzenli kontroller yaptırın\n\n"
    formatted += "🌟 Umarım bu plan size yardımcı olur. Geçmiş olsun!"
    
    return formatted

def save_symptom_log(date, disease_type, symptoms, severity, notes):
    """Semptom günlüğünü kaydet"""
    try:
        log_data = load_from_local_storage("symptom_log.json")
        
        log_entry = {
            "date": date,
            "disease_type": disease_type,
            "symptoms": symptoms,
            "severity": severity,
            "notes": notes,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        if date not in log_data:
            log_data[date] = []
        
        log_data[date].append(log_entry)
        
        if save_to_local_storage(log_data, "symptom_log.json"):
            return "✅ Semptom günlüğü kaydedildi!"
        else:
            return "❌ Kaydetme hatası!"
            
    except Exception as e:
        return f"❌ Hata oluştu: {e}"

def get_disease_info(disease_type):
    """Hastalık bilgilerini getir"""
    if disease_type in INTESTINAL_DISEASES_DB:
        disease = INTESTINAL_DISEASES_DB[disease_type]
        return f"""
**{disease['name']}**
{disease['description']}

**Önerilen Besinler:**
{', '.join(disease['recommended_foods'])}

**Kaçınılması Gereken Besinler:**
{', '.join(disease['avoid_foods'])}

**Diyet İpuçları:**
{chr(10).join(['• ' + tip for tip in disease['diet_tips']])}
"""
    else:
        return "❌ Hastalık bilgisi bulunamadı!"

def get_symptom_history():
    """Semptom geçmişini getir"""
    try:
        log_data = load_from_local_storage("symptom_log.json")
        if not log_data:
            return "Henüz semptom günlüğü kaydı yok."
        
        history = "**Semptom Geçmişi:**\n\n"
        for date, entries in log_data.items():
            history += f"**{date}:**\n"
            for entry in entries:
                history += f"• {entry['disease_type']} - {entry['symptoms']} (Şiddet: {entry['severity']})\n"
                if entry['notes']:
                    history += f"  Not: {entry['notes']}\n"
            history += "\n"
        
        return history
        
    except Exception as e:
        return f"❌ Geçmiş yüklenirken hata: {e}"

def save_food_log(date, meal_type, food_name, symptoms, notes):
    """Tek besin günlüğünü kaydet"""
    try:
        food_data = load_from_local_storage("food_log.json")
        
        food_entry = {
            "date": date,
            "meal_type": meal_type,
            "food_name": food_name.strip(),
            "symptoms": symptoms,
            "notes": notes,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        if date not in food_data:
            food_data[date] = []
        
        food_data[date].append(food_entry)
        
        if save_to_local_storage(food_data, "food_log.json"):
            return f"✅ {food_name} kaydedildi!"
        else:
            return "❌ Kaydetme hatası!"
            
    except Exception as e:
        return f"❌ Hata oluştu: {e}"

def get_food_history():
    """Besin geçmişini getir"""
    try:
        food_data = load_from_local_storage("food_log.json")
        if not food_data:
            return "Henüz besin günlüğü kaydı yok."
        
        history = "🍽️ **Besin Geçmişi**\n\n"
        for date, entries in food_data.items():
            history += f"📅 **{date}**\n"
            for entry in entries:
                history += f"• {entry['meal_type']}: {entry['food_name']}\n"
                if entry['symptoms']:
                    history += f"  ⚠️ Semptomlar: {entry['symptoms']}\n"
                if entry['notes']:
                    history += f"  📝 Not: {entry['notes']}\n"
            history += "\n"
        
        return history
        
    except Exception as e:
        return f"❌ Geçmiş yüklenirken hata: {e}"

def get_food_analysis():
    """Besin analizi yap - hangi besinler rahatsız ediyor"""
    try:
        food_data = load_from_local_storage("food_log.json")
        if not food_data:
            return "Henüz besin günlüğü kaydı yok."
        
        # Besin-semptom ilişkisini analiz et
        food_symptoms = {}
        food_count = {}
        
        for date, entries in food_data.items():
            for entry in entries:
                food_name = entry['food_name']
                symptoms = entry['symptoms']
                
                # Besin sayısını tut
                if food_name not in food_count:
                    food_count[food_name] = 0
                food_count[food_name] += 1
                
                # Semptom varsa kaydet
                if symptoms and symptoms.strip():
                    if food_name not in food_symptoms:
                        food_symptoms[food_name] = []
                    food_symptoms[food_name].append(symptoms)
        
        # Analiz sonuçlarını oluştur
        analysis = "🔍 **Besin Analizi**\n\n"
        
        if food_symptoms:
            analysis += "⚠️ **Rahatsız Eden Besinler:**\n\n"
            for food, symptoms_list in food_symptoms.items():
                total_eaten = food_count.get(food, 0)
                problematic_count = len(symptoms_list)
                percentage = (problematic_count / total_eaten) * 100
                
                analysis += f"🍽️ **{food}**\n"
                analysis += f"   📊 {problematic_count}/{total_eaten} kez rahatsız etti (%{percentage:.1f})\n"
                analysis += f"   🚨 Semptomlar: {', '.join(set(symptoms_list))}\n\n"
        else:
            analysis += "✅ Henüz rahatsız eden besin tespit edilmedi.\n\n"
        
        # AI önerisi ekle
        analysis += "🤖 **AI Önerileri:**\n\n"
        if food_symptoms:
            problematic_foods = list(food_symptoms.keys())
            analysis += f"• Bu besinlerden kaçınmanızı öneririm: {', '.join(problematic_foods)}\n"
            analysis += "• Semptomlarınızı doktorunuzla paylaşın\n"
            analysis += "• Alternatif besinler deneyin\n"
        else:
            analysis += "• Besin günlüğünüze devam edin\n"
            analysis += "• Farklı besinler deneyerek toleransınızı test edin\n"
        
        return analysis
        
    except Exception as e:
        return f"❌ Analiz hatası: {e}"

# Gradio arayüzünü oluştur
with gr.Blocks(
    title="AI Health & Fitness Planner",
    theme=gr.themes.Soft(),
    css="""
    .gradio-container {
        max-width: 1200px !important;
    }
    .output-markdown {
        background-color: #f8f9fa !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        min-height: 200px !important;
    }
    .output-markdown h1, .output-markdown h2, .output-markdown h3 {
        color: #2c3e50 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
    }
    .output-markdown strong {
        color: #e74c3c !important;
    }
    .output-markdown ul, .output-markdown ol {
        margin-left: 20px !important;
    }
    .output-markdown li {
        margin-bottom: 5px !important;
    }
    """
) as demo:
    
    # Başlık
    gr.Markdown("""
    # 🏋️‍♂️ AI Health & Fitness Planner
    
    Kişiselleştirilmiş beslenme ve fitness planları için AI destekli asistanınız.
    """)
    
    # Tab sistemi oluştur
    with gr.Tabs():
        with gr.Tab("🏋️‍♂️ Genel Sağlık & Fitness"):
            # Ana layout
            with gr.Row():
                # Sol kolon - Giriş formu
                with gr.Column(scale=1):
                    gr.Markdown("### 🔑 API Konfigürasyonu")
                    api_key = gr.Textbox(
                        label="Gemini API Key",
                        type="password",
                        placeholder="API key otomatik yüklendi",
                        value=os.getenv("GOOGLE_API_KEY", ""),
                        info="API key .env dosyasından otomatik yüklendi"
                    )
                    
                    gr.Markdown("### 👤 Kişisel Bilgiler")
                    age = gr.Number(
                        label="Yaş",
                        minimum=10,
                        maximum=100,
                        value=25,
                        step=1
                    )
                    
                    weight = gr.Number(
                        label="Kilo (kg)",
                        minimum=20,
                        maximum=300,
                        value=70,
                        step=0.1
                    )
                    
                    height = gr.Number(
                        label="Boy (cm)",
                        minimum=100,
                        maximum=250,
                        value=170,
                        step=0.1
                    )
                    
                    sex = gr.Dropdown(
                        choices=["Erkek", "Kadın", "Diğer"],
                        label="Cinsiyet",
                        value="Erkek"
                    )
                    
                    activity_level = gr.Dropdown(
                        choices=[
                            "Hareketsiz (Günlük aktivite yok)",
                            "Hafif Aktif (Haftada 1-3 gün egzersiz)",
                            "Orta Aktif (Haftada 3-5 gün egzersiz)",
                            "Çok Aktif (Haftada 6-7 gün egzersiz)",
                            "Aşırı Aktif (Günde 2+ kez egzersiz)"
                        ],
                        label="Aktivite Seviyesi",
                        value="Orta Aktif (Haftada 3-5 gün egzersiz)"
                    )
                    
                    dietary_preferences = gr.Dropdown(
                        choices=[
                            "Vejetaryen",
                            "Keto",
                            "Glutensiz",
                            "Düşük Karbonhidrat",
                            "Süt Ürünü İçermeyen",
                            "Genel (Kısıtlama yok)"
                        ],
                        label="Diyet Tercihleri",
                        value="Genel (Kısıtlama yok)"
                    )
                    
                    fitness_goals = gr.Dropdown(
                        choices=[
                            "Kilo Vermek",
                            "Kas Kazanmak",
                            "Dayanıklılık",
                            "Formda Kalmak",
                            "Güç Antrenmanı"
                        ],
                        label="Fitness Hedefleri",
                        value="Formda Kalmak"
                    )
                    
                    generate_btn = gr.Button(
                        "🎯 Kişiselleştirilmiş Planımı Oluştur",
                        variant="primary",
                        size="lg"
                    )
                    
                    status_output = gr.Textbox(
                        label="Durum",
                        interactive=False,
                        lines=2
                    )
                
                # Sağ kolon - Çıktılar
                with gr.Column(scale=1):
                    gr.Markdown("### 📋 Beslenme Planı")
                    dietary_output = gr.Markdown(
                        value="Plan oluşturulduktan sonra burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
                    
                    gr.Markdown("### 💪 Fitness Planı")
                    fitness_output = gr.Markdown(
                        value="Plan oluşturulduktan sonra burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
    
    # Tab sistemi oluştur
    with gr.Tabs():
        with gr.Tab("🏋️‍♂️ Genel Sağlık & Fitness"):
            # Q&A Bölümü
            gr.Markdown("---")
            gr.Markdown("### ❓ Planınız Hakkında Sorular")
            
            with gr.Row():
                question_input = gr.Textbox(
                    label="Sorunuzu buraya yazın...",
                    placeholder="Örn: Bu planı nasıl uygulayabilirim?",
                    lines=2
                )
                ask_btn = gr.Button("🤖 Cevap Al", variant="secondary")
            
            answer_output = gr.Markdown(
                value="Cevap burada görünecek...",
                elem_classes=["output-markdown"]
            )
            
        with gr.Tab("🏥 Bağırsak Hastalıkları"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("#### 📋 Hastalık Bilgileri")
                    disease_info_btn = gr.Button("📖 Hastalık Bilgilerini Göster", variant="secondary")
                    disease_info_output = gr.Markdown(
                        value="Hastalık bilgileri burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("#### 📊 Semptom Geçmişi")
                    history_btn = gr.Button("📈 Geçmişi Göster", variant="secondary")
                    history_output = gr.Markdown(
                        value="Semptom geçmişi burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
            
            # Bağırsak Sağlığı Planı Oluşturma
            gr.Markdown("#### 🎯 Bağırsak Sağlığı Planı Oluştur")
            
            with gr.Row():
                with gr.Column(scale=1):
                    disease_type = gr.Dropdown(
                        choices=["Crohn Hastalığı", "Ülseratif Kolit", "İBS (İrritabl Bağırsak Sendromu)"],
                        label="Hastalık Türü",
                        value="Crohn Hastalığı"
                    )
                    
                    symptoms = gr.Textbox(
                        label="Semptomlar",
                        placeholder="Örn: Karın ağrısı, ishal, yorgunluk...",
                        lines=3
                    )
                    
                    create_intestinal_btn = gr.Button("🏥 Bağırsak Sağlığı Planı Oluştur", variant="primary")
                    
                    intestinal_status = gr.Textbox(
                        label="Durum",
                        interactive=False,
                        lines=2
                    )
                
                with gr.Column(scale=1):
                    intestinal_plan_output = gr.Markdown(
                        value="Plan oluşturulduktan sonra burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
            
            # Semptom Günlüğü
            gr.Markdown("#### 📝 Semptom Günlüğü")
            
            with gr.Row():
                with gr.Column(scale=1):
                    log_date = gr.Textbox(
                        label="Tarih",
                        placeholder="YYYY-MM-DD",
                        value=datetime.datetime.now().strftime("%Y-%m-%d")
                    )
                    
                    log_disease_type = gr.Dropdown(
                        choices=["Crohn Hastalığı", "Ülseratif Kolit", "İBS (İrritabl Bağırsak Sendromu)"],
                        label="Hastalık Türü",
                        value="Crohn Hastalığı"
                    )
                    
                    log_symptoms = gr.Textbox(
                        label="Semptomlar",
                        placeholder="Bugün yaşadığınız semptomlar...",
                        lines=2
                    )
                    
                    severity = gr.Dropdown(
                        choices=["Hafif", "Orta", "Şiddetli"],
                        label="Şiddet",
                        value="Orta"
                    )
                    
                    log_notes = gr.Textbox(
                        label="Notlar",
                        placeholder="Ek notlarınız...",
                        lines=2
                    )
                    
                    save_log_btn = gr.Button("💾 Günlük Kaydet", variant="secondary")
                    
                    log_status = gr.Textbox(
                        label="Kaydetme Durumu",
                        interactive=False,
                        lines=2
                    )
            
            # Besin Takip Sistemi
            gr.Markdown("#### 🍽️ Besin Takip Sistemi")
            
            with gr.Row():
                with gr.Column(scale=1):
                    food_date = gr.Textbox(
                        label="Tarih",
                        placeholder="YYYY-MM-DD",
                        value=datetime.datetime.now().strftime("%Y-%m-%d")
                    )
                    
                    meal_type = gr.Dropdown(
                        choices=["Kahvaltı", "Öğle Yemeği", "Akşam Yemeği", "Ara Öğün"],
                        label="Öğün Türü",
                        value="Kahvaltı"
                    )
                    
                    foods = gr.Textbox(
                        label="Besin Adı",
                        placeholder="Örn: Yumurta (tek besin girin)",
                        lines=1
                    )
                    
                    food_symptoms = gr.Textbox(
                        label="Rahatsız Etti mi?",
                        placeholder="Örn: Karın ağrısı, ishal, gaz (boş bırakın eğer rahatsız etmediyse)",
                        lines=2
                    )
                    
                    food_notes = gr.Textbox(
                        label="Notlar",
                        placeholder="Ek notlarınız...",
                        lines=2
                    )
                    
                    save_food_btn = gr.Button("🍽️ Besin Kaydet", variant="secondary")
                    
                    food_status = gr.Textbox(
                        label="Kaydetme Durumu",
                        interactive=False,
                        lines=2
                    )
                
                with gr.Column(scale=1):
                    gr.Markdown("#### 📊 Besin Analizi")
                    food_analysis_btn = gr.Button("📈 Analiz Yap", variant="secondary")
                    food_analysis_output = gr.Markdown(
                        value="Analiz sonuçları burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
                    
                    gr.Markdown("#### 📋 Besin Geçmişi")
                    food_history_btn = gr.Button("📖 Geçmişi Göster", variant="secondary")
                    food_history_output = gr.Markdown(
                        value="Besin geçmişi burada görünecek...",
                        elem_classes=["output-markdown"]
                    )
    
    # Event handlers
    generate_btn.click(
        fn=generate_plans,
        inputs=[
            api_key, age, weight, height, sex, 
            activity_level, dietary_preferences, fitness_goals
        ],
        outputs=[dietary_output, fitness_output, status_output]
    )
    
    ask_btn.click(
        fn=answer_question,
        inputs=[api_key, question_input],
        outputs=[answer_output]
    )
    
    # Enter tuşu ile soru sorma
    question_input.submit(
        fn=answer_question,
        inputs=[api_key, question_input],
        outputs=[answer_output]
    )
    
    # Bağırsak hastalıkları event handlers
    disease_info_btn.click(
        fn=lambda: get_disease_info("crohn"),
        inputs=[],
        outputs=[disease_info_output]
    )
    
    history_btn.click(
        fn=get_symptom_history,
        inputs=[],
        outputs=[history_output]
    )
    
    create_intestinal_btn.click(
        fn=generate_intestinal_plan,
        inputs=[api_key, disease_type, age, weight, height, sex, activity_level, symptoms],
        outputs=[intestinal_plan_output, intestinal_status]
    )
    
    save_log_btn.click(
        fn=save_symptom_log,
        inputs=[log_date, log_disease_type, log_symptoms, severity, log_notes],
        outputs=[log_status]
    )
    
    # Besin takip event handlers
    save_food_btn.click(
        fn=save_food_log,
        inputs=[food_date, meal_type, foods, food_symptoms, food_notes],
        outputs=[food_status]
    )
    
    food_analysis_btn.click(
        fn=get_food_analysis,
        inputs=[],
        outputs=[food_analysis_output]
    )
    
    food_history_btn.click(
        fn=get_food_history,
        inputs=[],
        outputs=[food_history_output]
    )

# Hugging Face Spaces için gerekli
demo.launch() 