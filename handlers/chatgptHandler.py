import openai
from config import Config

# Set up a connection to the OpenAI API
openai.api_key = Config.OPENAI_API_KEY

# Define a function to send a message to the GPT-3 API and retrieve a response
def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.2,
    )
    res = response.choices[0].text
    return ' '.join(res.strip().split())
