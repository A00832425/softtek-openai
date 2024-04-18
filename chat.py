import os
import pdfplumber
import requests
from getpass import getpass

from softtek_llm.chatbots.chatbot import Chatbot
from softtek_llm.memory import WindowMemory
from softtek_llm.models import SofttekOpenAI
from softtek_llm.embeddings import SofttekOpenAIEmbeddings





# Openai model with Softtek's credentials
softtek_model = SofttekOpenAI(
    api_key="oHq72Gq1FeM08SyHwOR2",
    model_name="InnovationGPT4-Turbo",
)

softtek_embed = SofttekOpenAIEmbeddings(
  model_name= "OpenAIEmbeddings",
  api_key= "oHq72Gq1FeM08SyHwOR2",
)
# We create an empty memory for the chatbot.
# WindowMemory is a special type of memory that stores a limited
# set of messages. When it's full and a new message arrives, older messages are
# removed. We prefer this to save up tokens.
memory = WindowMemory(window_size=10)

# Finally, we instantiate the chatbot
softtek_chatbot = Chatbot(
    model=softtek_model,
    memory=memory,
    verbose=True,
)



def parse(file):
  with pdfplumber.open(file) as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    textRes = 'Dame un resumen de este texto: "' + text + '"'
    response = softtek_chatbot.chat(textRes)
    print(response.message.content)


def download(file):
  url = "https://pdfobject.com/pdf/sample.pdf"

  with open("file.pdf", "wb") as f:
    f.write(requests.get(file).content)
    parse("file.pdf")


def chat():
    print("ChatGPT 4:")
    while True:
        print(" ")
        message = input("> ")
        if message.lower() == "exit()":
            print("Exiting the chatbot")
            break
        elif message.lower() == "parse()":
            f = input("File: ")
            parse(f)
        elif message.lower() == "download()":
            f = input("Link: ")
            download(f)
        else:
            response = softtek_chatbot.chat(message)
            print(response.message.content)


chat()
