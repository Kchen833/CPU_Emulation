"""This file handles register emulation for the cpu"""



class registers():
    """This class handles memory emulation.
    The default (eg starting) settings a 64bit width with no valid registers or core.
    Width refers to the size of each memory address in bits"""
    def __init__(self):
        """Generates the default memory class object.\n
        NOTE:The general format of the registers class attribiutes is as follows:
             -registers.registers={"core name":{"reg_1_core_1":data},"core 2":{"reg_1_core_2":data,"reg_2_core_2":data}}
             -registers.register_list={"core name":["reg_1_core_1"],"core 2":["reg_1_core_2","reg_2_core_2"]}
             -registers.register_width=64\n
        WARNING:The object does not start out with any valid cores or register names."""
        self.registers={"0":{}}
        self.register_list={"0":[]}
        self.register_width=64
    def reg_read(self,core,register_name):
        """This methold retrives a core's register."""
        if isinstance(core,type(str()))!=True and isinstance(register_name,type(str())):
            raise TypeError("Both core and register name must be stings.")
        else:
            valid_reg_name=False
            try:
                valid_reg_list=self.register_list[core]
            except:
                raise ValueError("There is no core "+core+" .")
            for possible_reg_name in valid_reg_list:
                if possible_reg_name==register_name:
                    valid_reg_name=True
                    break
            if valid_reg_name!=True:
                raise ValueError("This core does not have the requested register.")
            else:
                try:
                    reg_list=self.registers[core]
                    reg=reg_list[register_name] #The register exists and already has a value.
                    return(reg)
                except: #The register is valid, however there is no vaule;therefore, it must be zero.
                    reg=format(0,"0"+str(self.register_width)+"b")
                    return(reg)
    def reg_write(self,core,register_name,data):
        """This function takes the core,targeted register and data
        and writes the data to the targeted register."""
        if isinstance(core,type(str()))!=True or isinstance(register_name,type(str()))!=True or isinstance(data,type(str()))!=True:
            raise TypeError("must be strings")
        elif len(data)!=self.register_width:
            raise ValueError("The data is not of an appropiate size.")
        else:
            for char in data:
                if char!="0" and char!="1":
                    raise ValueError("Data must be a binary string.")
            try:    #Check that the core exists
                valid_reg_list=self.register_list[core]
            except:
                raise ValueError("There is no core "+core+" .")
            for possible_reg_name in valid_reg_list:    #Check that the register_name given is valid
                valid_reg_name=False
                if possible_reg_name==register_name:
                    valid_reg_name=True
                    break
            if valid_reg_name!=True:
                raise ValueError("This core does not have the requested register.")
            if int(data,2)==0:
                try:    #Delete the register(default is zero).
                    register_list=self.registers[core]
                    del register_list[register_name]
                    self.registers[core]=register_list
                except:
                    pass    #Entry does not exist, no need for deletion
            else:
                register_list=self.registers[core]
                register_list[register_name]=data
                self.registers=register_list
    def reg_setting(self,register_list,width):
        """This methold sets both the register list and width of this class.\n
        WARNING:If the new setting would truncate the simulated registers,
        (eg a redution in size and/or width), the registers will be truncated accordingly."""
        if isinstance(register_list,type(dict()))!=True or isinstance(width,type(int()))!=True:
            raise TypeError("The register list must be a dictionary and the width must be an integer")
        elif width<1:
            raise ValueError("The width can not be lower than 1")
        for valid_reg_name_list_key in register_list:   #Check that the given register list is valid
            valid_reg_name_list=register_list[valid_reg_name_list_key]
            if isinstance(valid_reg_name_list,type(list()))!=True:
                raise ValueError("The register list must be a dictionary of key/data pairs like {'core0':['r1','r2']}.")
            for valid_reg_name in valid_reg_name_list:
                if isinstance(valid_reg_name,type(str()))!=True:
                    raise ValueError("The register list must be a dictionary of key/data pairs like {'core0':['r1','r2']}.")
        new_core_regs={}    #Now we remove invalid entries in self.registers
        for core_reg_list_key in self.registers:
            valid_core=False
            for valid_core_key in register_list:
                if valid_cores_key==valid_core_key:
                    valid_core=True
            if valid_core==True:    #The core is kept
                pass
            else:   #Else do not preserve the invalid core
                core_reg_list={}
                valid_reg_list=register_list[core_reg_list_key]
                valid_reg=False
                for core_reg_key in self.registers[core_reg_list_key]:  #Now we check the core registers
                    valid_reg=False
                    for valid_register in valid_reg_list:
                        if core_reg_key==valid_register:
                            valid_reg=True
                    if valid_reg==True: #It is a valid core reg, transfer.
                        core_reg_list[core_reg_key]=self.registers[core_reg_list_key][core_reg_key]
                    else:
                        pass    #Else, drop.
                new_core_regs[core_reg_list_key]=core_reg_list
        for valid_core_name in register_list:   #dont forget to add new cores
            present=False
            for core_name in new_core_regs:
                if core_name==valid_core_name:
                    present=True
            if present==False:
                new_core_regs[valid_core_name]={}
        self.registers=new_core_regs    #write out new data
        self.register_list=register_list
        self.register_width=width
    def reg_set_core_reg_list(self,core,reg_list):
        """This methold allows one to only alter a target core's register list(eg the allowed register names)."""
        if isinstance(reg_list,type(dict()))!=True:
            pass
        else:
            register_list=self.register_list
            register_list[core]=reg_list
            width=self.register_width
            self.reg_setting(register_list,width)
    def reg_set_reg_width(self,width):
        """This methold allows one to only alter the width of all registers. """
        if isinstance(width,type(int()))!=True:
            pass
        else:
            register_list=self.register_list
            self.reg_setting(register_list,width)
    def read_core_regs(self,core):
        """This methold returns all registers associated with the target core.\n
        WARNING:Scince the registers are removed from memory when their values are zero,
         you will also need to handle the lack of said registers."""
        if isinstance(core,type(str()))!=True:
            raise TypeError("")
        else:
            valid_core_name=False
            for core_name in self.registers:
                if core_name==core:
                    valid_core_name=True
            if valid_core_name==False:
                raise ValueError("")
            else:
                return(self.registers[core])
    def read_core_reg_list(self,core):
        """This methold returns all valid register names for the target core."""
        if isinstance(core,type(str()))!=True:
            raise TypeError("")
        else:
            valid_core_name=False
            for core_name in self.registers:
                if core_name==core:
                    valid_core_name=True
            if valid_core_name==False:
                raise ValueError("")
            else:
                return(self.register_list[core])



if __name__ == "__main__":
    help(registers)