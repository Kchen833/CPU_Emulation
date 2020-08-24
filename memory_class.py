"""This file handles memory emulation for the cpu.\n
NOTE:All returned vaules are binary strings."""



class memory():
    """This class handles memory emulation.
    The default(eg starting) settings are 64bit size and width with a null mem.
    Size refers to address space in bits.
    Width refers to the size of each memory address in bits"""
    def __init__(self):
        """Generates the default memory class object."""
        self.memory={}
        self.setting={"size":64,"width":64} 
    def mem_read(self,address):
        """This methold retrives a target address's data."""
        try:
            a=int(address,2)
            if len(address)!=self.setting["size"]:
                raise ValueError("Input not a "+str(self.setting["size"])+" length binary string.")
            address=a
        except:
            raise ValueError("Input not a binary string.")
        try:
            data=self.memory[address]
            return(data)
        except:
            data=0
            return(data)
    def mem_write(self,address,data):
        """This function takes two padded binary strings(address,data)
        and writes the data to the targeted address."""
        try:
            a=int(address,2)
            if len(address)!=self.setting["size"]:
                raise ValueError("Given address is not a "+str(self.setting["size"])+" length binary string.")
            address=a
        except:
            raise ValueError("Given address is not a binary string.")
        try:
            a=int(data,2)
            if len(address)!=self.setting["size"]:
                raise ValueError("Given data is not a "+str(self.setting["width"])+" length binary string.")
        except:
            raise ValueError("Given data is not a binary string.")
        if int(data,2)!=0:
            self.memory[address]=data
        else:
            try:            #There is a key vaule that corresponds to the address, delete.
                a=self.memory[address]
                del self.memory[address]
            except:         # There is no key vaule ,leave as is
                pass
    def mem_setting(self,size,width):
        """This methold sets both the size and width settings of this class.\n
        WARNING:If the new setting would truncate the simulated memory,
        (eg a redution in size and/or width), the memory regions will be truncated accordingly."""
        if isinstance(size,type(int()))!=True or isinstance(width,type(int()))!=True:
            raise TypeError("Both size and width must be integers.")
        elif size<1 or width<1:
            raise ValueError("Both size and width can not be less than 1.")
        setting={"size":size,"width":width}
        original_setting=self.setting
        lower_size=False
        lower_width=False
        higher_width=False
        if original_setting["size"]>size:
            lower_size=True
        if original_setting["width"]>width:
            lower_width=True
        elif original_setting["width"]<width:
            higher_width=True
        new_memory={}
        max_key_vaule=(2**(original_setting["size"]))-1
        for key in self.memory:
            if lower_size==True:            #The rea=son why we only check to truncate the address is because the addresses are intergers
                if int(key)>max_key_vaule:  #and do not require padding if the max_vaule would be higher unlike the data
                    del self.memory[key]
                else:
                    if lower_width==True:
                        original_data=self.memory[key]
                        diff=original_setting["width"]-width
                        data=original_data[diff:len(original_data)]
                        self.memory[key]=data
                    elif higher_width==True:
                        original_data=self.memory[key]
                        diff=original_setting["width"]-width
                        data=format(0,str(diff)+"b")+original_data
                        self.memory[key]=data
    def mem_size_set(self,size,width):
        """This methold only sets the size setting."""
        width=self.setting["width"]
        mem_setting(self,size,width)
    def mem_width_set(self,width):
        """This methold only sets the width setting."""
        size=self.setting["size"]
        mem_setting(self,size,width)



if __name__ == "__main__":
    help(memory)