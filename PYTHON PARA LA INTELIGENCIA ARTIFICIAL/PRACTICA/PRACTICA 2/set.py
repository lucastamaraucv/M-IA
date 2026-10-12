def rle(text):
    resultado=""
    contador=1
    elemento=text[0]
    for recorre in text[1:]:
        if recorre==elemento:
            contador = contador +1
        else:
            resultado+=elemento+str(contador)
            elemento=recorre
            contador =1
    resultado=elemento+str(contador)
    return resultado            




#"d5w2o4d3a3"
#"d5w2o4d3a3"
string = 'dddddwwoooodddaaa'
expected_output = 'd5w2o4d3a3'
output = rle(string)    # This calls your function named rle



