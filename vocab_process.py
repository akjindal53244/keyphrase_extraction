token_lines = open("/home/asjindal/Work/tf/keyword_extraction/resources/data/social_text_tokenized_lemma", "r").readlines()

token_freq_map = dict()
bigram_freq_map = dict()


def get_freq_words():
    for i, line in enumerate(token_lines):
        # print i
        jd = line.strip().split("\t")[1].lower()

        tokens = jd.split(" ")

        tokens_2gram = [" ".join(tokens[i:i+2]) for i in range(len(tokens)-1)]
        # tokens.extend(tokens_2gram)
        #
        # tokens = tokens_2gram

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

    freq_words = dict(sorted_word_freq[:50]).keys()
    return freq_words

get_freq_words()