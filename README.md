# E-posta Kimlik Avı Tespit Aracı

Bu araç, e-posta trafiğindeki kimlik avı (phishing) girişimlerini tespit etmeyi amaçlar. E-postaları tarayarak tehlikeli kelimeleri, bağlantıları ve dosya eklerindeki tehlikeli uzantıları kontrol eder. Kullanıcıya uyarı vererek zararlı etkilerin önlenmesini sağlar.

## Kullanım

- `config.py` dosyasında IMAP sunucu bilgilerinizi ve uyarı e-postası göndermek istediğiniz adresi ayarlayın.
- `main.py` dosyasını çalıştırarak programı başlatın.
- Program, e-posta kutunuzu düzenli aralıklarla kontrol edecek ve tehlikeli e-postaları tespit ederek uyarı verecektir.

## Kullanılan Kütüphaneler

- `imaplib`: IMAP protokolü üzerinden e-posta işlemleri yapmak için kullanılır.
- `email`: E-posta mesajlarını işlemek için kullanılır.
- `yagmail`: E-posta göndermek için kullanılır.
- `winsound`: Windows işletim sistemi üzerinde ses çalma işlemleri yapmak için kullanılır.
- `re`: Düzenli ifadeleri kullanarak metin işlemleri yapmak için kullanılır.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakabilirsiniz.
