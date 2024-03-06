# -*- coding: utf-8 -*-
"""Bank Reviews/ Complaint Analysis using NLP

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/#fileId=https%3A//storage.googleapis.com/kaggle-colab-exported-notebooks/bank-reviews-complaint-analysis-using-nlp-0b6d451f-3b2a-47b1-83e2-f1c30561c3e8.ipynb%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com/20240306/auto/storage/goog4_request%26X-Goog-Date%3D20240306T114314Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D0ed108177a4450ddc895267e7c23db744a487c20f61558dbb9ba3a2a046a7098d42c6c5fa127d535bc52a031d8839746dfe6362052e4837b16b28d8eaadf850126bb6d20e9d1685254caa0121b6043f8d746262be21e23358648ec1e26689416f109c87b85dad0d23a5628009e98f0fc37556aed936fd115a9ee5f25c59c2be8e49941d23e58dc1034df189d2fba60fb3a464ed479f7ba13727ef1548fa25960ccb6a91ddb0557d8b9b7ef73319ec910f9beff5e024fea41ca0e623f405b87d4380e786038aedd9ffbe016393d4adf7df3bf9fd742c0369ff7934593aeaf691a9d74963b927a556ad31b6e464c6cc6b0bafe685668b33d205ec2da86dcd96409
"""

import os
import sys
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
from urllib.parse import unquote, urlparse
from urllib.error import HTTPError
from zipfile import ZipFile
import tarfile
import shutil

CHUNK_SIZE = 40960
DATA_SOURCE_MAPPING = 'bank-reviewcomplaint-analysis:https%3A%2F%2Fstorage.googleapis.com%2Fkaggle-data-sets%2F406007%2F778483%2Fbundle%2Farchive.zip%3FX-Goog-Algorithm%3DGOOG4-RSA-SHA256%26X-Goog-Credential%3Dgcp-kaggle-com%2540kaggle-161607.iam.gserviceaccount.com%252F20240306%252Fauto%252Fstorage%252Fgoog4_request%26X-Goog-Date%3D20240306T114314Z%26X-Goog-Expires%3D259200%26X-Goog-SignedHeaders%3Dhost%26X-Goog-Signature%3D541c3c3f2b17ee980f0343905e9fdc6931eead1a275e78fc4d2ac1c82a14852fb1911307fafe80947e872a2483c3312eb348055e131304fb925090c837d547165b7aabe557855c569765dee6751e731f1ee54c7f50bcdd31686dfcc48475890da3bea8a581a11b8f4de7fb694e69c9d893cc04189e87d945f2c5c48b9e9f9d7bbd9116264f3afe590a773c5fe3b2d11bfb8fa4a2efbc08400e788400728f0ff5e3f253e4b46f0d19529dfa680eca6948f20e4f3349c1adf5dc45ae6e7e89db295c7b1cb4fb8e2f713619191532bdfcdd6fba0358c4a315b8cf8244e358d556870ecf51a051d97100f13dc77b5879e96ac207def11061b641e5dbcd88f5f02f7a'

KAGGLE_INPUT_PATH='/kaggle/input'
KAGGLE_WORKING_PATH='/kaggle/working'
KAGGLE_SYMLINK='kaggle'

!umount /kaggle/input/ 2> /dev/null
shutil.rmtree('/kaggle/input', ignore_errors=True)
os.makedirs(KAGGLE_INPUT_PATH, 0o777, exist_ok=True)
os.makedirs(KAGGLE_WORKING_PATH, 0o777, exist_ok=True)

try:
  os.symlink(KAGGLE_INPUT_PATH, os.path.join("..", 'input'), target_is_directory=True)
except FileExistsError:
  pass
try:
  os.symlink(KAGGLE_WORKING_PATH, os.path.join("..", 'working'), target_is_directory=True)
except FileExistsError:
  pass

for data_source_mapping in DATA_SOURCE_MAPPING.split(','):
    directory, download_url_encoded = data_source_mapping.split(':')
    download_url = unquote(download_url_encoded)
    filename = urlparse(download_url).path
    destination_path = os.path.join(KAGGLE_INPUT_PATH, directory)
    try:
        with urlopen(download_url) as fileres, NamedTemporaryFile() as tfile:
            total_length = fileres.headers['content-length']
            print(f'Downloading {directory}, {total_length} bytes compressed')
            dl = 0
            data = fileres.read(CHUNK_SIZE)
            while len(data) > 0:
                dl += len(data)
                tfile.write(data)
                done = int(50 * dl / int(total_length))
                sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl} bytes downloaded")
                sys.stdout.flush()
                data = fileres.read(CHUNK_SIZE)
            if filename.endswith('.zip'):
              with ZipFile(tfile) as zfile:
                zfile.extractall(destination_path)
            else:
              with tarfile.open(tfile.name) as tarfile:
                tarfile.extractall(destination_path)
            print(f'\nDownloaded and uncompressed: {directory}')
    except HTTPError as e:
        print(f'Failed to load (likely expired) {download_url} to path {destination_path}')
        continue
    except OSError as e:
        print(f'Failed to load {download_url} to path {destination_path}')
        continue

print('Data source import complete.')

"""<h1 align ='center'> Bank Review/Complaint Analysis </h1>

<h4><i>Central banks collecting information about customer satisfaction with the services provided by different banks. Also collects the information about the complaints.</i></h4>
<ul>
<li><i>Bank users give ratings and write reviews about the services on central bank websites. These reviews and ratings help banks evaluate services provided and take necessary action to improve customer service. While ratings are useful to convey the overall experience, they do not convey the context which led a reviewer to that experience.</i></li>
<li><i>If we look at only the rating, it is difficult to guess why the user rated the service as 4 stars. However, after reading the review, it is not difficult to identify that the review talks about good 'service' and 'experience'.</i></li></ul>

<h2>The objetive of the case study is to analyze customer reviews and predict customer satisfaction with the reviews.
</h2>

## Import necesssary libraries
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import string
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer,TfidfVectorizer
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import nltk
from nltk.corpus import wordnet

"""### Import the data set"""

customer = pd.read_csv('../input/bank-reviewcomplaint-analysis/BankReviews.csv', encoding='windows-1252' )

customer.head()

"""## Data Audit"""

customer.info()

customer.shape

customer.isnull().sum()

customer['Stars'].value_counts()

plt.figure(figsize=(8,6))
sns.countplot(customer.Stars)
plt.show()

"""## Sentiment Analysis to find positive and negative reviews"""

X = customer['Reviews']
Y = customer['Stars']

X.head()

# UDF to find sentiment polarity of the reviews
def sentiment_review(text):
    analysis = TextBlob(text)
    polarity_text = analysis.sentiment.polarity
    if polarity_text > 0:
        return 'Positive'
    elif polarity_text == 0:
        return 'Neutral'
    else:
        return 'Negative'

# creating dictionary which will contain both the review and the sentiment of the review
final_dictionary = []
for text in X:
    dictionary_sentiment = {}
    dictionary_sentiment['Review'] = text
    dictionary_sentiment['Sentiment'] = sentiment_review(text)
    final_dictionary.append(dictionary_sentiment)
print(final_dictionary[:5])

# Finding positive reviews
positive_reviews = []
for review in final_dictionary:
    if review['Sentiment'] =='Positive':
        positive_reviews.append(review)
print(positive_reviews[:5])

# Finding neutral reviews
neutral_reviews = []
for review in final_dictionary:
    if review['Sentiment'] =='Neutral':
        neutral_reviews.append(review)
print(neutral_reviews[:5])

# Finding negative reviews
negative_reviews = []
for review in final_dictionary:
    if review['Sentiment'] =='Negative':
        negative_reviews.append(review)
print(negative_reviews[:5])

# counting number of positive,neutral and negative reviews
reviews_count = pd.DataFrame([len(positive_reviews),len(neutral_reviews),len(negative_reviews)],index=['Positive','Neutral','Negative'])

reviews_count

reviews_count.plot(kind='bar')
plt.ylabel('Reviews Count')
plt.show()

# printing first five positive reviews
i=1
for review in positive_reviews[:5]:
        print(i)
        print(review['Review'])
        print('******************************************************')
        i+=1

# printing first five negative reviews
i=1
for review in negative_reviews[:5]:
        print(i)
        print(review['Review'])
        print('******************************************************')
        i+=1

"""## Finding most frequently used Positive/ Negative words

### Data Preprocessing
"""

# UDF to clean the reviews
def clean_text(text):
    text = text.lower()
    text = text.strip()
    text = "".join([char for char in text if char not in string.punctuation])
    return text

# X = customer['Reviews']
X.head()

# applying clean_text function defined above to remove punctuation, strip extra spaces and convert each word to lowercase
X = X.apply(lambda y: clean_text(y))

X.head()

"""### Coverting reviews to tokens"""

tokens_vect = CountVectorizer(stop_words='english')

token_dtm = tokens_vect.fit_transform(X)

tokens_vect.get_feature_names()

from sklearn.feature_extraction.text import CountVectorizer

print(type(tokens_vect))

feature_names = tokens_vect.get_feature_names_out()

token_dtm.toarray()

token_dtm.toarray().shape

len(feature_names)

pd.DataFrame(token_dtm.toarray(),columns = feature_names)

print(token_dtm)

# creating a dataframe which shows the count of how many times a word is coming in the corpus
count_dtm_dataframe = pd.DataFrame(np.sum(token_dtm.toarray(),axis=0),feature_names).reset_index()
count_dtm_dataframe.columns =['Word','Count']

count_dtm_dataframe.head()

#adding sentiment column which shows sentiment polarity of each word
sentiment_word = []
for word in count_dtm_dataframe['Word']:
    sentiment_word.append(sentiment_review(word))
count_dtm_dataframe['Sentiment'] = sentiment_word

count_dtm_dataframe.head()

# separating positive words
positive_words_df= count_dtm_dataframe.loc[count_dtm_dataframe['Sentiment']=='Positive',:].sort_values('Count',ascending=False)

positive_words_df.head(20)

# plotting word cloud of 10 most frequently used positive words
wordcloud = WordCloud(width = 1000, height = 500).generate(' '.join(positive_words_df.iloc[0:11,0]))
# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()

# separating negative words
negative_words_df= count_dtm_dataframe.loc[count_dtm_dataframe['Sentiment']=='Negative',:].sort_values('Count',ascending=False)

negative_words_df.head(10)

# plotting word cloud of 10 most frequently used positive words
wordcloud = WordCloud(width = 1000, height = 500).generate(' '.join(negative_words_df.iloc[0:11,0]))
# plot the WordCloud image
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()

"""## Topic Modelling

### Splitting the data into train and test
"""

train_X,test_X,train_Y,test_Y = train_test_split(X,Y,random_state = 123, test_size = 0.2)

print('No.of observations in train_X: ',len(train_X), '| No.of observations in test_X: ',len(test_X))
print('No.of observations in train_Y: ',len(train_Y), '| No.of observations in test_Y: ',len(test_Y))

"""# Feature Generation using DTM and TDM

### Feature generation using DTM
"""

vect = CountVectorizer(strip_accents='unicode', stop_words='english', ngram_range=(1,1),min_df=0.001,max_df=0.95)

train_X_fit = vect.fit(train_X)
train_X_dtm = vect.transform(train_X)
test_X_dtm = vect.transform(test_X)

print(train_X_dtm)

print(test_X_dtm)

vect.get_feature_names()

from sklearn.feature_extraction.text import CountVectorizer

vect.get_feature_names_out()

print('No.of features for are',len(vect.get_feature_names_out()))

train_X_dtm_df = pd.DataFrame(train_X_dtm.toarray(),columns=vect.get_feature_names_out())

train_X_dtm_df.head()

# Finding how many times a tem is used in corpus
train_dtm_freq = np.sum(train_X_dtm_df,axis=0)

train_dtm_freq.head(20)

"""### Feature generation using TDM"""

vect_tdm = TfidfVectorizer(strip_accents='unicode', stop_words='english', ngram_range=(1,1),min_df=0.001,max_df=0.95)

train_X_tdm = vect_tdm.fit_transform(train_X)
test_X_tdm = vect.transform(test_X)

print(train_X_tdm)

print(test_X_tdm)

vect_tdm.get_feature_names()

from sklearn.feature_extraction.text import TfidfVectorizer

print(type(vect_tdm))

feature_names = vect_tdm.vocabulary_

print('No.of features for are',len(feature_names))

# creating dataframe to to see which features are present in the documents
train_X_tdm_df = pd.DataFrame(train_X_tdm.toarray(),columns=feature_names)

train_X_tdm_df.head()

test_X_tdm_df = pd.DataFrame(test_X_tdm.toarray(),columns=feature_names)

test_X_tdm_df.head()

# Finding how many times a term is used in test corpus
test_tdm_freq = np.sum(test_X_tdm_df,axis=0)

test_tdm_freq.head(20)

# train a LDA Model
lda_model = LatentDirichletAllocation(n_components=20, learning_method='online', max_iter=50)
X_topics = lda_model.fit_transform(train_X_tdm)
topic_word = lda_model.components_
vocab = feature_names

# view the topic models
top_words = 10
topic_summaries = []
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))
    print(topic_words)

topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(top_words+1):-1, None]

print(np.argsort(topic_dist).shape)

print(np.array(vocab).shape)

try:
    topic_words = np.array(vocab)[np.argsort(topic_dist)]
except IndexError as e:
    print(e)

topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(top_words+1):-1, None]

# view the topic models
top_words = 10
topic_summaries = []
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))
topic_summaries

"""# Building Model

### Building Model on DTM
"""

# building naive bayes model on DTM
naive_model = MultinomialNB()
naive_model.fit(train_X_dtm,train_Y)

predict_train = naive_model.predict(train_X_dtm)
predict_test = naive_model.predict(test_X_dtm)

len(predict_test)

print('Accuracy on train: ',metrics.accuracy_score(train_Y,predict_train))
print('Accuracy on test: ',metrics.accuracy_score(test_Y,predict_test))

# predict probabilities on train and test
predict_prob_train = naive_model.predict_proba(train_X_dtm)[:,1]
predict_prob_test = naive_model.predict_proba(test_X_dtm)[:,1]

print('ROC_AUC score on train: ',metrics.roc_auc_score(train_Y,predict_prob_train))
print('ROC_AUC score on test: ',metrics.roc_auc_score(test_Y,predict_prob_test))

cm_test = metrics.confusion_matrix(test_Y,predict_test)

cm_test

import seaborn as sns
sns.heatmap(cm_test,annot=True,xticklabels=[5,1],yticklabels=[5,1])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

"""### Building Model on TDM"""

# building naive bayes model on DTM
naive_model = MultinomialNB()
naive_model.fit(train_X_tdm,train_Y)

predict_train = naive_model.predict(train_X_tdm)
predict_test = naive_model.predict(test_X_tdm)

len(predict_test)

print('Accuracy on train: ',metrics.accuracy_score(train_Y,predict_train))
print('Accuracy on test: ',metrics.accuracy_score(test_Y,predict_test))

# predict probabilities on train and test
predict_prob_train = naive_model.predict_proba(train_X_tdm)[:,1]
predict_prob_test = naive_model.predict_proba(test_X_tdm)[:,1]

print('ROC_AUC score on train: ',metrics.roc_auc_score(train_Y,predict_prob_train))
print('ROC_AUC score on test: ',metrics.roc_auc_score(test_Y,predict_prob_test))

# confusion matrix on test
cm_test = metrics.confusion_matrix(test_Y,predict_test)

cm_test

import seaborn as sns
sns.heatmap(cm_test,annot=True,xticklabels=[5,1],yticklabels=[5,1])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

"""<h3> Model showed better results using DTM values and using unigrams.</h3>

## We were asked that we can ignore intent analysis as that is covered in topic modelling. Hence skipping that part.
"""