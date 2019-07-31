import re
from nltk.corpus import wordnet as wn
import os.path
from itertools import product


def read_txt(file_path):
    with open(file_path, "r") as file:
        return [re.split("\s+", line.rstrip('\n')) for line in file]


list_data = (read_txt("original-pairs.txt"))
del list_data[0]  # delete the header
given_w1, given_w2, list_words, hypernym_1, hypernym_2, list_hyp1, list_hyp2, list_similarity = [], [], [], [], [], [], [], []

for index in list_data:
    given_w1.append(index[0])
    given_w2.append(index[1])
    list_words.append(index[2])

index = 0
for hypernyms in given_w1: # loop to get the hypernym of each word by getting the sense and pick the 1st sense and get the first hypernym of that sense
    hypernym_1 = wn.synsets(given_w1[index])
    hypernym_2 = wn.synsets(given_w2[index])
    if hypernym_1:
        hypernym_1 = hypernym_1[0].hypernyms()
        if hypernym_1:
            hypernym_1 = hypernym_1[0].lemma_names()
            list_hyp1.append(hypernym_1[0])
    if hypernym_2:
        hypernym_2 = hypernym_2[0].hypernyms()
        if hypernym_2:
            hypernym_2 = hypernym_2[0].lemma_names()
            list_hyp2.append(hypernym_2[0])
    if not hypernym_1:
        list_hyp1.append("None") # if the word1 has no hypernym it will return None
    if not hypernym_2:
        list_hyp2.append("None") # if the word2 has no hypernym it will return None
    index += 1

index_w2 = 0
for index_w1 in list_hyp1:  # loop in loop to cross check all the senses of the word1 and word2 to get the maximum path similarity
    w1 = [index_w1]
    w2 = [list_hyp2[index_w2]]
    if w1 != ["None"] and w2 != ["None"]:
        list_w1 = set(w for word in w1 for w in wn.synsets(word))
        list_w2 = set(w for word in w2 for w in wn.synsets(word))
        if list_w1 and list_w2:
            max_similarity = max((wn.path_similarity(w1, w2) or 0.00, w1, w2) for w1, w2 in product(list_w1, list_w2))
            list_similarity.append(max_similarity[0])
    else:
        list_similarity.append(0.00)
    index_w2 += 1

word_index = 0
predicted_list = "word1\tword2\tSimilarity1\thyp1\thyp2\tSimilarity2\n"  # add the header
for index in list_similarity:  # loop to add information to the list
    predicted_list += (given_w1[word_index])
    predicted_list += "\t"
    predicted_list += (given_w2[word_index])
    predicted_list += "\t"
    predicted_list += (list_words[word_index])
    predicted_list += "\t"
    predicted_list += (list_hyp1[word_index])
    predicted_list += "\t"
    predicted_list += (list_hyp2[word_index])
    predicted_list += "\t"
    if not index:
        predicted_list += '0.00'
    else:
        predicted_list += str(index)
    predicted_list += "\n"
    word_index += 1

save_path = 'original-pairs-hypernyms.txt'
if os.path.exists(save_path):
    update_file = open(save_path, 'w')
else:
    update_file = open(save_path, 'x')
    update_file = open(save_path, 'w')
update_file.write(predicted_list)
print(predicted_list)
