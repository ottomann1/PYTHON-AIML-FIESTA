import openai
from api_secrets import OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
response = openai.Image.create(
    prompt="Draven from league of legends crying",
    n=1,
    size="256x256"
)
image_url = response['data'][0]['url']
