

def parse_chat(chat_path):

    # messages = []
    messages = []
    try:
        with open(chat_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # print(lines)
            # doesn't work if multiple lines in content
            for line in lines:
                speaker, content = line.split(':', 1)
                messages.append({
                    'speaker': speaker.strip(),
                    'content': content.strip()
                })
            return messages
    except FileNotFoundError:
        print(f"File {chat_path} not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def message_statistics(messages):
    total = len(messages)
    user_count = 0
    ai_count = 0
    for message in messages:
        if message['speaker'] == 'User':
            user_count += 1
        elif message['speaker'] == 'AI':
            ai_count += 1
    stats = {
        'total_messages': total,
        'user_messages': user_count,
        'ai_messages': ai_count
    }
    return stats

def main():
    chat_path = 'logs/chat1.txt'
    messages = parse_chat(chat_path)
    # print(messages)
    stats = message_statistics(messages)
    print(stats)

if __name__ == "__main__":
    main()