from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from telethon.tl.functions.channels import InviteToChannelRequest

## CONSTANTS
API_ID = 14910831
API_HASH = "1b42db34f9419ad906054425a07ac38b"
TELEPHONE_NUMBER = "+447957253805"
GROUP = 'Lightningtipss'
MESSAGE = f"""
Join our free group for Football tips, we aim for 70/80% strike rate per month! 
Here is our group > https://t.me/{GROUP}
"""

## GLOBAL VARIABLES
client = TelegramClient('session', API_ID, API_HASH)
visited_members = []
channels = []

client.connect()
if not client.is_user_authorized():
    client.send_code_request(TELEPHONE_NUMBER)
    client.sign_in(TELEPHONE_NUMBER, input("Enter Login Code: "))
    
def loadChannels():
    for channel in client.get_dialogs():
        if channel.is_channel:
            channels.append(channel.entity)
    print(channels)

def sendMessages():
    for channel in channels:
        for member in client.get_participants(channel):
            if member in visited_members:
                continue
            member_entity = client.get_entity(InputPeerUser(member.id, member.access_hash))
            try:
                client.send_message(entity=member_entity, message=MESSAGE)
                client(InviteToChannelRequest(client.get_entity(GROUP), [member_entity]))
                print("Sent Invite !")
            except Exception:
                pass

            visited_members.append(member)

loadChannels()
sendMessages()