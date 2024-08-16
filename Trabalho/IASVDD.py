#Iniciando as váriaveis da ULA
MBR = 0
MQ = 0
AC = 0

#Iniciando as variávies da UC
PC = 0
IR = 0
MAR = 0

def procuraEnd(endereco):
    endereco = str(endereco)
    arq = open("RAM",'r')
    palavra = arq.readline().strip("\n").split(" ")
    offset = arq.tell()
    while palavra:
        if palavra[0] == endereco:
            return palavra[1:], offset
        elif palavra[0] == "":
            return "", offset
        else:
            offset = arq.tell()
            palavra = arq.readline().strip("\n").split(" ")


#Procurando a palavra de memória que contenha apenas um endereço
def ehEndereco(palavra):
    if palavra[:2] == '0x':
        return True
    else:
        return False
    
    
def leMem():
    global PC
    with open("RAM","r") as ram:
        achou = False
        while not achou:
            endereco = ram.readline().split(" ")[1]
            if ehEndereco(endereco):
                PC = endereco.strip("\n")
                achou = True
    buscaOp()

def buscaOp():
    global MAR, MBR, IR, PC
    MAR = PC
    exibeRegistradores("Antes do inicio do programa")
    MBR = procuraEnd(MAR)[0]
    while MBR[0] != 'EXIT': #Se for EXIT é o fim do programa
        PC = str(hex(int(PC,16)+1))
        exibeRegistradores("Dentro da Busca")
        decodificaOp()
        MAR = PC
        MBR = procuraEnd(MAR)[0]
    
def decodificaOp():
    global MBR, MAR, IR
    
    
    for carac in range(len(MBR[1])):
        if MBR[1][carac] == '(':
            IR = MBR[0] +" "+ MBR[1][:carac]
            MAR = MBR[1][carac:].strip("(").strip(")")
        elif MBR[1] == "MQ":
            IR = MBR[0] + " " +MBR[1]
    exibeRegistradores("Pós DecodificaOP")
    executaOp()

def executaOp():
    global IR, MAR, MBR, AC, MQ, PC
    IR = IR.split(" ")
    if IR[0] == "LOAD": #IF para os respectivos LOADS permitidos
        if IR[1] == "MQ": #Se apenas MQ no parametro o AC recebe MQ
            AC = MQ
        elif IR[1] == "M": #Se apenas M no parametro AC recebe M
            MBR = procuraEnd(MAR)[0] #MBR recebe o endereço especificado pelo MAR (repete em basicamente todos)
            AC = int(MBR[0]) #AC recebe MBR (repete em basicamente todos)
            
        elif IR[1] == "-M": 
            MBR = procuraEnd(MAR)[0]
            AC = -int(MBR[0])
            
        elif IR[1] == "|M":
            MBR = procuraEnd(MAR)[0]
            AC = abs(int(MBR[0]))
            
        elif IR[1] == "-|M":
            MBR = procuraEnd(MAR)[0]
            AC = -abs(int(MBR[0]))
            
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
        
        with open("RAM","r+") as ram: #Abertura do arquivo
            offset = procuraEnd(MAR)[1] #Offset de onde está o endereço especificado pelo MAR
            ram.seek(offset) #Foi até o endereço especificado
            aux = ram.readline() #aux armazenando o a linha completa do endereço especificado
            aux = aux.split(" ") #split para facilidade de manipulação dividindo a palavra por espaços
            MBR = AC #MBR recebendo AC para a escrita em memória
            aux[1] = MBR #Parte do dado recebe o MBR
            aux = aux[0]+" "+str(aux[1]) #Concatenação completa de aux
            ram.seek(offset) #ida ao endereço
            ram.write(aux) #escrita de novo dado
        
    elif IR[0] == "ADD": #ADIÇÃO DO AC PELO DADO PASSADO POR M(X)
        with open("RAM","r+") as ram:
            MBR = procuraEnd(MAR)[0] #obtenção
            AC = int(AC) + int(MBR[0])
            
    elif IR[0] == "SUB": #Subtração do AC pelo dado passado por M(X)
        with open("RAM","r+") as ram:
            MBR = procuraEnd(MAR)[0] #obtenção
            AC = int(AC) - int(MBR[0])
            
    elif IR[0] == "MUL": #multiplicação do MQ pelo dado passado por M(X)
        with open("RAM","r+") as ram:
            MBR = procuraEnd(MAR)[0] #obtenção do dado e salvamento no MBR
            MQ = int(MQ) * int(MBR[0])
            
    elif IR[0] == "DIV": #Divisão do dado passado pela memória M(X)
         with open("RAM","r+") as ram:
            MBR = procuraEnd(MAR)[0] #obtenção do dado e salvamento no MBR
            AC = int(MQ) // int(MBR[0]) #guardando o quociente em AC
            MQ = int(MQ) % int(MBR[0]) #guardando o resto em MQ
            
    elif IR[0] == "+JUMP":#Nas funções de JUMP apenas o PC é atribuido ao MAR (endereço passado pelo M(x))
        if int(AC) >= 0:
            PC = MAR
    elif IR[0] == "-JUMP":
        if int(AC) <= 0:
            PC = MAR
    elif IR[0] == "JUMP":
            PC = MAR 
    exibeRegistradores("Fim da Execução")
    
def exibeRegistradores(onde): #Função de exibição 
    global IR, MAR, MBR, AC, MQ, PC
    print(onde)
    print(f"PC: {PC}                   MBR: {MBR}")
    print(f"MAR: {MAR}                 IR: {IR}")
    print(f"AC: {AC}                   MQ: {MQ}")
    input()



if __name__ == "__main__":
    leMem()