import easyocr


def recognize_text(img_path):
    reader = easyocr.Reader(['en'])
    textFinal = []
    texts = reader.readtext(img_path)
    for text in texts:
      textFinal.append(text[1])
    print(textFinal)
    
recognize_text('/home/rodrigo/Documents/Adflow2/Inputs/Tue Mar 15 19-31-28 2022.jpg')

