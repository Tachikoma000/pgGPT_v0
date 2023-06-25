# pgGPT_v0

![Project screenshot](./images/pggpt_v0_vid.gif)

pgGPT_v0 is an intelligent search system, leveraging the capabilities of OpenAI's GPT-3.5-turbo model along with Google's Universal Sentence Encoder (USE) to empower users in extracting relevant information from Subgrounds documentation and Jupyter Notebook examples (`.ipynb` documents).

This application is designed as a versatile tool to navigate the ever-increasing collections of Subgrounds resources, offering instantaneous access to pertinent information. It serves as an invaluable educational utility for any individual seeking to delve deeper into the capabilities of Subgrounds, or striving to enhance their usage of it.

## Core Components

pgGPT_v0 consists of two key parts:

1. **OpenAI's GPT-3.5-turbo**: It is a language model that assists in interpreting user queries formulated in natural language, enabling the system to comprehend and process intricate queries that might be challenging for simpler keyword-based search mechanisms.

2. **Google's Universal Sentence Encoder**: This component is employed for semantic search, enabling the system to locate pertinent information even when the exact keywords aren't present in the query.

## Utility

The principal utility of this system lies in its ability to sift through extensive Subgrounds documents and Jupyter Notebook examples. It offers a convenient method to scan through the vast Subgrounds resource collections, making the search for relevant documentation or examples a breeze.

## Limitations

pgGPT_v0, despite being designed to mimic a chat bot, doesn't possess the memory or additional sophisticated features found in conversational GPT applications. It's essentially a simple AI program to query the docs using natural language. Although this system delivers accurate and useful responses, more conversational versions with advanced features will be developed in future iterations.

## Setting Up

The system can be easily set up and run on any local machine for development and testing purposes. Here are the prerequisites and steps for installation:

### Universal Sentence Encoder
Download the Universal Sentence Encoder locally to your project's root folder. This is important for generating embeddings for the docs. Download the encoder using this [link](https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed). 

Extract the downloaded file and place it in your project's root folder as shown below:
```text
Root folder
└───Universal Sentence Encoder
|   ├───assets
|   └───variables
|   └───saved_model.pb
```

### Prerequisites

Ensure the following packages are installed:

- Python 3.7 or higher
- httpx
- Textual
- openai
- numpy
- tensorflow_hub
- scikit-learn

### Installation

Clone the repository, navigate to the project directory, and install the requirements:

- git clone this repo
- cd pgGPT_v0
- pip install -r requirements.txt


## Usage

To use the application, ensure that your Subgrounds documents and examples are properly parsed and stored in `context_store.md`. You can edit the list of URLs in `md_parser.py` to include the documents you're interested in and then run `md_parser.py` to update `context_store.md` with the new data.

Set your OpenAI API key in the `config.py` file, and then run the main script:

`python main.py`


## Structure

pgGPT_v0's file structure is as follows:

- `api_md.py`: Contains the core functions, including the `SemanticSearch` class and the OpenAI GPT-3.5-turbo interaction functions.
- `main.py`: The main application that interacts with the user, retrieves markdown data based on user input, and displays the results.
- `main.css`: Contains the styles for the Textual application.
- `md_parser.py`: Fetches .md and .ipynb files from specified URLs and consolidates them into a single markdown file `context_store.md`.
- `config.py`: Stores the user's OpenAI API key.
- `context_store.md`: Stores all the .md and .ipynb content being used by the Universal Sentence Encoder and GPT-3.5-turbo to generate responses.
- `requirements.txt`: Lists all necessary python packages for the application.

## Future Work

While pgGPT_v0 has been built to provide precise, relevant, and comprehensive answers, future iterations will aim to make the application more interactive and conversational. Stay tuned for updates and improvements!
