import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

model_id = os.getenv("CLAUDE_MODEL")

response=client.messages.create(
    model=model_id,
    max_tokens=500,
    system="당신은 산업단지 기술자원 엔지니어야",
    messages=[{"role": "user", "content": "너는 어떤 내용을 말해 줄수 있어?"}]
)

texts = [block.text for block in response.content if block.type == "text"]
answer = "\n".join(texts)
