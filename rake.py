# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010).
# Automatic keyword extraction from indi-vidual documents.
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

import re
import operator
import pke
from pke import TopicRank, KPMiner


debug = False
test = False




def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        # current_word = single_word.strip().lower()
        current_word = single_word.strip()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            # phrase = phrase.strip().lower()
            phrase = phrase.strip()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        if word_list_length < 4:
            for word in word_list:
                word_frequency.setdefault(word, 0)
                word_frequency[word] += 1
                word_degree.setdefault(word, 0)
                word_degree[word] += word_list_degree  #orig.
                #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        if len(word_list) <4:
            candidate_score = 0
            for word in word_list:
                candidate_score += word_score[word]
            keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path):
        self.stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stop_words_path)

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.iteritems(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords


if test:
    text = "Experience in Java is a must. Knowledge of Spring, Struts, Hibernate etc. Should be good with algorithms, data structures. Should have working knowledge of GIT. Should have worked in an agile environment. Communication skills should be great."

    precessed_text = "Our/PRP$ client/NN is/VBZ a/DT leading/VBG publisher/NN of/IN consumer/NN and/CC trade/NN magazines/NNS and/CC due/JJ to/TO continued/JJ growth/NN currently/RB require/VBP an/DT Advertising/NN Sales/NNS Executive/NNP to/TO join/VB their/PRP$ busy/JJ and/CC successful/JJ team/NN ./. Candidates/NNS will/MD be/VB responsible/JJ for/IN selling/VBG advertising/NN in/IN a/DT range/NN of/IN business/NN and/CC consumer/NN magazines/NNS and/CC a/DT number/NN of/IN trade/NN magazines/NNS from/IN both/CC an/DT existing/VBG client/NN base/NN as/RB well/RB as/IN searching/VBG out/RP potential/JJ new/JJ clients/NNS ./. Candidates/NNS need/VBP to/TO have/VB a/DT minimum/NN of/IN one/CD years/NNS advertising/NN sales/NNS experience/NN as/RB well/RB as/IN a/DT proven/JJ track/NN record/NN of/IN achievement/NN and/CC an/DT enthusiastic/JJ approach/NN to/TO developing/VBG and/CC winning/VBG business/NN ./. Candidates/NNS will/MD also/RB be/VB responsible/JJ for/IN attending/VBG trade/NN shows/NNS //: events/NNS so/RB face/VBP to/TO face/VB sales/NNS ability/NN is/VBZ also/RB essential/JJ ./. In/IN return/NN candidates/NNS can/MD expect/VB to/TO receive/VB a/DT basic/JJ of/IN k/NN as/RB well/RB as/IN a/DT realistic/JJ uncapped/JJ OTE/NN of/IN k./NN"

    # Split text into sentences
    sentenceList = split_sentences(text)
    #stoppath = "FoxStoplist.txt" #Fox stoplist contains "numbers", so it will not find "natural numbers" like in Table 1.1
    stoppath = "resources/CombinedStopList"  #SMART stoplist misses some of the lower-scoring keywords in Figure 1.5, which means that the top 1/3 cuts off one of the 4.0 score words in Table 1.1
    stopwordpattern = build_stop_word_regex(stoppath)

    # generate candidate keywords
    phraseList = generate_candidate_keywords(sentenceList, stopwordpattern)

    # calculate individual word scores
    wordscores = calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = generate_candidate_keyword_scores(phraseList, wordscores)
    if debug: print keywordcandidates

    sortedKeywords = sorted(keywordcandidates.iteritems(), key=operator.itemgetter(1), reverse=True)
    if debug: print sortedKeywords

    totalKeywords = len(sortedKeywords)
    if debug: print totalKeywords
    # print sortedKeywords[0:(totalKeywords / 3)]

    rake = Rake("resources/CombinedStopList")
    keywords = rake.run(text)
    # print keywords
    print list(zip(*keywords)[0])[:20]

    input_file_path = "/home/asjindal/Work/tf/keyword_extraction/resources/sample_jd_preprocessed"

    f = open(input_file_path, "w")
    f.write(text)
    f.close()

    topic_rank_extractor = TopicRank(input_file=input_file_path, language='english')

    topic_rank_extractor.read_document(format='raw', stemmer=None)

    topic_rank_extractor.candidate_selection()
    topic_rank_extractor.candidate_weighting()
    topic_rank_keyphrases = topic_rank_extractor.get_n_best(n=20)
    # print topic_rank_keyphrases
    # print list(zip(*topic_rank_keyphrases)[0])[:20]

    words = list(zip(*topic_rank_keyphrases)[0])
    print words

    KPMiner_extractor = KPMiner(input_file=input_file_path, language='english')

    KPMiner_extractor.read_document(format='raw', stemmer=None)

    KPMiner_extractor.candidate_selection()
    KPMiner_extractor.candidate_weighting()
    KPMiner_keyphrases = KPMiner_extractor.get_n_best(n=20)

    words = list(zip(*KPMiner_keyphrases)[0])

    print words






"""
token_lines = open("/home/asjindal/Work/tf/keyword_extraction/resources/data/TrainData_tokenized", "r").readlines()
rake_out_f = open("resources/data/TrainData_tokenized_rake", "w")
rake = Rake("resources/CombinedStopList")
for i, line in enumerate(token_lines):
    print i
    parts = line.strip().split("\t")
    jd_pos = parts[2]
    rake_keywords = rake.run(jd_pos)

    words = list(zip(*rake_keywords)[0])
    rake_out_f.write(" , ".join(words[:min(20, len(words))]) + "\n")
"""
