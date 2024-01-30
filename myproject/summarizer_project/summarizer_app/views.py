from django.shortcuts import render
from .forms import DocumentForm
from .models import Document
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from nltk.tokenize.treebank import TreebankWordDetokenizer
import nltk


def summarize_document(content):
    # Tokenize the content into sentences
    sentences = sent_tokenize(content)

    # Tokenize and tag each sentence
    tagged_sentences = [pos_tag(word_tokenize(sentence)) for sentence in sentences]

    # Filter out stopwords and non-content words
    stop_words = set(stopwords.words('english'))
    filtered_sentences = [
        [word for word, pos in tagged_sentence if word.lower() not in stop_words and pos in {'NN', 'VB', 'JJ'}]
        for tagged_sentence in tagged_sentences
    ]

    # Calculate the frequency of each word in the document
    words = [word for sentence in filtered_sentences for word in sentence]
    freq_dist = FreqDist(words)

    # Choose the top N most frequent words
    top_words = [word for word, freq in freq_dist.most_common(10)]

    # Generate the summary by selecting sentences containing the top words
    summarized_sentences = [
        sentence for sentence in sentences
        if any(word in sentence for word in top_words)
    ]

    # Detokenize the summarized sentences into a single string
    summarized_content = TreebankWordDetokenizer().detokenize(summarized_sentences)

    return summarized_content

def home(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            summarized_content = summarize_document(document.content)
            return render(request, 'summarizer_app/result.html', {'document': document, 'summarized_content': summarized_content})
    else:
        form = DocumentForm()
    return render(request, 'summarizer_app/home.html', {'form': form})
