import sys


#Declaração dos registradores de controle
MAR = ""
MBR = ""
IR = ""
PC = 0

#Declaração dos registradores aritmeticos
MQ = 0
R = 0
AC = 0
C = 0
Z = 0



def procuraEnd(endereco):
    endereco = str(endereco).strip("\n").strip("|")
    arq = open("RAM",'r')
    palavra = arq.readline().split(" ")
    while palavra:
        if palavra[0] == endereco:
            return palavra, offset
        elif palavra[0] == "":
            return "", offset
        else:
            offset = arq.tell()
            palavra = arq.readline().split(" ")

def ehEndereco(palavra):
    if palavra[:2] == '0x':
        return True
    else:
        return False

def VerificaEnd(palavra):
    if palavra[0] == "-":
        if palavra[1] == "|":
            if palavra[2] == 'M':
                return "-|D"
            else:
                return "-|I"
        elif palavra[1] == 'M':
            return "-D"
        else:
            return "-I"
    elif palavra[0] == "|":
        if palavra[1] == 'M':
            return "|D"
        else:
            return "|I"
    elif palavra[0] == 'M':
        return "D"
    else:
        return "I"

def exibeRegistrador():
    print("PC: "+ str(PC).strip("\n"))
    print("MAR: "+MAR.strip("\n"))
    print("IR: "+IR.strip("\n"))
    print("MBR: "+str(MBR).strip("\n"))
    print("AC: "+str(AC).strip("\n"))
    print("MQ: "+str(MQ).strip("\n"))
    print("C: "+str(C).strip("\n"))
    print("R: "+str(R).strip("\n"))
    print("Z: "+str(Z).strip("\n"))
    print("\n")



def loadOp(palavra):
    global MBR, MAR, IR, PC, MQ, AC
    palavra = palavra.split(',')
    if len(palavra) == 1:
        if palavra[0] == "MQ":
            AC = MQ
        elif VerificaEnd(palavra[0]) == 'I':
            AC = palavra[0]
        
        elif VerificaEnd(palavra[0]) == 'D':
            AC = procuraEnd(palavra[0][1:])[0]
            AC = int(AC[1])
        
        elif VerificaEnd(palavra[0]) == '-I':
            AC = str(int(palavra[0]))
        
        elif VerificaEnd(palavra[0]) == '-D':
            AC, nulo = str(-int(procuraEnd(palavra[0][2:])[1]))
        
        elif VerificaEnd(palavra[0]) == '|I':
            palavra = palavra[0][1:].strip("\n").strip("|")
            AC = str(abs(int(palavra)))
        
        elif VerificaEnd(palavra[0]) == '|D':
            AC, nulo = str(abs(int(procuraEnd(palavra[0][2:])[1])))
        
        elif VerificaEnd(palavra[0]) == '-|I':
            palavra = palavra[0][2:].strip("\n").strip("|")
            AC = str(-abs(int(palavra)))
        
        elif VerificaEnd(palavra[0]) == '-|D':
            AC, nulo = str(-abs(int(procuraEnd(palavra[0][3:])[1])))
                
    elif palavra[0] == 'MQ':
        
        if VerificaEnd(palavra[1]) == 'I':
            MQ = palavra[1]
            
        elif VerificaEnd(palavra[1]) == 'D':
            MQ, nulo = procuraEnd(palavra[1][1:])[1]
            
        elif VerificaEnd(palavra[1]) == '-I':
            MQ = str(int(palavra[1]))
            
        elif VerificaEnd(palavra[1]) == '-D':
            MQ, nulo = str(-int(procuraEnd(palavra[1][2:])[1]))
            
        elif VerificaEnd(palavra[1]) == '|I':
            MQ = str(abs(int(palavra[1])))
            
        elif VerificaEnd(palavra[1]) == '|D':
            MQ, nulo = str(abs(int(procuraEnd(palavra[1][2:])[1])))
            
        elif VerificaEnd(palavra[1]) == '-|I':
            MQ = str(-abs(int(palavra[1])))
            
        elif VerificaEnd(palavra[1]) == '-|D':
            MQ, nulo = str(-abs(int(procuraEnd(palavra[1][3:])[1])))
            
def storOp(palavra):
    arq = open("RAM", 'r+')
    ender = palavra[2][1:]
    nulo, pos = procuraEnd(ender)
    arq.seek(pos)
    palavramem = arq.readline()
    palavramem = palavramem.split(" ")
    palavramem[1] = str(AC)
    palavramem = palavramem[0] + " " + palavramem[1]
    arq.seek(pos)
    arq.write(palavramem)
    arq.flush()

def addOp(palavra):
    #FAZER CASOS DE ENDEREÇAMENTO IMEDIATO
    global AC
    valor = procuraEnd(palavra[2][1:])[0]
    AC = AC + int(valor[1])
                     
            
            
#TEM  ARRUMAR ISSO DEPOIS TAMO SÓ FAZENDO AS FUNLÇOES FUNCIONAREM
def leMemoria():
    global MBR, MAR, IR, PC
    arq = open("RAM","r")
    palavra = arq.readline().split(" ")
    while palavra[0]:
        if ehEndereco(palavra[1]):
            PC = palavra[1]
            MAR = palavra[1]
            MBR = palavra[1:]
            exibeRegistrador()
            palavra, nulo = procuraEnd(PC.strip('\n'))
        elif palavra[1] == 'LOAD':
            IR = 'LOAD'
            loadOp(palavra[2])
            exibeRegistrador()
            PC = str(hex(int(PC,16) + 1))
            palavra, nulo = procuraEnd(PC)
        elif palavra[1] == 'STOR':
            IR = 'STOR'
            storOp(palavra)
            PC = str(hex(int(PC,16) + 1))
            palavra, nulo = procuraEnd(PC)
        elif palavra [1] == 'ADD':
            IR = 'ADD'
            addOp(palavra)
            PC = str(hex(int(PC,16) + 1))
            palavra, nulo = procuraEnd(PC)
        #elif palavra[1] == 'SUB':
            #IR = 'SUB'
            #subOp(palavra)
        #elif palavra[1] == 'MUL':
            #IR = 'MUL'
            #mulOp(palavra)
        #elif palavra[1] == 'DIV':
            #IR = 'DIV'
            #divOp(palavra)
        else:
            palavra = arq.readline().split(" ")
        try:
            verdade, nulo = procuraEnd(PC)
            if PC != 0 and verdade == "":
                break
        except IndexError:
            break
            
            
    arq.close()



if __name__ == "__main__":
    exibeRegistrador()
    leMemoria()