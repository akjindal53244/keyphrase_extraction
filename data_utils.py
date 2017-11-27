import collections
from collections import OrderedDict

lines = open("resources/data/social_text_tokenized").readlines()

domain_job_list_map = OrderedDict()

for i, line in enumerate(lines):

    parts = line.strip().split("\t")
    label = parts[0]
    uttr = parts[1]

    f = open("resources/data/docs/" + str(i) + ".txt", "a")
    f.write(uttr)
    f.close()
