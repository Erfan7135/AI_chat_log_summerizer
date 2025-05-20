


def main():
    chat = 'logs/chat1.txt'
    try:
        with open(chat, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"File {chat} not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

if __name__ == "__main__":
     main()