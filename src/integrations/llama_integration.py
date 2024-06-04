import logging
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler # 출력을 스트리밍하는 데 사용
from langchain_community.llms import Ollama

class LlamaIntegration:
    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B"):
        self.logger = logging.getLogger(__name__)
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Ollama(model="llama2")


    def generate_response(self, message):
        template = """
        Question: {question}

        Answer:
        """
        prompt = PromptTemplate(template=template, input_variables=["question"])
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        question = message
        response = llm_chain.run(question)
        return response
