#####################################################################################################
# title: 'Semantic severity method'
# author: "Naomi Baes"
#####################################################################################################

rm(list = ls()) # remove everything in global environment
cat("\014") # clear console
knitr::opts_chunk$set(echo = TRUE, include = TRUE) # set all chunks to show code (echo) and output (include) when running script

library(here) # detect root directory 
library(dplyr) # data manipulation

# specify paths for datasets
coll_path <- here("data/input", "trauma_year_counts.csv")
warr_path <- here("data/input", "warriner_rat.csv")

# load data
coll_count <- read.csv(coll_path) # load [1] trauma collocates in psychology abstracts per year (1970-2017)
coll_unique <- coll_count %>% distinct(lemma) # create tibble containing initial list of trauma collocates
warr_rat <- read.csv(warr_path) %>% # load and prep [2] Warriner norm ratings (1-9)
  rename(id = "X", lemma = "word") %>% # rename columns
  filter(lemma != "FALSE", lemma != "TRUE") %>% # remove non-values (#) 
  mutate(V.Mean.Sum.R = 9 - V.Mean.Sum) %>% # reverse score `V.Mean.Sum` so scores range from happy(1)-unhappy(9)
  select(c("id", "lemma", "V.Mean.Sum.R", "A.Mean.Sum")) # select relevant columns

# prep data
matches <- inner_join(warr_rat, coll_count, by = "lemma") # join "Warriner lemmas "warr_rat" by `lemma` column in "collocations df "coll_count" to obtain unique word matches
matches <- matches[, c(1, 2, 5, 6, 3, 4)] # reorder columns & rename data frame for data manipulation
df_word <- matches %>% mutate(AV.Mean.Sum=(A.Mean.Sum + V.Mean.Sum.R)) # merge mean valence and arousal ratings

############################ Compute repetition-weighted severity indices ###########################

# *Weighted average severity* = sum(ratings * repetitions by lemma) by year/ sum(repetitions) by year

# Step 1. Weighted sum = Sum(sum of mean severity ratings * the repetition of each word near trauma)

df_word <- df_word %>% # compute the product of mean sum ratings (AV,A,V) * lemma repetitions
  mutate(AV.prod = (AV.Mean.Sum*repet),
         A.prod = (A.Mean.Sum*repet),  
         V.prod = (V.Mean.Sum.R*repet))

df_word <- df_word %>% # group by year and sum for each group (AV,A,V) (numerator)
  group_by(year) %>%
  mutate(sumAVprod.word = sum(AV.prod),
         sumAprod.word = sum(A.prod),
         sumVprod.word = sum(V.prod)) %>% 
  ungroup()

# Step 2. Standardize 

df_word <- df_word %>% # sum repetitions by year (denominator)  
  group_by(year) %>% 
  mutate(sum_repet_word = sum(repet)) %>% 
  ungroup()

df <- df_word %>% # compute standardization (for AV,A,V)
  group_by(year) %>%
  summarize(sev_word = (sumAVprod.word/sum_repet_word),
            aro_word = (sumAprod.word/sum_repet_word),  
            val_word = (sumVprod.word/sum_repet_word)) %>%
  distinct() %>%
  ungroup()

# 3) Create and save the final data frame

write.csv(df, file='data/output/df.csv') # save final df in working directory (should contain variables for statistical analysis)
cat("The data frame has been exported.", "\n")

######################################## End of method setup ########################################