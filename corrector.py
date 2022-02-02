import pandas as pd
import numpy as np
import textdistance
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt
import json
import re
from collections import Counter

 
words = [] 
 
with open('ingles.txt', 'r') as f:
    file_name_data = f.read()
    file_name_data=file_name_data.lower()
    words = re.findall('\w+',file_name_data)
 
# This is our vocabulary
V = set(words)
 
#print(f"The first ten words in the text are: \n{words[0:10]}")
#print(f"There are {len(V)} unique words in the vocabulary.")

word_freq_dict = {}  
word_freq_dict = Counter(words)  
 
#print(word_freq_dict.most_common()[0:10])

probs = {} 
     
Total = sum(word_freq_dict.values())
     
for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k]/Total


def my_autocorrect(input_word):
    input_word = input_word.lower()
 
    if input_word in V:
        return(input_word)
    else:
        try:
            similarities = [1-(textdistance.Jaccard(qval=2).distance(v,input_word)) for v in word_freq_dict.keys()]
            df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
            df = df.rename(columns={'index':'Word', 0:'Prob'})
            df['Similarity'] = similarities
            output = df.sort_values(['Similarity', 'Prob'], ascending=False ).head()
            output.reset_index(inplace=True, drop=True)
        except :
            return ''
        return(output.iloc[0]['Word'])

#print(my_autocorrect('personal'))

def extract_text(img_path, lng, mod, quant, diccionario, file):
    # load image
    or_img = Image.open(img_path)
    # image transformation
    img = or_img.convert(mode=mod, dither=None) # convert to black and white
    if mod != '1':
        img = img.quantize(colors=quant)
    # extract text
    extracted = pytesseract.image_to_string(img, lang=lng)
    text = extracted        
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')    
    extracted = text    
    palabras = []
    palabras = text.split()
    palabras = [line for line in palabras if line.strip()]
    print(palabras)
    corregidas = []
    corregida = ''
    for palabra in palabras:        
        corregida += str(palabra)+' '    
    diccionario['Extraido'] = palabras
    diccionario['Corregidas'] = corregida  
    with open(file, 'w') as json_file:
        json.dump(diccionario, json_file, indent=4 ,ensure_ascii=False) 
    return palabra, palabras, corregida
