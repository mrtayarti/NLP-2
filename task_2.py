from nltk.corpus import wordnet as wn
from itertools import product
import os.path
from nltk.tokenize import RegexpTokenizer
import nltk.data
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords

lemmatizer = WordNetLemmatizer()


def read_file(path):  # read the file and split it into list
    with open(path, "r") as file:
        return file.read()


list_data = (read_file('text1.txt'))
list_data = list_data.lower()  # lower all the words
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

clean_text = " ".join([lemmatizer.lemmatize(i) for i in list_data.split()])  # lemmatize the words

index, x = 0, 0
clean_text = (clean_text.split())
for outer in clean_text:  # loop to clean the text by replacing with meaningful connection
    if x == 0:
        for inner in clean_text:
            clean_text[index] = clean_text[index].replace('--', " ")
            index += 1
    index = 0
    if x == 1:
        for inner in clean_text:
            clean_text[index] = clean_text[index].replace('-', "")
            index += 1
    index = 0
    if x == 2:
        for inner in clean_text:
            clean_text[index] = clean_text[index].replace('_', " ")
            index += 1
    x += 1

clean_text = ' '.join(clean_text)
tokenizer = RegexpTokenizer(r'\w+')
list_word = []
clean_text = tokenizer.tokenize(clean_text)
clean_text = list(dict.fromkeys(clean_text))
clean_text = [word for word in clean_text if word not in stopwords.words('english')] # apply the stopword
index_del = 0
for index in clean_text:
    if len(index) == 1:
        clean_text.remove(index)
    if index == "ha" or index == "wer" or index == "wa":  # remove the words that have no meaning after clean the text the words like was becomes wa | has become ha
        del clean_text[index_del]
    index_del += 1

for index in clean_text:
    list_word.append(tokenizer.tokenize(index))

list_similarity, cleaned_w1, cleaned_w2 = [], [], []

for index in list_word:
    cleaned_w1.append(index)
    cleaned_w2.append(index)

w1_list, w2_list = [], []
cleaned_w1 = [item for sublist in cleaned_w1 for item in sublist]
cleaned_w2 = [item for sublist in cleaned_w2 for item in sublist]

for index_word1 in cleaned_w1:  # loop in loop to cross check all the senses of the word1 and word2 to get the maximum path similarity
    for index_word2 in cleaned_w2:
        if index_word1 != index_word2:
            w1_list.append(index_word1)
            w2_list.append(index_word2)
            w1 = [index_word1]
            w2 = [index_word2]
            list_w1 = set(w for word in w1 for w in wn.synsets(word)) # get the senses into list
            list_w2 = set(w for word in w2 for w in wn.synsets(word)) # get the senses into list
            if list_w1 and list_w2:
                max_similarity = max(
                    (wn.path_similarity(w1, w2) or 0.0, w1, w2) for w1, w2 in product(list_w1, list_w2))
                list_similarity.append(max_similarity[0])
            else:
                list_similarity.append(0.0)

predicted_list = "word1\tword2\tSimilarity\n"  # add the header
word_index = 0
for index in list_similarity:  # loop to add information to the list
    predicted_list += (w1_list[word_index])
    predicted_list += "\t"
    predicted_list += (w2_list[word_index])
    predicted_list += "\t"
    predicted_list += str(index)
    predicted_list += "\n"
    word_index += 1

save_path = 'original-pairs.txt'
if os.path.exists(save_path):
    update_file = open(save_path, 'w')
else:
    update_file = open(save_path, 'x')
    update_file = open(save_path, 'w')
update_file.write(predicted_list)
print(predicted_list)
