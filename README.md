# Veridra: Yapay Zeka Tabanlı Kişisel Asistan Projesi (V1.0)

Bu çalışma, Google Gemini API altyapısı kullanılarak Streamlit framework'ü üzerinde geliştirilmiş bir kişisel asistan uygulamasıdır. Proje; yapay zeka entegrasyonu, veri kalıcılığı ve yerel güvenlik protokollerinin uygulanması odaklı hazırlanmıştır.

## Teknik Özellikler

* **Güvenlik Katmanı (Gizli Kasa):** Hassas verilerin ve sohbetlerin korunması amacıyla geliştirilen, kullanıcı tanımlı şifre kontrol mekanizması.
* **Veri Yönetimi ve Hafıza:** JSON formatında yapılandırılmış yerel veritabanı entegrasyonu ile geçmiş oturum verilerinin korunması ve sürekliliğin sağlanması.
* **Etkileşim Modelleri:** Kullanıcı ihtiyacına göre özelleştirilmiş farklı kişilik algoritmaları (Eğitmen ve Destek modları).
* **Görüntü İşleme Kapasitesi:** Vision modelleri üzerinden görsel verilerin analizi ve metinsel raporlanması.

## Kullanılan Teknolojiler

* **Programlama Dili:** Python
* **Arayüz Framework:** Streamlit
* **Yapay Zeka Modeli:** Google Gemini 2.5 Flash
* **Veri Saklama:** JSON (Local File System)

## Geliştirme Süreci ve Karşılaşılan Zorluklar

Bu proje geliştirilirken özellikle **JSON tabanlı veri yönetimi** aşamasında, verilerin her oturumda hata vermeden güncellenmesi ve üzerine yazılması konusunda mantıksal zorluklarla karşılaşılmıştır. Bu sorunlar, Python'daki dosya işleme (file handling) protokolleri optimize edilerek ve hata yakalama (exception handling) blokları güçlendirilerek çözülmüştür. Ayrıca Streamlit arayüzünün kullanıcı deneyimini artıracak şekilde özelleştirilmesi üzerine teknik çalışmalar yapılmıştır.

## Proje Amacı
Aydın Adnan Menderes Üniversitesi, Robotik ve Yapay Zeka bölümü öğrencisi olarak bu projeyi; karmaşık sistem mimarilerini uçtan uca tasarlama, API optimizasyonu ve güvenli veri depolama süreçlerini profesyonel standartlarda yönetme yetkinliği kazanmak amacıyla geliştirdim.
