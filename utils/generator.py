from transformers import AutoTokenizer, AutoModelForCausalLM
from textwrap import wrap 
import torch # data processing lib

model_name = 'TucanoBR/Tucano-1b1'
tokenizer = AutoTokenizer.from_pretrained(model_name) # text to token
model = AutoModelForCausalLM.from_pretrained(model_name)  # token processing
# Tucano is a series of decoder-transformers natively pretrained in Portuguese.
# In this link you can check this used model https://huggingface.co/TucanoBR/Tucano-1b1

def text_to_block(doc_text, max_length=450): # separate texts if they are very long for better processing
    return wrap(doc_text, width=max_length, break_long_words=False, replace_whitespace=False)

def generate_section(base_text: str, topic: str) -> str: # get base text and desired topic for generation
    prompt_pt = f"Crie uma nova seção técnica com foco em '{topic}' com base no seguinte texto: {base_text}"

    input_ids = tokenizer.encode( # encode: make token sequence
        prompt_pt, 
        return_tensors="pt", # return_tensors: pytorch tensor for token format definition
        truncation=True, # truncation: separate text if its too long
        max_length=512
        )
        
    output_ids = model.generate(
        input_ids,
        max_new_tokens=512, # generated text result size. can be modified as you wish.
        temperature=0.7, # avoid generic and random answers
        top_p=0.9, # control the text result choose together with 'temperature'
        no_repeat_ngram_size=2, # avoid constant word repeat
    )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # decode:token to text | token_result:the first result being choose | skip_special_tokens:remove special tokens 
    result = output_text.replace(prompt_pt, '').strip() # remove the initial prompt if the model duplicates
    return result #return generated text

def full_doc(base_text: str, topic: str) -> str:
    blocks = text_to_block(base_text) # turn the long texts to blocks 
    sections = []

    for i, block in enumerate(blocks):
        section = generate_section(block, topic) # for every block, a section will be separated with that topic
        sections.append(f'## Seção {i+1}\n\n{section}\n') # append all sections into sections list
    
    final_doc = "# Generated Document\n\n" + "\n".join(sections) # join all 
    return final_doc