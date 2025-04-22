# transformers it's a library for LMs
from transformers import AutoTokenizer, AutoModelForCausalLM # tokenizer auto load and auto model type for LMs
from textwrap import wrap 
import torch # data processing lib
from functools import lru_cache # least recently used cache: use the last result if its the same arguments
import re

@lru_cache(maxsize=1) # max memory cache 
def load_model():
    model_name = 'TucanoBR/Tucano-1b1'
    tokenizer = AutoTokenizer.from_pretrained(model_name) # text to token
    model = AutoModelForCausalLM.from_pretrained(model_name)  # token processing
    # Tucano is a series of decoder-transformers natively pretrained in Portuguese.
    # In this link you can check this used model https://huggingface.co/TucanoBR/Tucano-1b1
    return tokenizer, model

def text_to_block(doc_text, max_length=450): # separate texts if they are very long for better processing
    return wrap(doc_text, width=max_length, break_long_words=False, replace_whitespace=False)

def split_in_sections(text):
    sections = {} # storage the split sections
    actual = None # storage the actual filled section
    buffer = [] # temporary storage for actual section lines

    for line in text.split('\n'):
        line = line.strip()
        if re.match(r'^#{1,3} ', line): # detect if matches a title in the line
            if actual: # if it's in an actual filling section, join the buffer content as section text
                sections[actual] = '\n'.join(buffer).strip() # save in sections
            actual = line.lstrip('#').strip() # remove the '#' for getting a clean text
            buffer = [] # empty the buffer for a new section reading 
        else: # if its not a title, storage in buffer
            buffer.append(line)
    if actual:
        sections[actual] = '\n'.join(buffer).strip() # also save the last section 
    return sections

def generate_sections(base_text: str, topic: str) -> str:
    tokenizer, model = load_model()
    prompt_pt = f"""Você é um especialista em documentação técnica.
Com base no conteúdo a seguir, escreva uma nova seção com o tópico "{topic}":
{base_text}"""

    input_ids = tokenizer.encode( # encode: make token sequence
        prompt_pt, 
        return_tensors="pt", # return_tensors: pytorch tensor for token format definition
        truncation=True, # truncation: separate text if its too long
        max_length=512
        )
        
    output_ids = model.generate(
        input_ids,
        max_new_tokens=512, # generated text result size. can be modified as you wish.
        temperature=0.7, # control the 'creativity' of the answer
        top_p=0.95, # control the text result choose
        no_repeat_ngram_size=2, # avoid word repeat
        num_beams=4, # let the model search more possibilities of answers
        do_sample=True, # allow to don't make the same text for the same prompt
        early_stopping=True # allow early finishing generation if the model completes with a good answer
    )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # decode:token to text | token_result:the first result being choose | skip_special_tokens:remove special tokens 
    return output_text.replace(prompt_pt, '').strip()
    
def full_doc_sections(base_text: str, topic: str) -> str:
    sections = split_in_sections(base_text)
    result = '# Generated Document\n\n'

    for title, text in sections.items():
        print(f'Generating section: {title}')
        new_section = generate_sections(text, title)
        result += f"## {title}\n\n{new_section}\n\n"

    return result.strip() #return generated text