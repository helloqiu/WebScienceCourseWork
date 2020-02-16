import pandas as pd

fp = 'NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'

emolex_df = pd.read_csv(fp, names=["word", "emotion", "association"], sep='\t')
emolex_words = emolex_df.pivot(index='word',
                               columns='emotion',
                               values='association').reset_index()
