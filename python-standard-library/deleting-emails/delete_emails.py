import imaplib
import email
from email.header import decode_header

# Измените учетные данные
username = "youremailaddress@provider.com"
password = "yourpassword"

# создать класс IMAP4 с SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# аутентификация
imap.login(username, password)

# выберите почтовый ящик, в котором надо удалить письма
# если вам нужен SPAM, используйте вместо него imap.select("SPAM")
imap.select("INBOX")

# поиск определенных писем по отправителю
status, messages = imap.search(None, 'FROM "googlealerts-noreply@google.com"')

# чтобы получить все письма:
# status, messages = imap.search(None, "ALL")

# для получения писем по теме
# status, messages = imap.search(None, 'SUBJECT «Спасибо за подписку на нашу рассылку!»')

# для получения писем после определенной даты
# status, messages = imap.search(None, ''SINCE "01-JAN-2020"')

# для получения писем до определенной даты
# status, messages = imap.search (Нет, 'BEFORE "01-JAN-2020"')
# преобразовать сообщения в список адресов электронной почты 
messages = messages[0].split(b' ')
for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
        # если у вас длинный список писем, то можно удалить цикл for для повышения производительности
        # потому что он предназначен только для Subject цэлектронных писем для удаления
        for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # декодирование темы email
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # если это байтовый тип, декодировать в str
                subject = subject.decode()
            print("Deleting", subject)
    # отметить письмо как удаленное
    imap.store(mail, "+FLAGS", "\\Deleted")
# навсегда удалить письма, помеченные как удаленные
# из выбранного почтового ящика (в нашем случае INBOX)
imap.expunge()
# закрыть email
imap.close()
# выйти из аккаунта
imap.logout()
