import sys
#Iniciando as váriaveis da ULA
MBR = 0
MQ = 0
AC = 0
C = 0
#Iniciando as variávies da UC
PC = 0
IR = 0
MAR = 0
#Constante para tamanho de memoria
TAM_MEM = 4
#O programa suportará do valor 9999 ao -999, qualquer valor fora desse intervalo é dado como over ou underflow

#Registradores extras:
MPO = 0 #Memory Pointer, utilizador para apontar, incrementar e armazenar endereços de memória (em sí).
#Lista da Ram completa
ramList = []


def ehEndereco(palavra):
    if palavra[:2] == '0x':
        return True
    else:
        return False

def ehInteiro(inteiro):
    try:
        if inteiro[:2] == '-|':
            int(inteiro[2:].strip("|"))
        elif inteiro[:1] == '|':
            print("entrou aqui")
            int(inteiro[1:].strip("|"))
            print(inteiro)
        else:
            int(inteiro)

        return True
    except ValueError:
        return False


def procuraEnd(barramentoEnd):
    barramentoEnd = int(barramentoEnd, 16)
    barramentoDadoA = ramList[barramentoEnd].split(" ")
    barramentoDadoB = []
    for i in barramentoDadoA:
        barramentoDadoB.append(i.replace("\n", ""))
    return barramentoDadoB[1:]


def escreveRamList():
    with open("RAM", 'w+') as ram:
        for i in range(len(ramList)-1):
            ram.write(ramList[i])

def guardaEndMPO(barramentoEnd, barramentoDadoA):
    global ramList
    barramentoDadoB = ""
    barramentoEnd = int(barramentoEnd, 16)
    barramentoDadoB = ramList[barramentoEnd]
    barramentoDadoB = barramentoDadoB.split(" ")
    barramentoDadoB[1] = barramentoDadoA+"\n"
    barramentoDadoA = " ".join(barramentoDadoB)
    ramList[barramentoEnd] = barramentoDadoA
    

def guardaEnd(barramentoEnd, barramentoDadoA):
    global ramList
    barramentoDadoB = ""
    barramentoEnd = int(barramentoEnd, 16)
    barramentoDadoB = ramList[barramentoEnd]
    barramentoDadoB = barramentoDadoB.split(" ")
    memsobra = TAM_MEM-len(str(barramentoDadoA))
    if memsobra < 0:
        print(OverflowError)
    else:
        barramentoDadoB[1] = str(0)*memsobra+str(barramentoDadoA)+"\n"
        barramentoDadoA = " ".join(barramentoDadoB)
        ramList[barramentoEnd] = barramentoDadoA
    
    
    
    
    

def leMem():
    global ramList, PC
    with open("RAM", "r+") as ram:
        ramList = ram.readlines()
    PC = '0x14'
    buscaOp(ramList)
        
        
def buscaOp(ramList):
    global MAR, MBR, IR, PC
    MAR = PC
    #exibeRegistradores("Antes do inicio do programa")
    MBR = procuraEnd(MAR)
    while MBR[0] != 'EXIT': #Se for EXIT é o fim do programa
        PC = str(hex(int(PC,16)+1))
        #exibeRegistradores("Dentro da Busca")
        decodificaOp()
        MAR = PC
        MBR = procuraEnd(MAR)
    
    escreveRamList()       


def decodificaOp():
    global MBR, MAR, IR
    

    for carac in range(len(MBR[1])):
        if MBR[1][carac] == '(':
            IR = [MBR[0], MBR[1][:carac]]
            if MBR[1][carac:].strip("(").strip(")").strip("|").strip(")") == 'MPO':
                MAR = MPO
                print("entrou")
            else:
                MAR = MBR[1][carac:].strip("\n").strip("(").strip(")").strip("|").strip(")")
        
        elif MBR[1] == "MQ":
            IR = [MBR[0], MBR[1]]
        elif MBR[1] == "MPO":
            IR = [MBR[0], MBR[1]]
        elif MBR[1][:3] == "MQ,":
            parte = MBR[1].split(",")
            if ehInteiro(parte[1]):
                IR = [MBR[0], parte[0], parte[1]]
        elif ehInteiro(MBR[1]):
            IR = [MBR[0], MBR[1]]
            
    executaOp()
            
            



def executaOp():
    global IR, MAR, MBR, AC, MQ, PC, MPO
    print(f"primeiro ir {IR}")
    #IR = IR.split(" ")
    print(f"segundo ir {IR}")
    if IR[0] == "LOAD": #IF para os respectivos LOADS permitidos
        if IR[1] == "MQ": #Se apenas MQ no parametro o AC recebe MQ
            AC = MQ
        elif IR[1] == "M": #Se apenas M no parametro AC recebe M
            MBR = procuraEnd(MAR) #MBR recebe o endereço especificado pelo MAR (repete em basicamente todos)
            if ehEndereco(MBR[0]):
                MPO = MBR[0]
            else:
                MBR = MBR[0]
                AC = int(MBR) #AC recebe MBR (repete em basicamente todos)
        elif IR[1] == "MPO,M":
            MPO = MAR
            print("entrou")
        elif IR[1] == "-M": 
            MBR = procuraEnd(MAR)[0]
            AC = -int(MBR[0])
            
        elif IR[1] == "|M":
            MBR = procuraEnd(MAR)[0]
            AC = abs(int(MBR[0]))
            
        elif IR[1] == "-|M":
            MBR = procuraEnd(MAR)[0]
            AC = -abs(int(MBR[0]))
        #fazer uma verificacao para nao entrar direto no indireto so colocar um and tipo ser diferente de -|M para entrar 
        elif IR[1].isdigit():
            AC = int(MBR[1])
        
        elif IR[1][:1] == '-' and not IR[1][:2] == "-|" and not IR[1][2] == "M":
            AC = int(MBR[1])

        elif IR[1][:1] == "|" and not IR[1][2] == "M":
            c = MBR[1].strip("|")
            AC = abs(int(c))

        elif IR[1][:2] == "-|" and not IR[1][2] == "M":
            c = MBR[1].strip("-").strip("|").strip("|")
            AC = -abs(int(c))

        elif IR[1].split(",")[1].isdigit():
            MBR = MBR[1].split(",")
            MQ = int(MBR[1])

        elif IR[1].split(",")[1][:1] == "-" and not IR[1].split(",")[1][:2] == "-|" and not IR[1][3] == "M":
            MBR = MBR[1].split(",")
            MQ = int(MBR)

        elif IR[1].split(",")[1][:1] == "|" and not IR[1][2] == "M":
            MBR = MBR[1].split(",")
            c = MBR.strip("|")
            MQ = abs(int(c))

        elif IR[1].split(",")[1][:2] == "-|" and not IR[1][3] == "M":
            MBR = MBR[1].split(",")
            c = MBR.strip("-").strip("|").strip("|")
            MQ = -abs(int(c))

        elif IR[1].split(",")[1] == "M": #abaixo e esse são os casos para parametros do tipo MQ,M(x), para o carregamento da memoria para o MQ
            MBR = procuraEnd(MAR)[0]
            MQ = int(MBR[0])
            
        elif IR[1].split(",")[1] == "-M":
            MBR = procuraEnd(MAR)[0]
            MQ = -int(MBR[0])
            
        elif IR[1].split(",")[1] == "|M":
            MBR = procuraEnd(MAR)[0]
            MQ = abs(int(MBR[0]))
            
        elif IR[1].split(",")[1] == "-|M":
            MBR = procuraEnd(MAR)[0]
            MQ = -abs(int(MBR[0]))

    elif IR[0] == "STOR": #ARMAZENAMENTO DO DADO GUARDADO EM AC NO ESPAÇO DE MEMÓRIA ESPECIFICADO EM M(X)
        if IR[1] == "MPO,M":
            #Guardar no MAR o que esta contido em MPO
            guardaEndMPO(MAR, MPO)
        else:
            MBR = AC
            guardaEnd(MAR, MBR)
        
    elif IR[0] == "ADD": #ADIÇÃO DO AC PELO DADO PASSADO POR M(X)
        
        if IR[1] == "MPO":
            MPO = str(hex(int(MPO,16)+1))
        else:
            if ehInteiro(IR[1]):
                MBR = IR[1]
                AC = int(AC) + int(MBR)
                if AC > 9999:
                    C = 1
                    AC = AC - 10000
                else:
                    C = 0
            else:
                MBR = procuraEnd(MAR)[0] #obtenção
                AC = int(AC) + int(MBR[0])
                if AC > 9999:
                    C = 1
                    AC = AC - 10000
                else:
                    C = 0
            
    elif IR[0] == "SUB": #Subtração do AC pelo dado passado por M(X)
        
        if IR[1] == "MPO":
            MPO = str(hex(int(MPO,16)-1))
        else:
            if ehInteiro(IR[1]):
                MBR = IR[1]
                AC = int(AC) - int(MBR)
                if AC < -999:
                    C = 1
                    AC = AC + 10000
                else:
                    C = 0
            else:
                MBR = procuraEnd(MAR) #obtenção
                AC = int(AC) - int(MBR[0])
                if AC < -999:
                    C = 1
                    AC = AC + 10000
                else:
                    C = 0
            
    elif IR[0] == "MUL": #multiplicação do MQ pelo dado passado por M(X)
        
        if ehInteiro(IR[1]):
            MBR = IR[1]
            MQ = int(MQ) * int(MBR)
            if AC > 9999:
                C = 1
                AC = AC - 10000
            else:
                C = 0
        else:
            MBR = procuraEnd(MAR)[0] #obtenção do dado e salvamento no MBR
            MQ = int(MQ) * int(MBR[0])
            if AC > 9999:
                C = 1
                AC = AC - 10000
            else:
                C = 0
            
    elif IR[0] == "DIV": #Divisão do dado passado pela memória M(X)
         
        if ehInteiro(IR[1]):
            MBR = IR[1]
            AC = int(int(MQ) // int(MBR)) #guardando o quociente em AC
            MQ = int(MQ) % int(MBR) #guardando o resto em MQ
        else:
            MBR = procuraEnd(MAR) #obtenção do dado e salvamento no MBR
            AC = int(int(MQ) // int(MBR[0])) #guardando o quociente em AC
            MQ = int(MQ) % int(MBR[0]) #guardando o resto em MQ


    elif IR[0] == "+JUMP":#Nas funções de JUMP apenas o PC é atribuido ao MAR (endereço passado pelo M(x))
        if int(AC) >= 0:
            PC = MAR
    elif IR[0] == "-JUMP":
        if int(AC) <= 0:
            PC = MAR
    elif IR[0] == "JUMP":
            PC = MAR 
    #exibeRegistradores("Fim da Execução")
            
      
leMem()