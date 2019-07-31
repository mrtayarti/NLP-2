import os.path
import random
import re
import operator


def read_txt(file_path):
    with open(file_path, "r") as file:
        return [re.split("\s+", line.rstrip('\n')) for line in file]


list_data = (read_txt('original-pairs.txt'))
del list_data[0] # delete the header
list_data = random.sample(list_data, len(list_data))  # shuffle the order in the list
get_index = []

for i in list_data: # loop to add only similarity to the list to use on the loop below
    similar = float(i[2])
    get_index.append([similar])

path_index = []
counter = 0
while counter < 10: # loop ten times
    top = (max(enumerate(get_index), key=operator.itemgetter(1))) # to get the index of list then contains maximum similarity
    num = top[0]
    path_index.append(num)
    get_index[path_index[counter]] = [0]
    counter += 1

update_prediction = "word1\tword2\tSimilarity\n"  # add the header
counter = 0
for i in path_index: # loop to add information to the list
    top_index = path_index[counter]
    word_s = '\t'.join(list_data[top_index])
    update_prediction += word_s
    update_prediction += "\n"
    counter += 1

save_path = 'top.txt'
if os.path.exists(save_path):
    update_file = open(save_path, 'w')
else:
    update_file = open(save_path, 'x')
    update_file = open(save_path, 'w')
update_file.write(update_prediction)
print(update_prediction)
