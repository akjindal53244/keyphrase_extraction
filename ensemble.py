from vocab_process import get_freq_words
import collections

freq_unigrams = get_freq_words()


def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i + n]) for i in xrange(len(lst) - n + 1))


def add_all_words_position(i, keyphrase_freq_map, words):
    for j, word in enumerate(words):
        if word not in keyphrase_freq_map[i]:
            keyphrase_freq_map[i].setdefault(word, 0.)
        keyphrase_freq_map[i][word] += float(len(words) - j)
    return keyphrase_freq_map


def add_all_words_freq(i, keyphrase_freq_map, words):
    for j, word in enumerate(words):
        if word not in keyphrase_freq_map[i]:
            keyphrase_freq_map[i].setdefault(word, 0.)
        keyphrase_freq_map[i][word] += 1
    return keyphrase_freq_map


def retain_only_superphrase(word_list):
    redundant_indices = set()
    for idx, word_str1 in enumerate(word_list):
        if idx not in redundant_indices:
            for jdx, word_str2 in enumerate(word_list):
                if idx != jdx and jdx not in redundant_indices:
                    big_list = word_str1.lower().split(" ")
                    small_list = word_str2.lower().split(" ")
                    if contains_sublist(big_list, small_list):
                        redundant_indices.add(jdx)

    word_list = [word_list[idx] for idx in range(len(word_list)) if idx not in redundant_indices]
    return word_list


def remove_redundant_subphrases(word_list):
    redundant_indices = set()
    for idx in range(len(word_list) - 1, -1, -1):
        if idx not in redundant_indices:
            for j in range(idx - 1, -1, -1):
                if j not in redundant_indices:
                    small_list = word_list[idx].lower().split(" ")
                    big_list = word_list[j].lower().split(" ")
                    if contains_sublist(big_list, small_list):
                        redundant_indices.add(idx)
                        break

    word_list = [word_list[idx] for idx in range(len(word_list)) if idx not in redundant_indices]
    return word_list


def remove_freq_unigrams(word_list, lemma_list):
    word_list = [word for (word, lemma) in zip(word_list, lemma_list) if lemma.lower() not in freq_unigrams]
    return word_list


def apply_filters(word_list, lemma_list):
    word_list = remove_freq_unigrams(word_list, lemma_list)
    # word_list = remove_redundant_subphrases(word_list)
    word_list = retain_only_superphrase(word_list)
    return word_list


def ensemble_predictions():
    # rake_lines = open("resources/data/social_text_tokenized_rake_filtered_all",
    #                   "r").readlines()
    topic_rank_lines = open(
        "resources/data/social_text_tokenized_pos_topicrank_filtered_all",
        "r").readlines()
    kp_miner_lines = open(
        "resources/data/social_text_tokenized_pos_kpminer_filtered_all",
        "r").readlines()

    ensemble_phrases_f = open(
        "resources/data/social_text_tokenized_pos_ensemble_filtered_topic_kpminer", "w")

    keyphrase_freq_map = dict()

    for i, (topic_line, kpminer_line) in enumerate(zip(topic_rank_lines, kp_miner_lines)):
        print i

        keyphrase_freq_map.setdefault(i, dict())

        # rake_words = rake_line.strip().split(" , ")
        topic_rank_words = topic_line.strip().split(" , ")
        kpminer_words = kpminer_line.strip().split(" , ")

        min_length = min(len(topic_rank_words), len(kpminer_words))

        # keyphrase_freq_map = add_all_words_pos(i, keyphrase_freq_map, rake_words[:min_length])
        keyphrase_freq_map = add_all_words_position(i, keyphrase_freq_map, topic_rank_words)
        keyphrase_freq_map = add_all_words_position(i, keyphrase_freq_map, kpminer_words)

        if len(keyphrase_freq_map[i]) > 0:
            sorted_word_freq = sorted(keyphrase_freq_map[i].items(), key=lambda x: x[1])[::-1]

            top_k_ensembled_phrases = sorted_word_freq[:min(10, len(sorted_word_freq))]
            top_k_words = list(zip(*top_k_ensembled_phrases)[0])
            top_k_words = retain_only_superphrase(top_k_words)
            ensemble_phrases_f.write(" , ".join(top_k_words[:min(5, len(top_k_words))]).strip().lower() + "\n")

        else:
            ensemble_phrases_f.write("\n")

        print "A"

    ensemble_phrases_f.close()


ensemble_predictions()
