import openai
from config import Config

# Set up a connection to the OpenAI API
openai.api_key = Config.OPENAI_API_KEY

# Define a function to send a message to the GPT-3 API and retrieve a response
def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text

def check_relativity(message):
    prompt = f"{message}. Is this sentence related to clothings ?. return 'Y' or 'N' as answer."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    res = response.choices[0].text
    return ' '.join(res.strip().split())
