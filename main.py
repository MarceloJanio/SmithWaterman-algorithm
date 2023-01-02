file = open("input.txt", "r")

save_data = []

for i in file:
    save_data.append(i.split("\n")[0])

#print(save_data)

def criaMatriz(seq1, seq2):
    matriz = []
    seq1 = seq1[::-1]
    for i in seq1:
        templist = [i]
        [templist.append(None) for j in range(0,len(seq2)+1)]
        matriz.append(templist)
    templist = ["-"]
    [templist.append(None) for j in range(0,len(seq2)+1)]
    matriz.append(templist)
    templist = ["start", "-"]
    [templist.append(i) for i in seq2]
    matriz.append(templist)
    return [matriz, len(seq1)+2, len(seq2)+2]

matriz = criaMatriz(save_data[0], save_data[1])


def inicializaMatriz(matriz, gapValue):
    nLin = int(matriz[1])
    nCol = int(matriz[2])
    matriz = matriz[0]
    matriz[-2][1] = [0, '','', 'stop']
    for i in range(nLin-3, -1,-1):
        matriz[i][1] = [int(matriz[i+1][1][0]) + int(gapValue), i+1, 1, "baixo"]
    for i in range(2, nCol, 1):
        matriz[-2][i] = [int(matriz[-2][i-1][0]) + int(gapValue), nLin-2, i, "esq"]
    return (matriz, nLin, nCol) 

inicializaMatriz(matriz, save_data[-1])

def calculaCasa(matriz, match, missmatch, gap, posLin, posCol):

    diag = None
    if(matriz[posLin][0][0] == matriz[-1][posCol][0]):
        diag = matriz[posLin+1][posCol-1][0] + match
    else:
        diag = matriz[posLin+1][posCol-1][0] + missmatch
    maior = [diag, posLin+1, posCol-1, "diag"] 

    esq = matriz[posLin][posCol-1][0] + gap

    if(esq > maior[0]):
        maior = [esq, posLin, posCol-1, "esq"] 
    baixo = matriz[posLin+1][posCol][0] + gap
    if(baixo>maior[0]):
        maior = [baixo, posLin+1, posCol, "baixo"] 
    return maior


for i in range(matriz[1]-3, -1, -1):
    for j in range(2, matriz[2], 1):
        matriz[0][i][j] = calculaCasa(matriz[0], int(save_data[2]), int(save_data[3]), int(save_data[4]), i, j)

def findScore(matriz, nLin, nCol):
    score = matriz[0][1][0]
    for i in range(2, nCol):
        if(matriz[0][i][0]>score):
            score = matriz[0][i][0]
    for i in range(1, nLin-1):
        if(matriz[i][-1][0]>score):
            score = matriz[i][-1][0]
    return score

scoreFinal = findScore(matriz[0], matriz[1], matriz[2])

def backTrace(matriz, nLin, nCol):
    colIni = nCol-1
    linIni = 0
    primSeq = []
    segSeq = []
    while(True):
        if(matriz[linIni][colIni][-1] == "diag"):
            primSeq.append(matriz[linIni][0])
            segSeq.append(matriz[nLin-1][colIni])
        elif(matriz[linIni][colIni][-1] == "baixo"):
            primSeq.append(matriz[linIni][0])
            segSeq.append("-")
        else:
            primSeq.append("-")
            segSeq.append(matriz[nLin-1][colIni])
       
        newCol = matriz[linIni][colIni][-2]
        newLin = matriz[linIni][colIni][-3]
        colIni = newCol
        linIni = newLin
        if(matriz[linIni][colIni][-1] == 'stop'):
            break

    seq1 = ''.join(primSeq[::-1])
    seq2 = ''.join(segSeq[::-1])

    return [seq1, seq2]

seq1Final, seq2Final = backTrace(matriz[0], matriz[1], matriz[2])

for i in matriz[0]:
    print(i)

with open("output.txt", 'w') as file:
    file.writelines([str(seq1Final)+'\n', str(seq2Final)+'\n', str(scoreFinal)+'\n', str(save_data[2])+'\n', str(save_data[3])+'\n', str(save_data[4])])
