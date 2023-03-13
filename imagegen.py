import openai
from api_secrets import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
response = openai.Image.create(
    prompt="cats",
    n=1,
    size="256x256"
)
image_url = response['data'][0]['url']
