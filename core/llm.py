# from llama_cpp import Llama

# class LLMEngine:
#     def __init__(self, model_path):
#         self.llm = Llama(
#             model_path=model_path,
#             n_ctx=4096,
#             n_threads=8,
#             verbose=False
#         )

#     def stream(self, prompt: str):
#         """
#         Generator that yields tokens as they are produced
#         """
#         for output in self.llm(
#             prompt,
#             max_tokens=512,
#             stream=True,
#             stop=["</s>", "User:"]
#         ):
#             token = output["choices"][0]["text"]
#             if token:
#                 yield token


import os
from llama_cpp import Llama

class LLMEngine:
    def __init__(self, model_path):
        self.llm = Llama(
            model_path=model_path,

            
            n_ctx=2048,           
            n_threads=os.cpu_count(),

            
            n_gpu_layers=35,      
            offload_kqv=True,

           
            use_mlock=True,
            use_mmap=True,

            verbose=False
        )

    def stream(self, prompt: str):
        for out in self.llm(
            prompt,
            max_tokens=256,
            temperature=0.7,
            stream=True,
            stop=["</s>", "User:"]
        ):
            yield out["choices"][0]["text"]
