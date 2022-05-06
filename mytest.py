from typing import Mapping
from urllib import response
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np

#tf_idf
#words = whole text
#word the word we finding the score for
#return the score


words = ['this is the first document '
         'this is another one this is the final '
         'Kaeya of all the docs wow this will just '
         'keep going who knew that ther could be this '
         'much Madeon - Love You Back (Visualizer)'
         'how many how many how how how how']
doc1 = ["I can't fucking take it any more. Among Us has singlehandedly ruined my life. The other day my teacher was teaching us Greek Mythology and he mentioned a pegasus and I immediately thought 'Pegasus? more like Mega Sus!!!!' and I've never wanted to kms more. I can't look at a vent without breaking down and fucking crying. I can't eat pasta without thinking 'IMPASTA??? THATS PRETTY SUS!!!!' Skit 4 by Kanye West. The lyrics ruined me. A Mongoose, or the 25th island of greece. The scientific name for pig. I can't fucking take it anymore. Please fucking end my suffering."]
doc2 = ["Anyways, um... I bought a whole bunch of shungite rocks, do you know what shungite is? Anybody know what shungite is? No, not Suge Knight, I think he's locked up in prison. I'm talkin' shungite. Anyways, it's a two billion year-old like, rock stone that protects against frequencies and unwanted frequencies that may be traveling in the air. That's my story, I bought a whole bunch of stuff. Put 'em around the la casa. Little pyramids, stuff like that."]
word = 'life'

try:
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(doc1)
    df = pd.DataFrame(tfidf_matrix.toarray(), columns = tfidf.get_feature_names_out())
    print(df.iloc[0][''.join(word)])
    #print(df)
except KeyError: # word does not exist 
    print(-1)

# vect = TfidfVectorizer()
# tfidf_matrix = vect.fit_transform(words)
# feature_index = tfidf_matrix[0,:].nonzero()[1]
# feature_names = vect.get_feature_names_out()
# tfidf_scores = zip(feature_index, [tfidf_matrix[0, x] for x in feature_index])
# for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
#     if w == word: 
#         print(s)
#--------------------------------- Prints the list of all -----------------------------------#        
# for w, s in [(feature_names[i], s) for (i, s) in tfidf_scores]:
#   print (w, s)

#--------------------------------- Both of these implentations are from this link -----------------------------------------#
# https://stackoverflow.com/questions/34449127/sklearn-tfidf-transformer-how-to-get-tf-idf-values-of-given-words-in-documen
# tfidf = TfidfVectorizer()
# response = tfidf.fit_transform([doc1, doc2])
# print(len(tfidf.vocabulary_))
# print(tfidf.vocabulary_)
# feature_names = tfidf.get_feature_names_out()
# for col in response.nonzero()[1]:
#     print(feature_names[col], ' - ', response[0,col])









