from twilio.rest import Client

account_sid = "AC38bdb4986ad46768a555d2728c1fcdf5"
auth_token = "40173d4e0442f1e032bab9b2dbe32e44"

client = Client(account_sid, auth_token)

message = client.messages.create(
    body="Hello Safa, WhatsApp test message 🚀",
    from_="whatsapp:+14155238886",
    to="whatsapp:+91XXXXXXXXXX"
)

print(message.sid)
