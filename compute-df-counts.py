# -*- coding: utf-8 -*-

import os
import logging
import sys

from pke import compute_document_frequency
from string import punctuation

# setting info in terminal
logging.basicConfig(level=logging.INFO)

# path to the collection of documents
input_dir = "/home/asjindal/Work/tf/keyword_extraction/resources/data/docs"

# path to the df weights dictionary, saved as a gzipped csv file
output_file = "/home/asjindal/Work/tf/keyword_extraction/resources/data/train_df_count.tsv.gz"

# stoplist are punctuation marks
stoplist = list(punctuation)
stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']

# compute idf weights
compute_document_frequency(input_dir=input_dir,
						   output_file=output_file,
						   format="raw",                # input files format
                           use_lemmas=False,        # do not use Stanford lemmas
                           stemmer=None,                # use porter stemmer
                           stoplist=stoplist,                         # stoplist
                           delimiter='\t',                # tab separated output
                           extension='txt',              # input files extension
                           n=3)                  # compute n-grams up to 5-grams
