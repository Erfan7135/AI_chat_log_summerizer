import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

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

def keyword_analysis(messages, top_n=5):
    stop_words = set(stopwords.words('english'))
    all_words = []

    for message in messages:
        # tokenize the content of each message
        words = word_tokenize(message['content'].lower())
        # remove punctuation and non-alphabetic characters
        words = [word for word in words if word.isalpha()]
        # remove stop words
        words = [word for word in words if word not in stop_words]
        # add to the list of all words
        all_words.extend(words)

    print(all_words)
    # count the frequency of each word
    word_counts = Counter(all_words)
    # get the most common words
    most_common = word_counts.most_common(top_n)
    ### use textrank to better common words
    most_common_words = ', '.join(word for word, count in most_common)
    return most_common_words
    

def main():
    chat_path = 'logs/chat1.txt'
    messages = parse_chat(chat_path)
    # print(messages)
    stats = message_statistics(messages)
    # print(stats)
    most_common = keyword_analysis(messages)
    print("Most common keywords:",most_common)

if __name__ == "__main__":
    main()