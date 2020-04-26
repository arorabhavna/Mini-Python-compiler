from sys import stdin
import re
NUM_REGISTERS = 16


is_int=lambda x: bool(re.match("[0-9]+", x))

is_float=lambda x: bool(re.match("[0-9]+\.[0-9]+", x))

is_variable= lambda x: bool(re.match("[a-zA-Z_][a-zA-Z0-9_]*", x))

is_str= lambda x: bool(re.match("(\".*\")|(\'.*\')", x))

is_bool = lambda x: x=="True" or x=="False"

is_const = lambda x: is_int(x) or is_bool(x) or is_float(x) or is_str(x)

operators={'+','-','*','/','//','%','in','and','or','|','&','**','^','not','>>','<<',"==","!=",">","<",">=","<="}

class Variable:
    def __init__(self,n,ne):
        
        self.name=n
        self.next_use=ne 

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            return self.name == other

    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name

class Operation:

    def __init__(self,ins):
        self.ins=ins
        if ins=='Label':
            self.asm="L" #label
        elif ins=='goto':
            self.asm="B" #unconditional branch
        elif ins=='IfFalse' or ins[0]=="If" or ins[0]=='IfTrue':
            self.asm="BEQ" #conditional branch
        elif ins=='call':
            self.asm="BL" #branch and link (function call)
        elif ins=='param':
            self.asm='PUSH' #push register content to stack pointed by stack pointer SP (R13 in ARM)
        elif ins=='=':
            self.asm='MOV' #move the constant into register represented by the variable
        elif ins=='+':
            self.asm='ADD' # continue for the rest



class RegisterBank:

    register_map=[None for i in range(NUM_REGISTERS-3)] #register to variable
    var_map={} #variable to register mapping
    allocated=set() #set of allocated registers
    unallocated=set([i for i in range(NUM_REGISTERS-3)]) #set of unallocated registers
    
    @staticmethod
    def deallocate(var):
        reg=RegisterBank.var_map[var]
        RegisterBank.allocated.remove(reg)
        RegisterBank.unallocated.add(reg)
        del RegisterBank.var_map[var]
        RegisterBank.register_map[reg]=None
        code="\t\tSTR R"+str(reg)+",="+var.name+"\n"
        return reg,code

    @staticmethod
    def algorithm(var):
        if var in RegisterBank.var_map:
            return var_map[var],''
        if len(RegisterBank.unallocated)>0:
            for i in RegisterBank.unallocated:
                code="\t\tLDR R"+str(i)+",="+var.name+"\n"
                return i,code
        else:
            max_next_use_var=Variable('',-1)
            for i in RegisterBank.var_map:
                if i.next_use>max_next_use_var.next_use:
                    max_next_use_var=Variable(i.name,i.next_use)
            reg,code=RegisterBank.deallocate(max_next_use_var)
            code+="\t\tLDR R"+str(reg)+",="+max_next_use_var.name+"\n"
            return RegisterBank.var_map[max_next_use_var],code
    
    @staticmethod
    def allocate(var):
        reg,code=RegisterBank.algorithm(var)
        RegisterBank.allocated.add(reg)
        RegisterBank.unallocated.remove(reg)
        RegisterBank.register_map[reg]=var
        RegisterBank.var_map[var]=reg
        return reg,code
            
class Instruction:
    def __init__(self,ins):
        self.op=Operation(ins[0])
        self.src1=ins[1]
        self.src2=ins[2]
        self.dst=ins[3]
    
    def convert(self):
        if self.op.ins=='+':
            src1,code1=RegisterBank.allocate(self.src1)
            src2,code2=RegisterBank.allocate(self.src2)
            dst,code3=RegisterBank.allocate(self.dst)
            code=code1+code2+code3
            code+="\t\t"+self.op.asm+" R"+str(src1)+",R"+str(src2)+",R"+str(dst)+"\n"
            return code
        
        if self.op.ins=='=':
            dst,code=RegisterBank.allocate(self.dst)
            if type(self.src1)==Variable: #variable is being equated
                src1,code1=RegisterBank.allocate(self.src1)
                code+=code
                src1="R"+str(src1)
            else: #constant is being equated
                src1="#"+self.src1
            code+="\t\tMOV R"+str(dst)+","+src1
            return code
        
lines=[]        

for line in stdin:
    temp=line.strip().split("\t")
    if temp!=['']:
        lines.append(temp)

def next_use_algorithm(program):
    symTable={}
    for i in range(len(program)):

        if program[i][0] in ('call','Label','goto'):
            continue 

        elif program[i][0]=='IfFalse':
            if is_variable(program[i][1]):
                program[i][1]=Variable(program[i][1],None) 
                symTable[program[i][1]]=Variable(program[i][1].name,None)

        elif program[i][0]=='=':
            if is_variable(program[i][1]):
                program[i][1]=Variable(program[i][1],None) 
                symTable[program[i][1]]=Variable(program[i][1].name,None)
            
            if is_variable(program[i][3]):
                program[i][3]=Variable(program[i][3],None)
                symTable[program[i][3]]=Variable(program[i][3].name,None)
            
        
        else:
            if is_variable(program[i][1]):
                program[i][1]=Variable(program[i][1],None)
                symTable[program[i][1]]=Variable(program[i][1].name,None)

            if is_variable(program[i][2]):
                program[i][2]=Variable(program[i][2],None)
                symTable[program[i][2]]=Variable(program[i][2].name,None)

            if is_variable(program[i][3]):
                program[i][3]=Variable(program[i][3],None)
                symTable[program[i][3]]=Variable(program[i][3].name,None)
    
    for i in range(len(program)-1,-1,-1):
        if program[i][0] in ('call','Label','goto'):
            continue 

        elif program[i][0] == 'IfFalse':
            if type(program[i][1])==Variable:
                if program[i][1] in symTable:
                    x=symTable[program[i][1]]
                    program[i][1]=Variable(x.name,x.next_use)
                    x.next_use=i

        elif program[i][0] == '=':
            if type(program[i][1])==Variable:
                if program[i][1] in symTable:
                    x=symTable[program[i][1]]
                    program[i][1]=Variable(x.name,x.next_use)
                    x.next_use=i

            if type(program[i][3])==Variable:
                if program[i][3] in symTable:
                    x=symTable[program[i][3]]
                    program[i][3]=Variable(x.name,x.next_use)
                    x.next_use=i
        
        else:
            if type(program[i][1])==Variable:
                if program[i][1] in symTable:
                    x=symTable[program[i][1]]
                    program[i][1]=Variable(x.name,x.next_use)
                    x.next_use=i

            if type(program[i][2])==Variable:
                if program[i][2] in symTable:
                    x=symTable[program[i][2]]
                    program[i][2]=Variable(x.name,x.next_use)
                    x.next_use=i

            if type(program[i][3])==Variable:
                if program[i][3] in symTable:
                    x=symTable[program[i][3]]
                    program[i][3]=Variable(x.name,x.next_use)
                    x.next_use=i
    
    for i in range(len(program)):
        program[i]=Instruction(program[i])

    return symTable

def translate(program):
    symTable=next_use_algorithm(program)
    asm_code="""\t\tAREA     ARMex, CODE, READONLY\n\t\tENTRY                   ; Mark first instruction to execute\n\n\t\t.text\n\nstart:\n"""
    
    for i in program:
        try:
            asm_code+=i.convert()
        except:
            continue
    
    asm_code+="""\nstop:\n\t\tMOV      r0, #0x18      ; angel_SWIreason_ReportException\n\t\tLDR      r1, =0x20026   ; ADP_Stopped_ApplicationExit\n\t\tSVC      #0x123456      ; ARM semihosting (formerly SWI)\n"""
    asm_code+="\n\t\t.data\n"

    for i in symTable:
        asm_code+=str(i)+": 0"

    return asm_code

asm_code=translate(lines)
print(asm_code)



            

         





