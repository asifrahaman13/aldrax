from openai import Client
from src.constants.prompts.prompts import Prompt


class OpenAIRepository:
    def __init__(self, openai_client: Client):
        self.openai_client = openai_client

    def get_llm_response(self, prompt: str) -> str:
        completion = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": Prompt.get_prompt()},
                {"role": "user", "content": f"The user prompt is: {prompt}"},
            ],
        )

        result = completion.choices[0].message.content.strip("```sql\n").strip("```")
        return result