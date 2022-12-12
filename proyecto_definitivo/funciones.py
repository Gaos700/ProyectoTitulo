def verificacionLetras(texto):# [A][B][C][D][-][1][0]
    letras= ['B','C','D','F','G','H','J','K','L','P','R','S','T','V','W','X','Y','Z'] #las PPU utilizan estas 18 letras
    if texto[0] and texto[1] in letras:
        return True
def verificacionNumeros(texto):
    numeros= ['1','2','3','4','5','6','7','8','9','0']
    if texto[6] and texto[7] in numeros:
        return True
def removerString(texto):
    a = list(texto)
    a.pop(2)
    a.pop(4)
    salida = "".join(a)
    return salida




    