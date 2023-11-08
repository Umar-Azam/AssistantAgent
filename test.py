import os
import openai
from openai import OpenAI

# %%
client = OpenAI()
client.api_key = os.environ.get('OPENAI_API_KEY')

print(f'Key is {client.api_key}')
