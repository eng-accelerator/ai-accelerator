# Introduction to Hugging Face and Using its Models

Welcome to this session on using Hugging Face models! This guide is designed to introduce you to the world of Hugging Face and empower you to leverage its powerful tools and pre-trained models for various machine learning tasks.

## What is Hugging Face?

Hugging Face is an open-source platform that has revolutionized the field of Natural Language Processing (NLP) and is rapidly expanding into other domains like computer vision and audio. Its core mission is to democratize access to cutting-edge machine learning models and tools, making it easier for everyone to build and deploy AI applications.

Think of Hugging Face as a central hub for the ML community, offering:

*   **A vast Model Hub:** A repository of thousands of pre-trained models for various tasks, contributed by researchers and developers worldwide. You can find models for text classification, translation, summarization, image recognition, audio transcription, and much more.
*   **Powerful Libraries:** Open-source libraries like `transformers`, `datasets`, and `tokenizers` that provide easy-to-use interfaces for working with models, datasets, and text processing.
*   **A Collaborative Community:** A vibrant community of ML practitioners who share models, datasets, and expertise.

Hugging Face significantly reduces the barrier to entry for using state-of-the-art ML models, allowing you to quickly experiment and build applications without having to train models from scratch.

## Managing Hugging Face Tokens

To access some models or features on the Hugging Face Hub, you might need to use an API token. This token helps authenticate your requests and can be used to interact with the Hub programmatically, including downloading gated models or uploading your own.

Here's how you can manage and verify your Hugging Face token:

1.  **Obtain a Token:** Go to your Hugging Face profile settings (https://huggingface.co/settings/tokens) and generate a new access token. You can choose different roles for the token (e.g., read, write).
2.  **Store your Token Securely:** It's crucial to store your token securely. In Google Colab, you can use the "Secrets" feature (🔑 icon in the left panel) to store your token as an environment variable. Name your secret `HF_TOKEN`.
3.  **Log in Programmatically:** You can use the `huggingface_hub` library to log in to the Hugging Face Hub using your token.

Let's add a code block to install the necessary library and verify your token.

!pip install huggingface_hub

from huggingface_hub import whoami
from google.colab import userdata

# Get your Hugging Face token from Colab Secrets
hf_token = userdata.get('HF_TOKEN')

# Verify the token by checking your identity
try:
    user_info = whoami(token=hf_token)
    print(f"Logged in as: {user_info['name']}")
except Exception as e:
    print(f"Could not log in: {e}")
    print("Please make sure you have added your Hugging Face token to Colab Secrets with the name 'HF_TOKEN'")

## Showcasing Different Model Types

Hugging Face isn't just about text! Let's explore how to use models for other modalities like images and audio, and also how to work with datasets.

### Image Classification

Image classification is the task of categorizing an image into one of several classes. We can use a pre-trained image classification model from the Hugging Face Hub.

from transformers import pipeline
from PIL import Image
import requests

# Load an image classification pipeline
classifier = pipeline("image-classification")

# Get an image from a URL (replace with your image URL)
url = "https://i.guim.co.uk/img/media/327aa3f0c3b8e40ab03b4ae80319064e401c6fbc/377_133_3542_2834/master/3542.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=34d32522f47e4a67286f9894fc81c863"
image = Image.open(requests.get(url, stream=True).raw)

# Classify the image
predictions = classifier(image)

print("Image Classification Results:")
for prediction in predictions:
    print(f"- {prediction['label']}: {prediction['score']:.2f}")

### Audio Classification

Audio classification is the task of categorizing audio data into different classes, such as identifying the type of sound or the speaker's emotion.

from transformers import pipeline
import torch
import soundfile as sf

# Load an audio classification pipeline
# We use a smaller model for demonstration purposes
classifier = pipeline("audio-classification", model="superb/wav2vec2-base-superb-ks")

# This is a simple sine wave, you would load your actual audio data
dummy_audio = torch.randn(16000) # 1 second of dummy audio at 16kHz
sf.write("dummy_audio.wav", dummy_audio.numpy(), 16000)


# Classify the audio
audio_file = "dummy_audio.wav"
predictions = classifier(audio_file)

print("Audio Classification Results:")
for prediction in predictions:
    print(f"- {prediction['label']}: {prediction['score']:.2f}")

### Working with Datasets

Hugging Face provides the `datasets` library, which makes it easy to access and work with a wide variety of datasets for various ML tasks.

from datasets import load_dataset

# Load a dataset (e.g., the SQuAD dataset for question answering)
dataset = load_dataset("squad")

# Print information about the dataset
print(dataset)

# Access an example from the training set
print("\nExample from the training set:")
print(dataset["train"][0])

## Introduction to Gradio

Gradio is an open-source Python library that allows you to quickly create customizable UI components for your machine learning models. It's a great way to build interactive demos and share your models with others.

While we won't cover Gradio in detail in this Colab, it's a valuable tool for building user interfaces for the Hugging Face models we'll be using. You can learn more about Gradio in a separate Colab notebook dedicated to it. We will, however, use it in our final assignment to build a simple demo.

## Transcription with Hugging Face

Audio transcription is the task of converting spoken language into text. Hugging Face also offers models for this task.

Here's how you can use a pre-trained model for audio transcription:

from transformers import pipeline
import soundfile as sf
import torch

# Load the automatic speech recognition pipeline
transcriber = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

# This is just for demonstration purposes. In a real scenario, you would load your audio file.
# audio_data = "/content/Durga Nagar Road 3.m4a" # Dummy data for 1 second of audio at 16kHz
# sf.write("/content/Durga Nagar Road 3.m4a", audio_data, 16000)

# Transcribe the audio
audio_file = "/content/Durga Nagar Road 3.m4a"
transcription = transcriber(audio_file)

print("Transcription:")
print(transcription['text'])

## Summarization with Hugging Face

Text summarization is the task of creating a shorter version of a text while preserving its main ideas. Hugging Face provides several models that can be used for this purpose.

Here's how you can use a pre-trained model from Hugging Face for summarization:

from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

# Text to summarize
text = """
Hugging Face is a company and open-source platform that provides tools and models for natural language processing (NLP). It has become a central hub for the ML community, offering a wide range of pre-trained models that can be easily used or fine-tuned for specific applications. Key aspects of Hugging Face include the Transformers library, Model Hub, Datasets library, and Tokenizers library. Hugging Face democratizes access to powerful ML models, making it easier for developers and researchers to build and deploy applications.
"""

# Summarize the text
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)

print("Original Text:")
print(text)
print("\nSummary:")
print(summary[0]['summary_text'])
