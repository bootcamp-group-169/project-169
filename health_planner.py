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
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_tokens=2048
        )
    except Exception as e:
        raise Exception(f"LLM oluşturulurken hata: {e}")

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
        
        return dietary_plan, fitness_plan, "✅ Planlar başarıyla oluşturuldu!"
        
    except Exception as e:
        return "", "", f"❌ Hata oluştu: {e}"

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
        
        return response["text"]
        
    except Exception as e:
        return f"❌ Hata oluştu: {e}"

def create_interface():
    """Gradio arayüzünü oluşturur"""
    
    with gr.Blocks(
        title="AI Health & Fitness Planner",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        """
    ) as demo:
        
        # Başlık
        gr.Markdown("""
        # 🏋️‍♂️ AI Health & Fitness Planner
        
        Kişiselleştirilmiş beslenme ve fitness planları için AI destekli asistanınız.
        """)
        
        # Ana layout
        with gr.Row():
            # Sol kolon - Giriş formu
            with gr.Column(scale=1):
                gr.Markdown("### 🔑 API Konfigürasyonu")
                api_key = gr.Textbox(
                    label="Gemini API Key",
                    type="password",
                    placeholder="API key'inizi buraya girin...",
                    info="https://aistudio.google.com/apikey adresinden alabilirsiniz"
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
                dietary_output = gr.Textbox(
                    label="",
                    lines=15,
                    max_lines=20,
                    interactive=False,
                    placeholder="Plan oluşturulduktan sonra burada görünecek..."
                )
                
                gr.Markdown("### 💪 Fitness Planı")
                fitness_output = gr.Textbox(
                    label="",
                    lines=15,
                    max_lines=20,
                    interactive=False,
                    placeholder="Plan oluşturulduktan sonra burada görünecek..."
                )
        
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
        
        answer_output = gr.Textbox(
            label="Cevap",
            lines=5,
            interactive=False,
            placeholder="Cevap burada görünecek..."
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
    
    return demo

if __name__ == "__main__":
    # Gradio arayüzünü oluştur ve başlat
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    ) 