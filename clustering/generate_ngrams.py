token_lines = open("/home/asjindal/Work/tf/keyword_extraction/resources/data/TrainData_tokenized_lemma", "r").readlines()

token_freq_map = dict()
bigram_freq_map = dict()


def load_stop_words(stop_word_file):
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def get_freq_words():

    stop_word_file = "../resources/CombinedStopList"
    stop_words = load_stop_words(stop_word_file)

    for i, line in enumerate(token_lines):
        jd = line.strip().split("\t")[0].lower()
        tokens = jd.split(" ")

        tokens_2gram = [" ".join(tokens[i:i+2]) for i in range(len(tokens)-1) if " ".join(tokens[i:i+2]) not in stop_words]
        tokens_3gram = [" ".join(tokens[i:i + 3]) for i in range(len(tokens) - 2) if " ".join(tokens[i:i+3]) not in stop_words]


        for token in tokens:
            if token not in token_freq_map:
                token_freq_map.setdefault(token, 0)
            token_freq_map[token] += 1

        for bigram in tokens_2gram:
            if bigram not in bigram_freq_map:
                bigram_freq_map.setdefault(bigram, 0)
            bigram_freq_map[bigram] += 1

    sorted_word_freq = sorted(token_freq_map.items(), key=lambda x: x[1])[::-1]
    sorted_bigram_freq = sorted(bigram_freq_map.items(), key=lambda x: x[1])[::-1]

    freq_words = dict(sorted_word_freq[:480]).keys()
    return freq_words

get_freq_words()