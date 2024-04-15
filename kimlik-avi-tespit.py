import imaplib
import email
import yagmail
import winsound
import time
import re

# IMAP sunucu bilgileri
IMAP_SERVER = "imap.sunucunuz.com"  # Örneğin: "imap.gmail.com"
IMAP_PORT = 993
IMAP_USERNAME = "email@adresiniz.com"  # E-posta adresinizi buraya girin
IMAP_PASSWORD = "sifreniz"  # E-posta şifrenizi buraya girin

# Mail bilgileri
MAIL_TO = "bildirim@alacakemail.com"  # Bildirim almak istediğiniz e-posta adresini buraya girin
subject = "Tehdit İçeren E-posta Uyarısı"
body = "Tehdit içeren bir e-posta tespit edildi. Lütfen dikkatli olun."

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" not in content_disposition and "text/plain" in content_type:
                return part.get_payload(decode=True).decode()
    else:
        return msg.get_payload(decode=True).decode()

def contains_dangerous_words_or_links(email_content):
    dangerous_words = ["recorded you", "seni kaydettim", "kimlik bilgilerin bende"]
    if any(word in email_content.lower() for word in dangerous_words):
        return True

    # E-posta içindeki linkleri kontrol ediyor
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
    if links:
        return True

    return False

previous_email_id = None
reset_interval = 60  # Önceki email ID'sini sıfırlamak için beklenen süre (saniye cinsinden)
last_reset_time = time.time()

while True:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(IMAP_USERNAME, IMAP_PASSWORD)
    mail.select("inbox")

    status, email_ids = mail.search(None, "ALL")
    latest_email_id = email_ids[0].split()[-1]

    if previous_email_id == latest_email_id:
        time.sleep(10)
        continue

    status, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    email_body = get_email_body(msg)

    if contains_dangerous_words_or_links(email_body):
        yag = yagmail.SMTP(IMAP_USERNAME, IMAP_PASSWORD)
        yag.send(to=MAIL_TO, subject=subject, contents=body)
        print("Olasi Kimlik Avi Tespit Edildi")
        winsound.Beep(1500, 400)
        time.sleep(0.1)
        winsound.Beep(1500, 400)
        time.sleep(0.1)
        winsound.Beep(1500, 400)
        # E-postayı Spam klasörüne taşıma
        mail.store(latest_email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
        mail.select("[Gmail]/Spam")
        mail.append("[Gmail]/Spam", '', imaplib.Time2Internaldate(time.time()), raw_email)
        
    previous_email_id = latest_email_id
    if time.time() - last_reset_time > reset_interval:
        previous_email_id = None
        last_reset_time = time.time()

    time.sleep(5)
