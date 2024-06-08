# import logging
# import os
#
# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
# from huggingface_hub import login
# from transformers import AutoModelForCausalLM, AutoTokenizer
#
# class LlamaIntegration:
#     def __init__(self, model_name="meta-llama/Meta-Llama-3-8B"):
#         self.logger = logging.getLogger(__name__)
#         self.api_key = os.getenv("Llama_API_KEY")
#         self.model_name = "meta-llama/Meta-Llama-3-8B"
#         self.tokenizer = None
#         self.model = None
#         self.llama_model = None
#         self._set_up()
#
#     def _set_up(self):
#         login(self.api_key)
#         # 모델과 토크나이저 로드
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
#
#         # LangChain을 사용하여 모델 통합
#         # self.llm = HuggingFaceLLM(model=self.model, tokenizer=self.tokenizer)
#
#     def generate_response(self, message):
#         template = """
#         Question: {question}
#
#         Answer:
#         """
#         prompt = PromptTemplate(template=template, input_variables=["question"])
#         llm_chain = LLMChain(prompt=prompt, llm=self.model)
#         question = message
#         response = llm_chain.run(question)
#         return response
