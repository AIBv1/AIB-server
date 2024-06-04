from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os

class ChatGPTIntegration:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.llm = OpenAI(openai_api_key=api_key)

    def create_prompt_template(self):
        template = """Question: {question}
        Answer: Let's explain calories of food step by step."""

        return PromptTemplate(template=template, input_variables=["question"])

    def generate_response(self, message):
        prompt = self.create_prompt_template()
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        question = message
        response = llm_chain.run(question)
        return response

