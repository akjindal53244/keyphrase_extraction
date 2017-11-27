chunk_ids = [str(i+1) for i in range(8)]

topic_rank = "resources/data/social_text_tokenized_pos_topicrank_filtered_"
kpminer = "resources/data/social_text_tokenized_pos_kpminer_filtered_"

def merge_chunks():
    all_topic_rank_lines = []
    all_kpminer_lines = []
    for i in range(8):

        topic_rank_lines = open(topic_rank + chunk_ids[i], "r").readlines()
        all_topic_rank_lines.extend([line.strip() for line in topic_rank_lines])

        kpminer_lines = open(kpminer + chunk_ids[i], "r").readlines()
        all_kpminer_lines.extend([line.strip() for line in kpminer_lines])

    print "topic_rank lines:" + str(len(all_topic_rank_lines))
    print "kpminer lines:" + str(len(all_kpminer_lines))

    topic_rank_combined_f = open(topic_rank + "all", "w")
    kpminer_combined_f = open(kpminer + "all", "w")

    if len(all_topic_rank_lines) == len(all_kpminer_lines):
        print "consistent data"

        for i, (l2, l3) in enumerate(zip(all_topic_rank_lines, all_kpminer_lines)):
            # rake_combined_f.write(l1 + "\n")
            topic_rank_combined_f.write(l2 + "\n")
            kpminer_combined_f.write(l3 + "\n")
    else:
        print "Inconsistent data"
    topic_rank_combined_f.close()
    kpminer_combined_f.close()

merge_chunks()