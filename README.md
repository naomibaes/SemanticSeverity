# Semantic Severity Method
Source code to evaluate the semantic severity (vertical expansion) of concepts. 

*Note*: Collocate files use three centre terms ($word = "trauma", "anxiety", "depression") but the list can be expanded to include more terms. 

## Data

### Input folder

[1] **"warriner_rat.csv"**: csv file containing valence and arousal ratings to be matched with lemmas (collocates for the target/centre term). The file contains normed ratings of 13,915 words (lemmas specifically) on a 9-point likert scale: "mean", "sd", "gender" responses for US residents grouped by age. Only these columns are relevant to the method:
- `word` = English lemmas
- `V.Mean.Sum` = Summed average ratings of lemmas on Valence (i.e., the pleasantness of the emotions invoked by a word) from happy (9) to unhappy (1) 
- `A.Mean.Sum` = Summed average ratings of lemmas on Arousal (i.e., the intensity of emotion provoked by a stimulus) from aroused (9) to calm/unaroused (1) 

[2i--n] **"$word_year_coll_repet.csv"**: csv file containing corpus statistics for collocate's occurence near the target/centre term per year. 
- `year` = the year in which the lemma appeared in the corpus (1970-2017)
- `coll` = collocate appearing within the target term's context window (+/- 5 words); also a lemma (the root form of the English word)
- `repet` = the number of times that the collocates occur near (+/- 5-word context-window) the target/centre term in corpus sentences (abstracts) per year

### Output folder

[3] **"$word_$corpus_severity_indices.csv**: csv file containing time series of severity indices
- `year` = the year in which the lemma appeared in the corpus (1970-2017)
- `sev_index` = index for the severity (repetition-weighted valence+arousal ratings) of $word-related lemmas
- `aro_index` = index for the (repetition-weighted) arousal ratings of $word-related lemmas
- `val_index` = index for the (repetition-weighted) valence ratings of $word-related lemmas
![head(df)](https://user-images.githubusercontent.com/58921702/174312003-82dc3a7b-8780-4a5c-9fec-d4743163d2c3.PNG)

## Method

### Corpus Preprocessing
See **"preprocess_data_spacy.py"** script (Python). Dependencies: ``spacy'' library and a pre-trained model (e.g., "en_core_web_lg"). 
- **Steps**: (i) Remove punctuation, (ii) Lemmatize words, (iii) De-capitalize words, (iv) Remove stop-words

### Collocations
See **"retrieve_coll_year_repet_corpora.sh"** script (bash) for how to extract collocations (`word`) and their repetitions (`repet`) for 3 terms in 2 corpora.
- **Steps**: (i) Restrict corpus to only lines (abstracts/articles) containing the target/centre term, (ii) identify collocates (within 5-word context window), (iii) compute statistics for the number of times collocate occurs near the target/centre term and in what corpus year.

### Severity Index
See **"warrmatched_coll_year_stats_indices.R"** script (R Programming). **"severity_indices.R"** is an example of how to run the method on one term.
- **Steps**: (i) Link the Warriner ratings with the collocate data and reverse score `V.Mean.Sum` so scores range from happy (1) to unhappy (9), (ii) compute repetition-weighted average semantic severity index by (a) summing `V.Mean.Sum` and `A.Mean.Sum`, (b) weighting it by the repetition of each colocate by year and (c) dividing this numerator by the sum of collocate repetitions grouped by year (denominator).

## References

[1] Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior research methods, 45(4), 1191-1207. https://doi.org/10.3758/s13428-012-0314-x

*This method has been used in the following manuscripts:* 

[2] Baes, N., Vylomova, E., Zyphur, M., & Haslam, N. (2023). The semantic inflation of “trauma” in psychology. Psychology of Language and Communication, 27(1), 23-45. DOI: https://doi.org/10.58734/plc-2023-0002

[3] Xiao, Y., Baes, N., Vylomova, E., & Haslam, N. (2023). Have the concepts of ‘anxiety’and ‘depression’been normalized or pathologized? A corpus study of historical semantic change. Plos one, 18(6), e0288027.

[4] Naomi Baes, Nick Haslam, and Ekaterina Vylomova. 2023. Semantic Shifts in Mental Health-Related Concepts. In Proceedings of the 4th Workshop on Computational Approaches to Historical Language Change, pages 119–128, Singapore. Association for Computational Linguistics.

[5] pending publication

