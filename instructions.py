"""
This file hold the fuctions that emulate the possible instructions for STANDARD_01_64_mem.
It needs the following files:
     -memory_class.py
     -registers.py

"""



#Imports here:
from memory_class import memory
from registers_class import registers



###Instructions here###

def ADD(registers,memory):
    """This instruction takes 2 targeted registers and outpusts their sum into a third register."""
    pass



###Internal functions here###




def parse_input(registers,memory):
    """This function is used to identify the target registers given the program state."""
    general_register=[]
    for register in ["r1","r2","r3","r4","r5","r6","r7","r8","r9"]:
        general_registers[register]=registers.reg_read("0",register)
    program_counter=registers.reg_read("0","pc")
    intr=registers.reg_read("0","intr")
    intr_on=registers.reg_read("0","intr_on")
    intr_jump=registers.reg_read("0","intr_jmp")
    intr_mask_low=registers.reg_read("0","intr_mask_low")
    intr_mask_high=registers.reg_read("0","intr_mask_high")
    exec_allow_low=registers.reg_read("0","exec_low")
    exec_allow_high=registers.reg_read("0","exec_high")
    cycles=registers.reg_read("0","cycles")
    cpuid=registers.reg_read("0","cpuid")
    TRUE=registers.reg_read("0","TRUE")
    FALSE=registers.reg_read("0","FALSE")
    if intr_on==TRUE:   #handle possible intr
        intr_mask_low_int=int(intr_mask_low,2)
        intr_mask_high_int=int(intr_mask_high,2)
        intr_masked=False
        for mem_address in range[intr_mask_low_int,intr_mask_high_int+1]:   #search to see if this intr should be masked
            if intr==memory.mem_read(mem_address):
                intr_masked=True
                break
        if intr_masked==True:
            #handle standard
            #remove intr and turn off intr_on
            pass
        else:
            #jump to intr_handling
            return()
    else:   #intr is not on, procede as normal
        raw_instruction=memory.mem_read(int(program_counter,2)  #fetch the data
        instr_frame=raw_instruction[0:16]   #split into components
        reg_target_1=raw_instruction[16:32]
        reg_target_2=raw_instruction[32:48]
        rea_target_3=raw_instruction[48:64]
        target_reg=[]   #handle register targets first
        for target_reg in [reg_target_1,reg_target_2,reg_target_3]:
            control=target_reg[0:4]
            if control=="1111":
                control="vector"
            elif control=="0000":
                control="direct"
            else:
                pass    #handle err
            register=int(target_reg[4:16],2)
            register_types=[]
            valid_register=False
            try:
                register_type=register_type[register]
            except:
                #handle error
                pass
            target_reg.append([control,register])
        