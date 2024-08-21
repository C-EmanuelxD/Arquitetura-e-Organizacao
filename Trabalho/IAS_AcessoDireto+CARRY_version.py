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



def procuraEnd(endereco):
    endereco = str(endereco)
    endereco = int(endereco, 16)
    offset = 0
    with open("RAM", "r") as arq:
        ram = arq.readlines() #LE TODAS AS LINHAS DA RAM, PARA REALIZAÇÃO DO ACESSO DIRETO
        for i in range(endereco): #FAZ CALCULO DO OFFSSET (PARTE FORA DA "SIMULAÇÃO", PARA SABER ONDE ESCREVER NO ARQUIVO)
            offset += len(ram[i])+1
        palavra = ram[endereco].strip("\n")
        return palavra.split(" ")[1:], offset, palavra #RETORNO DAS INFORMAÇÕES: PALAVRA SEM O ENDEREÇO, OFFSET, PALAVRA COM O ENDEREÇO
    
#Procurando a palavra de memória que contenha apenas um endereço
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
        print(f"mbr puro: {MBR}")
        print(f'mbr indice 1: {MBR[1]}')
        if MBR[1][carac] == '(':
            IR = MBR[0] +" "+ MBR[1][:carac]
            MAR = MBR[1][carac:].strip("(").strip(")").strip("|").strip(")")
        elif MBR[1] == "MQ":
            IR = MBR[0] + " " +MBR[1]

        elif MBR[1][:3] == "MQ,":
            parte = MBR[1].split(",")
            if ehInteiro(parte[1]):
                IR = MBR[0] + " " + parte[0] + "," + parte[1]
                MAR = parte[1]

        elif ehInteiro(MBR[1]):
            IR = MBR[0] + " " + MBR[1]
    exibeRegistradores("Pós DecodificaOP")
    executaOp()

def executaOp():
    global IR, MAR, MBR, AC, MQ, PC
    print(f"primeiro ir {IR}")
    IR = IR.split(" ")
    print(f"segundo ir {IR}")
    if IR[0] == "LOAD": #IF para os respectivos LOADS permitidos
        if IR[1] == "MQ": #Se apenas MQ no parametro o AC recebe MQ
            AC = MQ
        elif IR[1] == "M": #Se apenas M no parametro AC recebe M
            MBR = procuraEnd(MAR)[0] #MBR recebe o endereço especificado pelo MAR (repete em basicamente todos)
            MBR = MBR[0]
            AC = int(MBR) #AC recebe MBR (repete em basicamente todos)
            
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
            MQ = int(MAR)

        elif IR[1].split(",")[1][:1] == "-" and not IR[1].split(",")[1][:2] == "-|" and not IR[1][3] == "M":
            MQ = int(MAR)

        elif IR[1].split(",")[1][:1] == "|" and not IR[1][2] == "M":
            c = MAR.strip("|")
            MQ = abs(int(c))

        elif IR[1].split(",")[1][:2] == "-|" and not IR[1][3] == "M":
            c = MAR.strip("-").strip("|").strip("|")
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
        
        with open("RAM","r+") as ram: #Abertura do arquivo
            nulo, offset, aux = procuraEnd(MAR) #Offset de onde está o endereço especificado pelo MAR
            ram.seek(offset) #Foi até o endereço especificado
            aux = aux.split(' ')
            MBR = str(AC) #MBR recebendo AC para a escrita em memória
            aux[1] = MBR
            ram.seek(offset)
            memsobra = TAM_MEM-len(aux[1])
            if memsobra < 0:
                print("O VALOR EXCEDEU O TAMANHO DISPONÍVEL. FECHANDO!")
                exit(OverflowError)
            else:
                aux = aux[0] + " " +(str(0)*(memsobra))+aux[1]
                ram.write(aux)
        
    elif IR[0] == "ADD": #ADIÇÃO DO AC PELO DADO PASSADO POR M(X)
        with open("RAM","r+") as ram:
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
        with open("RAM","r+") as ram:
            if ehInteiro(IR[1]):
                MBR = IR[1]
                AC = int(AC) - int(MBR)
                if AC < -999:
                    C = 1
                    AC = AC + 10000
                else:
                    C = 0
            else:
                MBR = procuraEnd(MAR)[0] #obtenção
                AC = int(AC) - int(MBR[0])
                if AC < -999:
                    C = 1
                    AC = AC + 10000
                else:
                    C = 0
            
    elif IR[0] == "MUL": #multiplicação do MQ pelo dado passado por M(X)
        with open("RAM","r+") as ram:
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
         with open("RAM","r+") as ram:
            if ehInteiro(IR[1]):
                MBR = IR[1]
                AC = int(int(MQ) // int(MBR)) #guardando o quociente em AC
                MQ = int(MQ) % int(MBR) #guardando o resto em MQ
            else:
                MBR = procuraEnd(MAR)[0] #obtenção do dado e salvamento no MBR
                AC = int(int(MQ) // int(MBR[0])) #guardando o quociente em AC
                MQ = int(MQ) % int(MBR[0]) #guardando o resto em MQ

    elif IR[0] == "MOV":
        if IR[1] == "AC" and IR[2] == "MQ":
            AC = MQ

        elif IR[1] == "MQ" and IR[2] == "AC":
            MQ = AC

        elif IR[1] == "AC" and ehEndereco(IR[2]):
            MBR = procuraEnd(IR[2])[0]
            AC = int(MBR[0])

        elif IR[1] == "M" and ehEndereco(IR[2]):
            with open("RAM", "r+") as ram:
                offset = procuraEnd(IR[2])[1]
                ram.seek(offset)
                aux = procuraEnd(IR[2])[2]
                MBR = str(AC)
                aux[1] = MBR
                ram.seek(offset)
                memsobra = TAM_MEM - len(aux[1])
                if memsobra < 0:
                    print("o valor excedeu o tamanho disponivel")
                    exit(OverflowError)
                else:
                    aux = aux[0] + " " + (str(0) * (memsobra)) + aux[1]
                    ram.write(aux)

        elif IR[1] == "M" and ehEndereco(IR[2]):
            with open("RAM", "r+") as ram:
                offset = procuraEnd(IR[2])[1]
                ram.seek(offset)
                aux = procuraEnd(IR[2])[2]
                MBR = str(MQ)
                aux[1] = MBR
                ram.seek(offset)
                memsobra = TAM_MEM - len(aux[1])
                if memsobra < 0:
                    print("o valor excedeu o tamanho disponivel")
                    exit(OverflowError)
                else:
                    aux = aux[0] + " " + (str(0) * (memsobra)) + aux[1]
                    ram.write(aux)
                    ram

        elif ehEndereco(IR[1]) and ehEndereco(IR[2]):
            MBR = procuraEnd(IR[1])[0]
            valor = int(MBR[0])

            with open("RAM", "r+") as ram:
                offset = procuraEnd(IR[2])[1]
                ram.seek(offset)
                aux = procuraEnd(IR[2])[2]
                MBR = str(valor)
                aux[1] = MBR
                ram.seek(offset)
                memsobra = TAM_MEM - len(aux[1])
                if memsobra < 0:
                    print("o valor excedeu o tamanho disponivel")
                    exit(OverflowError)
                else:
                    aux = aux[0] + " " + (str(0) * (memsobra)) + aux[1]
                    ram.write(aux)

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
    print(f"Carry: {C}")
    #input()



if __name__ == "__main__":
    leMem()