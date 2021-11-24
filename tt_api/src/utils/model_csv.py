import pandas as pd
df = pd.read_csv('/Users/adriannava/Documents/Cursando/LyricGenerator/src/tt_api/src/utils/Pop.csv')
# Drop all the columns except Lyrics
df.drop(['Artist','Songs','Popularity','Genre','Genres','Idiom','ALink','SName','SLink'],axis=1,inplace=True)
df.drop(df.columns[df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
df = df[:700]
df['Number_of_words'] = df['Lyric'].apply(lambda x:len(str(x).split()))
df.to_csv('pop_model.csv')