import poplib
from email import parser
from email.header import decode_header
from email.utils import parsedate_to_datetime

def decode_mime_words(s):
    if not s:
        return ''
    decoded_segments = []
    for word, charset in decode_header(s):
        try:
            if charset:
                decoded_segments.append(word.decode(charset, errors='ignore'))
            elif isinstance(word, bytes):
                decoded_segments.append(word.decode('utf-8', errors='ignore'))
            else:
                decoded_segments.append(word)
        except:
            decoded_segments.append(str(word))
    return ''.join(decoded_segments)

def fetch_emails(email, password, server='qasid.iitk.ac.in', port=995, limit=50):
    try:
        connection = poplib.POP3_SSL(server, port)
        connection.user(email)
        connection.pass_(password)
        num_messages = len(connection.list()[1])

        if limit is None:
            indices = range(1, num_messages + 1)
        else:
            indices = range(num_messages, max(num_messages - limit, 0), -1)

        messages = []
        for i in indices:
            try:
                response, lines, octets = connection.top(i, 0)
                msg = parser.BytesParser().parsebytes(b'\r\n'.join(lines))
                messages.append({
                    'msg_num': i,
                    'subject': decode_mime_words(msg.get("Subject", "")),
                    'sender': decode_mime_words(msg.get("From", "")),
                    'date': parsedate_to_datetime(msg.get("Date", "")) if msg.get("Date") else None
                })
            except Exception as e:
                print(f"[!] Error parsing email {i}: {e}")
                continue

        connection.quit()
        return messages

    except Exception as e:
        print(f"[!] Connection error: {e}")
        return []
