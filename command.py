import nltk
from nltk.tokenize import word_tokenize
from sklearn.svm import SVC

# Preprocess the text by tokenizing it
text = "Hello, how are you today?"
tokens = word_tokenize(text)

# Stem or lemmatize the words
stemmer = nltk.stem.PorterStemmer()
lemmatizer = nltk.stem.WordNetLemmatizer()
stemmed_tokens = [stemmer.stem(token) for token in tokens]
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

# Train an SVM classifier on the preprocessed text
X = [stemmed_tokens, lemmatized_tokens]  # input data
y = ["command1", "command2"]  # target labels
classifier = SVC()
classifier.fit(X, y)

# Use the trained classifier to predict the category of new data
new_text = "Hi there, can you please open the door?"
new_tokens = word_tokenize(new_text)
new_stemmed_tokens = [stemmer.stem(token) for token in new_tokens]
new_lemmatized_tokens = [lemmatizer.lemmatize(token) for token in new_tokens]
new_X = [new_stemmed_tokens, new_lemmatized_tokens]
predictions = classifier.predict(new_X)

# Print the predicted categories
print(predictions)  # Output: ["command1", "command2"]
