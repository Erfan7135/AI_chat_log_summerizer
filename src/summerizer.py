import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

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

def keyword_analysis(messages):
    custom_stop_words = ['hi', 'hello', 'hey', 'ok', 'okay', 'yes', 'no', 'sure', 'thanks', 'thank you', 'please', 'tell', 'ask']
    stop_words = set(stopwords.words('english')).union(set(custom_stop_words))
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

    # count the frequency of each word
    word_counts = Counter(all_words)
    # get the most common words
    most_frequent = word_counts.most_common()
    return most_frequent
    

def tfidf_analysis(messages):
    stop_words = list(stopwords.words('english'))

    docs = [message['content'].lower() for message in messages]
    vectorizer = TfidfVectorizer(
        stop_words=stop_words, 
        token_pattern=r'(?u)\b[a-zA-Z]+\b', # only alphabetic words
    )

    tfidf_matrix = vectorizer.fit_transform(docs)
    feature_names = vectorizer.get_feature_names_out()

    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    word_scores = {word: score for word, score in zip(feature_names, tfidf_scores)}

    return sorted(word_scores.items(), key=lambda x: x[1], reverse=True)

def most_common_words(messages):
    # messages =[ msg for msg in messages if msg['speaker'] == 'User']
    frequncy = keyword_analysis(messages)
    tfidf = tfidf_analysis(messages)
    # print(frequncy)
    # print(tfidf)
    aggregated_results = {}
    tfidf_dict = {word: score for word, score in tfidf}
    # aggregate the results
    for word, count in frequncy:
        if word in tfidf_dict:
            #get the tfidf score for the word
            tfidf_score = tfidf_dict[word]
            # square ensures that the frequency has a greater impact on the score
            # and add the tfidf score to it as tie breaker
            aggregated_results[word] = (count**2)+tfidf_score
            # print(f"Word: {word}, Frequency: {count}, TF-IDF Score: {tfidf_score}, Aggregated Score: {aggregated_results[word]}")
    
    # print("Aggregated results:", aggregated_results)
    sorted_results = sorted(aggregated_results.items(), key=lambda x: x[1], reverse=True)
    sorted_results = [word for word, score in sorted_results]
    print("Most common words:", sorted_results)

def main():
    chat_path = 'logs/chat2.txt'
    messages = parse_chat(chat_path)
    # print(messages)
    stats = message_statistics(messages)
    # print(stats)
    # most_common = keyword_analysis(messages)
    # # most_common = tfidf_analysis(messages)
    # print("Most common keywords:",most_common)
    most_common_words(messages)

if __name__ == "__main__":
    main()