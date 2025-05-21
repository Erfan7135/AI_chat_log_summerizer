import os
import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
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
            current_speaker = None
            current_content = []
            for line in lines:
                if line.startswith('User:') or line.startswith('AI:'):
                    #save the previoud message if it exists
                    if current_speaker and current_content:
                        messages.append({
                            'speaker': current_speaker,
                            'content': ' '.join(current_content).strip()
                        })
                        current_speaker = None
                        current_content = []
                    # reset for new message
                    speaker, content = line.split(':', 1)
                    current_speaker = speaker.strip()
                    current_content .append(content.strip())
                    
                else:
                    # if line doesn't start with User: or AI:, it's part of the content
                    if current_speaker:
                        current_content.append(line.strip())

            # save the last message if it exists
            if current_speaker and current_content:
                messages.append({
                    'speaker': current_speaker,
                    'content': ' '.join(current_content).strip()
                })

            # print(messages)
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
    # print("Sorted results:", sorted_results)
    return sorted_results

def gen_summery(file_path):
    chat_path = file_path
    messages = parse_chat(chat_path)
    stats = message_statistics(messages)
    keywords = most_common_words(messages)
    # print(keywords)

    ## template base summery using the first keyword
    ## Can be improved by using a more sophisticated model or API
    summary_text = f"This conversation is about {keywords[0]}.\n"
    keywords = ', '.join(word for word in keywords[:5])

    # create a new file with same name and .txt extension in a different directory
    #remove logs/ & add output/ to the path
    output_path = chat_path.replace('logs/', 'output/').replace('.txt', '_summary.txt')
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(f"The Conversation had {stats['total_messages']} exchanges.\n")
            file.write(summary_text)
            file.write(f"Most common keywords: " + keywords + "\n")
            
        print(f"Summary saved to {output_path}")
    except Exception as e:
        print(f"An error occurred while saving the summary: {e}")

def main():
    # chat_path = 'logs/chat2.txt'
    # gen_summery(chat_path)

    current_dir = os.getcwd()
    for file in os.listdir(os.path.join(current_dir, 'logs')):
        if file.endswith('.txt'):
            chat_path = 'logs/' + file
            gen_summery(chat_path)

if __name__ == "__main__":
    main()