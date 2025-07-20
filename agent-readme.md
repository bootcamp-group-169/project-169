<<<<<<< HEAD
# AI Health & Fitness Planner

Kişiselleştirilmiş beslenme ve fitness planları sunan AI destekli uygulama.

## Özellikler

- 🏋️‍♂️ Kişiselleştirilmiş fitness planları
- 🍽️ Beslenme önerileri
- 🤖 Google Gemini AI entegrasyonu
- 💬 Soru-cevap sistemi
- 🎨 Modern Gradio arayüzü

## Kurulum

1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Google AI Studio'dan API key alın:

   - https://aistudio.google.com/apikey adresine gidin
   - Yeni bir API key oluşturun

3. Uygulamayı çalıştırın:

```bash
python health_planner.py
```

## Kullanım

1. API key'inizi girin
2. Kişisel bilgilerinizi doldurun (yaş, ağırlık, boy, vb.)
3. "Generate My Personalized Plan" butonuna tıklayın
4. Planlarınızı inceleyin ve sorularınızı sorun

## Teknolojiler

- **Frontend**: Gradio
- **AI Model**: Google Gemini 2.0 Flash
- **Framework**: LangChain
- **Language**: Python
=======
# Akıllı Randevu ve Ön Değerlendirme Sistemi

## Proje Tanımı ve Amaç

Bu proje, sağlık kurumları için web tabanlı, yapay zeka destekli bir randevu ve ön değerlendirme platformudur. Hastalar, randevu alırken şikayetlerini girer; sistem, semptomlara göre önceliklendirme ve yönlendirme yapar. n8n otomasyon entegrasyonu ile randevu, bildirim ve veri akışları otomatikleştirilir. Ayrıca, temel veri bilimi ve analiz modülleriyle, toplanan verilerden anlamlı içgörüler elde edilmesi hedeflenmektedir. Amaç, sağlık çalışanlarının iş yükünü azaltmak, hasta deneyimini iyileştirmek ve süreçleri standartlaştırmaktır.

## Aktif Ekip Üyeleri

- **Ulaş Pirim**
- **Ahmet Furkan Çayırtepe**
- **Ozan Kalınağaç**

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

## Kullanılan Teknolojiler ve Entegrasyonlar

- **n8n:** Otomasyon akışları (randevu bildirimi, veri akışı, loglama, LLM entegrasyonu)
- **LLM (Büyük Dil Modeli):** n8n üzerinden OpenAI, Gemini veya benzeri LLM API'leri ile semptomlardan otomatik ön değerlendirme ve öneri üretimi
- **Veri Bilimi/Analizi:** Toplanan randevu ve semptom verilerinin temel istatistiksel analizi, görselleştirme ve raporlama
- **Frontend:** React.js (veya benzeri)
- **Backend:** Node.js (Express.js veya benzeri)
- **Veritabanı:** Firebase (MVP için hızlı ve kolay entegrasyon)

## Proje Akışı ve Standup Örnekleri

### Daily Standup Örneği

- **Dün:** Ekip üyeleriyle tanışıldı, proje konusu netleştirildi.
- **Bugün:** MVP için temel özellikler ve iş bölümü yapılacak.
- **Engeller:** Veri bilimi modülü için örnek veri ihtiyacı var.

### Sprint Board

- [ ] Ekip tanışma ve rol paylaşımı
- [ ] Proje fikri ve hedeflerin belirlenmesi
- [ ] n8n otomasyon akışlarının tasarımı
- [ ] LLM modülü entegrasyonu (n8n üzerinden)
- [ ] Veri analizi ve raporlama modülü
- [ ] Web arayüzü taslağı

## Ana Özellikler ve MVP Hedefleri

- **Web Tabanlı Randevu Sistemi:** Hastalar kolayca randevu oluşturabilir.
- **Ön Değerlendirme Modülü:** Girilen semptomlara göre önceliklendirme ve yönlendirme.
- **Otomatik Bildirimler:** n8n ile e-posta/SMS bilgilendirme ve doktorlara otomatik bildirim.
- **LLM Destekli Akıllı Öneriler:** n8n üzerinden LLM API ile semptomlardan otomatik ön değerlendirme ve öneri.
- **Veri Bilimi/Analizi:** Toplanan verilerden temel istatistiksel analiz ve görselleştirme.
- **Yönetici Paneli:** Randevu ve hasta yönetimi için kullanıcı dostu arayüz.

## Mentorler için Notlar

- Proje yönetimi ve ilerleme, Trello üzerinden düzenli olarak takip edilmekte ve raporlanmaktadır.
- n8n ile otomasyon, LLM entegrasyonu ve temel AI modülü MVP'nin ana odak noktasıdır.
- Ekip içi iletişim, şeffaflık ve düzenli raporlama süreç boyunca ön planda tutulmaktadır.
- Veri bilimi/analizi modülüyle, sistemin çıktılarından anlamlı içgörü elde edilmesi hedefleniyor.
- 1 aylık süreçte, temel işlevsellik ve demo odaklı bir MVP çıkarılması planlanıyor.
- Riskler: Gerçek veri eksikliği, LLM API kullanımı, zaman yönetimi.

---

> **Not:** Bu proje, eğitim ve demo amaçlıdır. Gerçek hasta verisiyle çalışırken yasal ve etik kurallara uyulmalıdır.
>>>>>>> b573811cd8baa0ab2372a3e855a6f697723fe649
