# AI Health & Fitness Planner

## Proje Tanımı ve Amaç

Bu proje, kişiselleştirilmiş beslenme ve fitness planları sunan AI destekli bir sağlık asistanıdır. LangChain ve Google Gemini entegrasyonu ile kullanıcıların yaş, kilo, boy, aktivite seviyesi ve hedeflerine göre özel planlar oluşturur. Modern Gradio arayüzü ile kullanıcı dostu deneyim sunar.

**Ana Amaç:** Kullanıcıların sağlık ve fitness hedeflerine ulaşmasına yardımcı olmak, kişiselleştirilmiş beslenme ve egzersiz önerileri sunmak, sağlıklı yaşam tarzı benimsemelerini desteklemektir.

## Aktif Ekip Üyeleri

- **Ulaş Pirim**
- **Ahmet Furkan Çayırtepe**
- **Ozan Kalınağaç**
- **Kadir Zeyrek**

## Süreç ve Yöntem

- Proje yönetimi ve süreç takibi için **Trello** aktif olarak kullanılmaktadır.
- Scrum metodolojisiyle, düzenli sprint planlamaları, günlük standup'lar ve sprint retrospektifleri gerçekleştirilmektedir.
- Ekip içi iletişim ve şeffaflık ön planda tutulmakta, ilerleme ve riskler düzenli olarak değerlendirilmekte ve raporlanmaktadır.
- Sürekli iyileştirme ve iteratif geliştirme yaklaşımı benimsenmiştir.

## Sprint 1: Tanışma, Kaynaşma ve Proje Planlama

- Grup değişikliği sonrası ilk sprintte ekip üyeleriyle tanışma ve kaynaşma sağlandı.
- Her üyenin güçlü yönleri ve ilgi alanları belirlendi.
- Proje konusu olarak sağlıkta yapay zeka destekli randevu ve ön değerlendirme sistemi seçildi.
- Hangi alanlara odaklanacağımız (web, otomasyon, veri bilimi) netleştirildi.
- MVP için temel hedefler ve iş bölümü oluşturuldu.

### Sprint 1 Hedefleri

- Ekip içi iletişim ve rol paylaşımı
- Proje fikrinin netleştirilmesi
- Kullanılacak teknolojilerin ve entegrasyonların belirlenmesi
- Veri bilimi/analizi için temel modül planı

## Sprint 2: AI Health & Fitness Planner (Agent v1) Geliştirme

- **AI Health & Fitness Planner Agent v1 başarıyla tamamlandı!** ✅
- LangChain framework'ü ile Google Gemini 2.0 Flash entegrasyonu gerçekleştirildi.
- Modern Gradio arayüzü tasarlandı ve implement edildi.
- Kişiselleştirilmiş beslenme ve fitness planları üreten AI sistemi geliştirildi.
- Prompt engineering ile Türkçe beslenme ve fitness önerileri optimize edildi.
- Soru-cevap sistemi ile kullanıcı etkileşimi sağlandı.
- Kapsamlı test sistemi oluşturuldu ve tüm testler başarıyla geçildi.

### Sprint 2 Başarıları

- ✅ **LangChain + Google Gemini Entegrasyonu:** Modern AI framework entegrasyonu
- ✅ **Gradio Arayüzü:** Modern ve responsive web arayüzü
- ✅ **Prompt Template'leri:** Beslenme, fitness ve Q&A için özelleştirilmiş promptlar
- ✅ **Kişiselleştirme:** Yaş, kilo, boy, aktivite seviyesi ve hedeflere göre özel planlar
- ✅ **Türkçe Destek:** Tamamen Türkçe arayüz ve çıktılar
- ✅ **Hata Yönetimi:** Kapsamlı error handling ve kullanıcı dostu mesajlar
- ✅ **Test Coverage:** %100 test başarı oranı
- ✅ **Dokümantasyon:** Kapsamlı README ve kullanım kılavuzları

### Sprint 2 Teknik Detaylar

- **Frontend:** Gradio 4.44.0 (Modern, responsive UI)
- **AI Framework:** LangChain 0.3.26
- **AI Model:** Google Gemini 2.0 Flash
- **Prompt Engineering:** 3 farklı prompt template (Beslenme, Fitness, Q&A)
- **Architecture:** Modular yapı, kolay genişletilebilir
- **Deployment:** Local ve cloud-ready

## Kullanılan Teknolojiler ve Entegrasyonlar

### 🧠 AI ve Machine Learning

- **LangChain 0.3.26:** AI framework ve prompt management
- **Google Gemini 2.0 Flash:** Gelişmiş AI model entegrasyonu
- **Prompt Engineering:** Özelleştirilmiş Türkçe prompt template'leri
- **LLMChain:** LangChain LLM entegrasyonu

### 🖥️ Frontend ve UI/UX

- **Gradio 4.44.0:** Modern web arayüzü ve kullanıcı deneyimi
- **Responsive Design:** Mobil ve desktop uyumlu arayüz
- **Real-time Updates:** Anlık plan üretimi ve güncellemeler

### 💻 Backend ve Development

- **Python 3.12:** Ana programlama dili
- **Environment Management:** .env dosyası ile API key yönetimi
- **Error Handling:** Kapsamlı hata yönetimi ve kullanıcı dostu mesajlar
- **Session Management:** Gradio session state yönetimi

### 🧪 Testing ve Quality Assurance

- **Unit Testing:** Kapsamlı test coverage (%100)
- **Import Testing:** Tüm modüllerin doğru import edilmesi
- **Component Testing:** Gradio bileşenlerinin test edilmesi
- **Integration Testing:** LangChain + Gemini entegrasyon testleri

### 📦 Dependencies ve Package Management

- **requirements.txt:** Python paket yönetimi
- **Version Control:** Git ile versiyon kontrolü
- **Documentation:** Kapsamlı README ve kullanım kılavuzları

## Proje Akışı ve Standup Örnekleri

### Daily Standup Örneği

- **Dün:** AI Health & Fitness Planner Agent v1 tamamlandı, tüm testler başarılı.
- **Bugün:** Agent'ın production'a hazır hale getirilmesi ve dokümantasyon tamamlanması.
- **Engeller:** Yok - tüm hedefler başarıyla tamamlandı.

### Sprint Board

- [x] Ekip tanışma ve rol paylaşımı
- [x] Proje fikri ve hedeflerin belirlenmesi
- [x] AI Health & Fitness Planner Agent v1 geliştirme
- [x] LangChain + Google Gemini entegrasyonu
- [x] Gradio arayüzü tasarımı ve implementasyonu
- [x] Prompt engineering ve Türkçe optimizasyonu
- [x] Test sistemi ve %100 test coverage
- [x] Dokümantasyon ve kullanım kılavuzları

## Ana Özellikler ve MVP Hedefleri

- **Kişiselleştirilmiş Beslenme Planları:** Yaş, kilo, boy ve hedeflere göre özel diyet önerileri
- **Kişiselleştirilmiş Fitness Planları:** Aktivite seviyesi ve hedeflere göre egzersiz rutinleri
- **AI Destekli Soru-Cevap Sistemi:** Planlar hakkında akıllı öneriler ve açıklamalar
- **Modern Gradio Arayüzü:** Kullanıcı dostu, responsive web arayüzü
- **Türkçe Destek:** Tamamen Türkçe arayüz ve çıktılar
- **Gerçek Zamanlı Plan Üretimi:** LangChain + Google Gemini ile anında plan oluşturma

## Mentorler için Notlar

- **AI Health & Fitness Planner Agent v1 başarıyla tamamlandı!** ✅
- LangChain framework'ü ile modern AI entegrasyonu sağlandı
- Modern Gradio arayüzü ile kullanıcı deneyimi optimize edildi
- %100 test coverage ile kalite güvencesi sağlandı
- Kapsamlı dokümantasyon ve kullanım kılavuzları hazırlandı
- Proje yönetimi ve ilerleme, Trello üzerinden düzenli olarak takip edilmekte ve raporlanmaktadır.
- Ekip içi iletişim, şeffaflık ve düzenli raporlama süreç boyunca ön planda tutulmaktadır.
- 1 aylık süreçte, temel işlevsellik ve demo odaklı bir MVP çıkarılması planlanıyor.
- Riskler: LLM API kullanımı, zaman yönetimi.

---

> **Not:** Bu proje, eğitim ve demo amaçlıdır. Gerçek hasta verisiyle çalışırken yasal ve etik kurallara uyulmalıdır.
