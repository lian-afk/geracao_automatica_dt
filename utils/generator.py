from transformers import AutoTokenizer, AutoModelForSeq2SeqLM # huggingface LLM
from textwrap import wrap 
import torch # data processing lib

tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab") # text to token
model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/ptt5-base-portuguese-vocab")  # token processing
# 'unicamp-dl/ptt5-base-portuguese-vocab' its a portuguese vocabulary pretrained model
# link for the model page: https://huggingface.co/unicamp-dl/ptt5-large-portuguese-vocab

def text_to_block(doc_text, max_length=450): # separate texts if they are very long for better processing
    return wrap(doc_text, width=max_length, break_long_words=False, replace_whitespace=False)

def generate_section(base_text: str, topic: str) -> str: # get base text and desired topic for generation
    prompt_pt = f"Crie uma nova seção técnica com foco em '{topic}' com base no seguinte texto: {base_text}"

    tokens = tokenizer.encode( # encode: make token sequence
        prompt_pt, 
        return_tensors="pt", # return_tensors: pytorch tensor for token format definition
        truncation=True, # truncation: separate text if its too long
        max_length=512
        )
        
    token_result = model.generate(
        tokens,
        max_length=512, # generated text result size. can be modified as you wish.
        num_beams=5, # text generation tester and best result choosing
        temperature=0.7, # avoid generic and random answers
        top_p=0.9, # control the text result choose together with 'temperature'
        no_repeat_ngram_size=2, # avoid constant word repeat
        early_stopping=True # instant generation if the best result is found
    )

    result = tokenizer.decode(token_result[0], skip_special_tokens=True)
    # decode:token to text | token_result:the first result being choose | skip_special_tokens:remove special tokens 
    return result #return generated text