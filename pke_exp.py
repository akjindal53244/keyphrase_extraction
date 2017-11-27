import pke
from joblib import Parallel, delayed
import multiprocessing
from rake import Rake
from vocab_process import get_freq_words
from pke import TopicRank, KPMiner
from ensemble import apply_filters

# from ensemble import ensemble_predictions
num_cores = multiprocessing.cpu_count()
chunk_size = 11000
core_id = 4
offset = 5230

preprocessed_lines = open("resources/data/social_text_tokenized_pos", "r").readlines()
rake_data_lines = open("resources/data/social_text_tokenized", "r") \
    .readlines()
lemma_lines = open("resources/data/social_text_tokenized_lemma",
                   "r").readlines()

rake = Rake("resources/CombinedStopList")
#rake_out_f = open("resources/data/social_text_tokenized_rake_filtered_" + str(core_id + 1), "a")
topic_rank_out_f = open("resources/data/social_text_tokenized_pos_topicrank_filtered_" + str(core_id + 1), "a")
kpminer_out_f = open("resources/data/social_text_tokenized_pos_kpminer_filtered_" + str(core_id + 1), "a")

input_file_path = "resources/sample_jd_preprocessed"
meta_file_path = "resources/sample_jd_meta_data"

freq_unigrams = get_freq_words()

new_preprocessed_lines = preprocessed_lines[
                         chunk_size * core_id + offset: min(len(preprocessed_lines), chunk_size * (core_id + 1))]
new_rake_data_lines = rake_data_lines[
                      chunk_size * core_id + offset: min(len(rake_data_lines), chunk_size * (core_id + 1))]
new_lemma_lines = lemma_lines[chunk_size * core_id + offset: min(len(lemma_lines), chunk_size * (core_id + 1))]

total_lines = len(lemma_lines)

"""
def get_keyphrases(core_id):
    new_preprocessed_lines = preprocessed_lines[
                             chunk_size * core_id: min(len(preprocessed_lines), chunk_size * (core_id + 1))]
    new_rake_data_lines = rake_data_lines[chunk_size * core_id: min(len(rake_data_lines), chunk_size * (core_id + 1))]
    new_lemma_lines = lemma_lines[chunk_size * core_id: min(len(lemma_lines), chunk_size * (core_id + 1))]


    for i, (preprocessed_line, rake_raw_line, lemma) in enumerate(zip(new_preprocessed_lines, new_rake_data_lines,
                                                                      new_lemma_lines)):

        if i >= 0:
            print i
            parts = preprocessed_line.strip().split("\t")
            jd_pos = parts[1]

            parts = rake_raw_line.strip().split("\t")
            jd = parts[1]

            # f = open(input_file_path, "w")
            # f.write(jd_pos)
            # f.close()

            # f = open(meta_file_path, "w")
            # f.write(title.strip())
            # f.close()

            raw_words = jd.split(" ")
            lemma_words = lemma.strip().split(" ")

            word_lemma_map = dict()

            if len(raw_words) == len(lemma_words):
                [word_lemma_map.setdefault(word, lemma) for (word, lemma) in zip(raw_words, lemma_words)]
            else:
                "Error!"

            # =========Rake=======
            rake_keywords = rake.run(jd)
            words = list(zip(*rake_keywords)[0]) if len(rake_keywords) > 0 else []
            my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]

            words = apply_filters(words, my_lemmas)
            rake_output += " , ".join(words[:min(5, len(words))]) + "\n"
            # rake_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")

            # =========TopicRank===========
            topic_rank_extractor = TopicRank(input_file=input_file_path, meta_file=meta_file_path, language='english')
            topic_rank_extractor.read_document(format='preprocessed', stemmer=None)

            topic_rank_extractor.candidate_selection()
            topic_rank_extractor.candidate_weighting()
            topic_rank_keyphrases = topic_rank_extractor.get_n_best(n=5)

            words = list(zip(*topic_rank_keyphrases)[0]) if len(topic_rank_keyphrases) > 0 else []
            my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]
            words = apply_filters(words, my_lemmas)
            topic_rank_output += " , ".join(words[:min(5, len(words))]) + "\n"
            # topic_rank_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")

            # ==========KPMiner===========
            KPMiner_extractor = KPMiner(input_file=input_file_path, meta_file=meta_file_path, language='english')
            KPMiner_extractor.read_document(format='preprocessed', stemmer=None)

            KPMiner_extractor.candidate_selection()
            KPMiner_extractor.candidate_weighting()
            KPMiner_keyphrases = KPMiner_extractor.get_n_best(n=5)

            words = list(zip(*KPMiner_keyphrases)[0]) if len(KPMiner_keyphrases) > 0 else []
            my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]
            words = apply_filters(words, my_lemmas)
            kpminer_output += " , ".join(words[:min(5, len(words))]) + "\n"
            # kpminer_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")
            # rake_out_f.write(rake_output + "\n")

    rake_out_f.write(rake_output)
    topic_rank_out_f.write(topic_rank_output)
    kpminer_out_f.write(kpminer_output)

    rake_out_f.close()
    topic_rank_out_f.close()
    kpminer_out_f.close()
"""

rake_output = ""
topic_rank_output = ""
kpminer_output = ""

for i, (preprocessed_line, rake_raw_line, lemma) in enumerate(zip(new_preprocessed_lines, new_rake_data_lines,
                                                                  new_lemma_lines)):
    print i
    parts = preprocessed_line.strip().split("\t")
    jd_pos = parts[1]

    parts = rake_raw_line.strip().split("\t")
    jd = parts[1]

    f = open(input_file_path, "w")
    f.write(jd_pos)
    f.close()

    # f = open(meta_file_path, "w")
    # f.write(title.strip())
    # f.close()

    raw_words = jd.split(" ")
    lemma_words = lemma.strip().split(" ")

    word_lemma_map = dict()

    if len(raw_words) == len(lemma_words):
        [word_lemma_map.setdefault(word, lemma) for (word, lemma) in zip(raw_words, lemma_words)]
    else:
        "Error!"

    # =========Rake=======
    """
    rake_keywords = rake.run(jd)
    words = list(zip(*rake_keywords)[0]) if len(rake_keywords) > 0 else []
    my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]

    words = apply_filters(words, my_lemmas)
    rake_output += " , ".join(words[:min(5, len(words))]) + "\n"
    # rake_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")
    """

    # =========TopicRank===========
    topic_rank_extractor = TopicRank(input_file=input_file_path, meta_file=meta_file_path, language='english')
    topic_rank_extractor.read_document(format='preprocessed', stemmer=None)

    topic_rank_extractor.candidate_selection()
    topic_rank_extractor.candidate_weighting()
    topic_rank_keyphrases = topic_rank_extractor.get_n_best(n=5)

    words = list(zip(*topic_rank_keyphrases)[0]) if len(topic_rank_keyphrases) > 0 else []
    my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]
    words = apply_filters(words, my_lemmas)
    topic_rank_output += " , ".join(words[:min(5, len(words))]) + "\n"
    # topic_rank_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")

    # ==========KPMiner===========
    KPMiner_extractor = KPMiner(input_file=input_file_path, meta_file=meta_file_path, language='english')
    KPMiner_extractor.read_document(format='preprocessed', stemmer=None)

    KPMiner_extractor.candidate_selection()
    KPMiner_extractor.candidate_weighting()
    KPMiner_keyphrases = KPMiner_extractor.get_n_best(n=5)

    words = list(zip(*KPMiner_keyphrases)[0]) if len(KPMiner_keyphrases) > 0 else []
    my_lemmas = [word_lemma_map[word] if word in word_lemma_map else word for word in words]
    words = apply_filters(words, my_lemmas)
    kpminer_output += " , ".join(words[:min(5, len(words))]) + "\n"
    # kpminer_out_f.write(" , ".join(words[:min(5, len(words))]) + "\n")

    if (i + 1) % 100 == 0:
        print "dumping into respective files"
        # rake_out_f.write(rake_output)
        topic_rank_out_f.write(topic_rank_output)
        kpminer_out_f.write(kpminer_output)
        rake_output = ""
        topic_rank_output = ""
        kpminer_output = ""

# rake_out_f.write(rake_output)
topic_rank_out_f.write(topic_rank_output)
kpminer_out_f.write(kpminer_output)

# rake_out_f.close()
topic_rank_out_f.close()
kpminer_out_f.close()

# ensemble_predictions()

# Parallel(n_jobs=num_cores)(delayed(get_keyphrases)(core_id) for core_id in range(num_cores))
