
# This is used to create a unique channel for a chat
def get_chat_room_name(user1, user2):

    users = sorted([user1.id, user2.id])
    return f"chat_{users[0]}_{users[1]}"
