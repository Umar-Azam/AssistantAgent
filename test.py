# %%
import os
import openai

# %%
# getting key from file in parent directory.
key = ''

# Reading the content of the file into a variable
# Make sure no newline at the end of openai_key file
with open('../openai_key', 'r') as file:
    key = file.read()

os.environ['OPENAI_API_KEY'] = key

# %%
client = openai.OpenAI()
print(f'Key is {client.api_key}')

# %%
client.files.list()

# %%


def test_func(input1, input2, input3):
    print(f'input1 : {input1}\ninput2 : {input2}\ninput3 : {input3}')


# %%
test_input = {'input1': 'hello', 'input2': 'world', 'input_3': '!'}
# %%
test_func(**test_input)
# %%
