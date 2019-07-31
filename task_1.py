from nltk.corpus import wordnet as wn
from itertools import product
import re
import os.path


def read_file(path):  # read the file and split it into list
    with open(path, "r") as file:
        return [re.split("\s+", line.rstrip('\n')) for line in file]


list_data = (read_file('SimLex999-100.txt'))
del list_data[0]  # delete the header
given_w1, given_w2, gold_similarity, list_similarity = [], [], [], []

for index in list_data:  # get w1, w2 in the lists along with the old similarity
    given_w1.append(index[0])
    given_w2.append(index[1])
    gold_similarity.append(index[2])

index_w2 = 0
for index_w1 in given_w1:  # loop to check the senses of words and cross check the path similarity to get the maximum ones
    w1 = [index_w1]
    w2 = [given_w2[index_w2]]
    list_w1 = set(ss for word in w1 for ss in wn.synsets(word))
    list_w2 = set(ss for word in w2 for ss in wn.synsets(word))
    if list_w1 and list_w2:
        max_similarity = max((wn.path_similarity(w1, w2) or 0.00, w1, w2) for w1, w2 in product(list_w1, list_w2))
        list_similarity.append(max_similarity[0])
    index_w2 += 1

word_index = 0
predicted_list = "word1\tword2\tGoldSimilarity\tWordNetSimiliarity\n"
for index in list_similarity:  # loop to add information to the list
    predicted_list += (given_w1[word_index])
    predicted_list += "\t"
    predicted_list += (given_w2[word_index])
    predicted_list += "\t"
    predicted_list += (gold_similarity[word_index])
    predicted_list += "\t"
    predicted_list += str(index)
    predicted_list += "\n"
    word_index += 1

save_path = 'BioSim-100-predicted.txt'

if os.path.exists(save_path):  # check if file exists
    update_file = open(save_path, 'w')  # if yes set the overwrite
else:
    update_file = open(save_path, 'x')  # if no create it
    update_file = open(save_path, 'w')  # and set the overwrite
update_file.write(predicted_list)  # overwrite the information from the list to the file
print(predicted_list)
