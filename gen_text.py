import numpy as np
import pandas as pd


import torch
import transformers
import textwrap

if torch.cuda.is_available():    
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
 
model = torch.load('dostoevsky1_model.pt', map_location=torch.device('cpu'))
# /Users/Muminsho/dostoevsky_bot/dostoevsky1_model.pt
# home/centos/tg_bot/dostoevsky1_model.pt

from transformers import GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('sberbank-ai/rugpt3small_based_on_gpt2')

def generate(prompt):
    generated = tokenizer.encode(prompt, return_tensors='pt') #.to(device)
    out = model.generate(input_ids=generated, max_length=120, temperature=1.,
        num_beams=7, do_sample=True, top_k=50, top_p=0.5,
        no_repeat_ngram_size=2, num_return_sequences=1,
        ).cpu().numpy()

    sequence = tokenizer.decode(*out)
    return sequence

# def generate(prompt, len_gen=120, temperature=0.7, num_beams=5, top_p=0.6, top_k=70,
#              no_repeat_ngram_size=2):
#     generated = tokenizer.encode(prompt)
#     context = torch.tensor([generated]).to(device)
#     past = None

#     for i in range(len_gen):
#         output, past = model(context, past_key_values=past).values()
#         # token = torch.argmax(output[..., -1, :], dim=-1)
#         output = output / temperature
#         token = torch.distributions.Categorical(logits=output[..., -1, :]).sample()
        
#         generated += token.tolist()
#         context = token.unsqueeze(0)

#     sequence = tokenizer.decode(generated)

#     return sequence