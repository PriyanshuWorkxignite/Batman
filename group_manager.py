from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

class GroupManager:
    @staticmethod
    async def load_groups(client):
        """Load all groups from an account"""
        try:
            groups = []
            dialogs = await client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=InputPeerEmpty(),
                limit=200,
                hash=0
            ))

            for dialog in dialogs.dialogs:
                try:
                    entity = dialog.peer
                    
                    if hasattr(entity, 'channel_id'):
                        # Channel or supergroup
                        chat_title = None
                        for chat in dialogs.chats:
                            if hasattr(chat, 'id') and chat.id == entity.channel_id:
                                chat_title = chat.title
                                break
                        
                        if chat_title:
                            groups.append({
                                'id': entity.channel_id,
                                'title': chat_title,
                                'type': 'channel',
                                'entity': entity
                            })
                    
                    elif hasattr(entity, 'chat_id'):
                        # Basic group
                        chat_title = None
                        for chat in dialogs.chats:
                            if hasattr(chat, 'id') and chat.id == entity.chat_id:
                                chat_title = chat.title
                                break
                        
                        if chat_title:
                            groups.append({
                                'id': entity.chat_id,
                                'title': chat_title,
                                'type': 'group',
                                'entity': entity
                            })
                    
                    elif hasattr(entity, 'user_id'):
                        # Skip private chats
                        pass
                
                except Exception as e:
                    print(f"Error processing dialog: {e}")
                    continue

            return groups

        except Exception as e:
            print(f"Error loading groups: {e}")
            return []

    @staticmethod
    async def send_message(client, group_entity, message):
        """Send message to a group"""
        try:
            await client.send_message(group_entity, message)
            return True, "Message sent successfully"
        except Exception as e:
            return False, f"Error sending message: {str(e)}"

# Global group manager
group_manager = GroupManager()
