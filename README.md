# Semantic Severity Method
Source code to evaluate the semantic severity (vertical expansion) of concepts.

## Data

[1] **"warriner_rat.csv"**: csv file containing valence and arousal ratings to be matched with lemmas that are concept collocates. File contains normed ratings of 13,915 words on a 9-point likert scale: mean, sd, gender responses for US residents grouped by age.
- `word` = English lemmas
- `V.Mean.Sum` = Summed average ratings of lemmas on Valence (i.e., the pleasantness of the emotions invoked by a word) from happy (9) to unhappy (1) 
- `A.Mean.Sum` = Summed average ratings of lemmas on Arousal (i.e., the intensity of emotion provoked by a stimulus) from aroused (9) to calm/unaroused (1) 

[2] **"concept_year_counts.csv"**: csv file containing corpus statistics for counts of collocates appearing near (i.e., within a set context window) the term(s) representing the concept within sentences in the corpus by year.
- `year` = the year in which the lemma appeared in the corpus (e.g., 1970-2017)
- `lemma` = the root form of the English word
- `repet` = the number of times the lemma appeared with trauma within the context window in each sentence in the corpus
- `cond_prob` = conditional probability: `repet` of each `lemma` divided by the sum of `repet` of lemmas in each year (i.e., a sort of relative frequency)

## Method

To compute severity indices:
- **Step 1**: First link the Warriner ratings with the concept collocates dataset and reverse score `V.Mean.Sum` so scores range from happy (1) to unhappy (9). 
- **Step 2**: Filter `year` in the matched data frame from when all collocate counts reach double digits (< 10).
- **Step 3**: Then, compute a weighted average for semantic severity by (1) summing `V.Mean.Sum` and `A.Mean.Sum`, (2) weighting it by the repetition of each colocate by year and (3) standardizing it by the sum of collocate repetitions grouped by year.

## References

[1] Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior research methods, 45(4), 1191-1207. https://doi.org/10.3758/s13428-012-0314-x

*This method has been used in the following manuscripts:* 

[2] Baes, N., Vylomova, E., Zyphur, M. J., Haslam, N. The semantic inflation of 'trauma' in psychology. [COMPLETE]
