# Semantic Severity Method
Source code to evaluate the semantic severity (vertical expansion) of concepts. 

*Note*: All files except "warriner_rat.csv" contain example files using 'trauma' in a corpus of psychology article abstracts. 

## Data

### Input folder

[1] **"warriner_rat.csv"**: csv file containing valence and arousal ratings to be matched with lemmas that are concept collocates. File contains normed ratings of 13,915 words on a 9-point likert scale: "mean", "sd", "gender" responses for US residents grouped by age. Only relevant columns noted below.
- `word` = English lemmas
- `V.Mean.Sum` = Summed average ratings of lemmas on Valence (i.e., the pleasantness of the emotions invoked by a word) from happy (9) to unhappy (1) 
- `A.Mean.Sum` = Summed average ratings of lemmas on Arousal (i.e., the intensity of emotion provoked by a stimulus) from aroused (9) to calm/unaroused (1) 

[2] **"trauma_year_counts.csv"**: csv file containing corpus statistics for counts of collocates appearing near (i.e., +/- 5-word context window) the term representing the concept in sentences in the corpus by year.
- `year` = the year in which the lemma appeared in the corpus (e.g., 1970-2017)
- `lemma` = the root form of the English word
- `repet` = the number of times the lemma appeared with trauma within the context window in each sentence in the corpus

### Output folder

[3] **"df.csv**: csv file containing time series of severity indices
- `year` = the year in which the lemma appeared in the corpus (e.g., 1970-2017)
- `sev_word` = index for the severity (valence+arousal ratings) of trauma-related lemmas
- `aro_word` = index for the arousal ratings of trauma-related lemmas
- `val_word` = index for the valence ratings of trauma-related lemmas
![head(df)](https://user-images.githubusercontent.com/58921702/174312003-82dc3a7b-8780-4a5c-9fec-d4743163d2c3.PNG)

## Method

### Corpus Preprocessing
The preprocessing is done via preprocess_data_spacy.py script. Note you need ``spacy'' library and download a pre-trained model, e.g. "en_core_web_lg" 
- **Step 1**: Remove punctuation 
- **Step 2**: Lemmatize words
- **Step 3**: De-capitalize words
- **Step 4**: Remove stop-words

### Collocations
To extract collocations (`lemma`) and their repetitions (`repet`) in "trauma_year_counts.csv", see **"xx.xx"** for corpus preprocessing instructions.
- **Step 1**: Compute algorithm to select lemmas within +/- 5-word context window of [term representing the concept], number of times words repeat, and order words by repetitions. 
```{r}
cat preprocessed_corpus.csv |  grep -oP '(\w+) trauma\W' | sort -d | uniq -c | sed -r 's/^ +//g' | sort -k1 -n -r | head -n 10
```
- **Step 2**: Extract word list and counts in a .csv file
```{r}
code
```
### Severity Index
To compute severity indices (see **"severity_indices.R"** file - also in **"severity_indices.Rmd"** form.):
- **Step 1**: First, link the Warriner ratings with the concept collocates dataset and reverse score `V.Mean.Sum` so scores range from happy (1) to unhappy (9). 
- **Step 2**: Then, compute a weighted average for semantic severity by (1) summing `V.Mean.Sum` and `A.Mean.Sum`, (2) weighting it by the repetition of each colocate by year and (3) standardizing it by the sum of collocate repetitions grouped by year.

## References

[1] Warriner, A. B., Kuperman, V., & Brysbaert, M. (2013). Norms of valence, arousal, and dominance for 13,915 English lemmas. Behavior research methods, 45(4), 1191-1207. https://doi.org/10.3758/s13428-012-0314-x

*This method has been used in the following manuscripts:* 

[2] Baes, N., Vylomova, E., Zyphur, M. J., Haslam, N. The semantic inflation of 'trauma' in psychology. [SUBMITTED]
