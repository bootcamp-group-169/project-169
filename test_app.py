#!/usr/bin/env python3
"""
AI Health & Fitness Planner Test Script
Bu dosya uygulamanın temel fonksiyonlarını test eder.
"""

import sys
import os

# Ana dizini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Gerekli kütüphanelerin import edilip edilemediğini test eder"""
    try:
        import gradio as gr
        print("✅ Gradio başarıyla import edildi")
    except ImportError as e:
        print(f"❌ Gradio import hatası: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI başarıyla import edildi")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI import hatası: {e}")
        return False
    
    try:
        from langchain_core.prompts import PromptTemplate
        print("✅ LangChain Core başarıyla import edildi")
    except ImportError as e:
        print(f"❌ LangChain Core import hatası: {e}")
        return False
    
    try:
        from langchain.chains import LLMChain
        print("✅ LangChain Chains başarıyla import edildi")
    except ImportError as e:
        print(f"❌ LangChain Chains import hatası: {e}")
        return False
    
    return True

def test_prompt_templates():
    """Prompt template'lerin doğru oluşturulup oluşturulmadığını test eder"""
    try:
        from langchain_core.prompts import PromptTemplate
        
        # Test prompt template
        test_prompt = PromptTemplate(
            input_variables=["name"],
            template="Merhaba {name}!"
        )
        
        result = test_prompt.format(name="Test")
        expected = "Merhaba Test!"
        
        if result == expected:
            print("✅ Prompt template testi başarılı")
            return True
        else:
            print(f"❌ Prompt template testi başarısız: {result} != {expected}")
            return False
            
    except Exception as e:
        print(f"❌ Prompt template testi hatası: {e}")
        return False

def test_gradio_components():
    """Gradio bileşenlerinin oluşturulup oluşturulmadığını test eder"""
    try:
        import gradio as gr
        
        # Test bileşenleri oluştur
        textbox = gr.Textbox(label="Test")
        number = gr.Number(label="Test", value=10)
        dropdown = gr.Dropdown(choices=["A", "B", "C"], label="Test")
        button = gr.Button("Test")
        
        print("✅ Gradio bileşenleri başarıyla oluşturuldu")
        return True
        
    except Exception as e:
        print(f"❌ Gradio bileşenleri testi hatası: {e}")
        return False

def main():
    """Ana test fonksiyonu"""
    print("🧪 AI Health & Fitness Planner Test Başlatılıyor...")
    print("=" * 50)
    
    tests = [
        ("Kütüphane Import Testi", test_imports),
        ("Prompt Template Testi", test_prompt_templates),
        ("Gradio Bileşenleri Testi", test_gradio_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name} çalıştırılıyor...")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Sonuçları: {passed}/{total} test başarılı")
    
    if passed == total:
        print("🎉 Tüm testler başarılı! Uygulama çalıştırılmaya hazır.")
        print("\n🚀 Uygulamayı başlatmak için:")
        print("   python health_planner.py")
    else:
        print("⚠️ Bazı testler başarısız. Lütfen hataları kontrol edin.")
        print("\n📦 Gerekli paketleri yüklemek için:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 