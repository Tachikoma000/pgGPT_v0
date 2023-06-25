import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import re
import numpy as np
import openai
import tensorflow_hub as hub
from sklearn.neighbors import NearestNeighbors

from config import OPENAI_API_KEY


class SemanticSearch:
    def __init__(self):
        self.use = hub.load('./Universal Sentence Encoder/')
        self.fitted = False

    def fit(self, data, batch=1000, n_neighbors=5):
        self.data = data
        self.embeddings = self.get_text_embedding(data, batch=batch)
        n_neighbors = min(n_neighbors, len(self.embeddings))
        self.nn = NearestNeighbors(n_neighbors=n_neighbors)
        self.nn.fit(self.embeddings)
        self.fitted = True

    def __call__(self, text, return_data=True):
        inp_emb = self.use([text])
        neighbors = self.nn.kneighbors(inp_emb, return_distance=False)[0]

        if return_data:
            return [self.data[i] for i in neighbors]
        else:
            return neighbors

    def get_text_embedding(self, texts, batch=1000):
        embeddings = []
        for i in range(0, len(texts), batch):
            text_batch = texts[i : (i + batch)]
            emb_batch = self.use(text_batch)
            embeddings.append(emb_batch)
        embeddings = np.vstack(embeddings)
        return embeddings

def preprocess(text):
    text = text.replace('\n', ' ')
    text = re.sub('\s+', ' ', text)
    return text

def read_md_file(path):
    with open(path, 'r') as file:
        return preprocess(file.read())

def text_to_chunks(texts, word_length=150):
    text_toks = [t.split(' ') for t in texts]
    chunks = []

    for idx, words in enumerate(text_toks):
        for i in range(0, len(words), word_length):
            chunk = words[i : i + word_length]
            if (
                (i + word_length) > len(words)
                and (len(chunk) < word_length)
                and (len(text_toks) != (idx + 1))
            ):
                text_toks[idx + 1] = chunk + text_toks[idx + 1]
                continue
            chunk = ' '.join(chunk).strip()
            chunks.append(chunk)
    return chunks

def load_recommender(md_file_path):
    recommender = SemanticSearch()
    texts = [read_md_file(md_file_path)]
    chunks = text_to_chunks(texts)
    recommender.fit(chunks)
    return recommender

def generate_text(openAI_key, prompt, engine="gpt-3.5-turbo"):
    openai.api_key = openAI_key
    try:
        message = ''
        response = openai.ChatCompletion.create(
            model=engine,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['message']['content']
    except Exception as e:
        message = f'API Error: {str(e)}'
    return message


def generate_answer(question, recommender, openAI_key):
    topn_chunks = recommender(question)
    prompt = ""
    prompt += 'search results:\n\n'
    for c in topn_chunks:
        prompt += c + '\n\n'
        
    prompt += (
        "Instructions: You are an AI expert in the topics covered in the search results, and are serving as a personal coding "
        "assistant. The user can ask for explanations, code examples, and solutions using the information provided in the search results. "
        "Utilize the information from the search results to answer the query. Extrapolate, synthesize or make connections that were not "
        "explicitly stated in the search results, if necessary and logical, based on the context. When asked for code examples, use "
        "the examples covered in the search results as a reference, but feel free to extrapolate or come up with additional examples "
        "if appropriate and logical. The aim is to provide a comprehensive and accurate response even if it's not explicitly detailed in "
        "the search results. Cite each reference using [Reference Number] notation. The responses should primarily be sourced from the "
        "knowledge provided in the search results, but you can also leverage your understanding of other programming languages and software "
        "engineering to provide rich responses, all while avoiding hallucinations.\n\n"
    )

    prompt += f"Query: {question}\nAnswer:"
    answer = generate_text(openAI_key, prompt, "gpt-3.5-turbo")
    return answer

def load_openai_key() -> str:
    if OPENAI_API_KEY is None:
        raise ValueError(
            "[ERROR]: Please pass your OPENAI_API_KEY. Get your key here : https://platform.openai.com/account/api-keys"
        )
    return OPENAI_API_KEY

def get_markdown(query):
    md_file_path = 'context_store.md'
    recommender = load_recommender(md_file_path)
    openAI_key = load_openai_key()
    answer = generate_answer(query, recommender, openAI_key)
    return answer


