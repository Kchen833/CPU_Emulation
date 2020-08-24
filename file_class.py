"""This file handles importation of file data into a more convient class to acesss
and save data"""



class file_object():
    """This class handles creation,loading and storage of data from/to files.\n
    WARNING:You cannot read any data from this class without initialization.
    """
    def __init__(self):
        """This methold initializes the class\n
        WARNING:This is only used to intialize a file_object.
        In order to use any methold thatperforms reads from this class, it must have information loaded via:
             -import_into_file_obj
             -set_file_object
        The following metholds also enable reading but may have undefined effects if not used carefully:
             -set_file_obj_settings
             -set_file_obj_cpu
             -set_file_obj_memory
        However if you use all three to configure all of the fields before reading there will be no undefined effects.
        The only exception to these rules is check_file_obj_set which is used to check the above condition.
        The list of functions that are locked is as follows:
             -file_object_read_settings
             -file_object_read_cpu
             -file_object_read_memory
             -save_file_object"""
        self.settings={"CPU":0,"MEM":0,"TYPE":0}
        self.cpu={"0":{}}
        self.memory={"0":{}}
        self.set=False
    def import_into_file_obj(self,filename):
        """This methold takes a file name and iports the data into this file.\n
        WARNING: this methold does not attempt to verify that any of the data vaulse is correct
        due to the nature of the file format.
        You must validate all components before using this object."""
        if isinstance(filename,type(str()))!=True:
            raise TypeError("Given file name input is not a string.")
        try:
            file=open(filename+".sav","r")
            file.close()
        except:
            raise FileNotFoundError("There is no file with the name "+filename+".sav .")
        with open(filename+".sav") as file:
            file_lines=file.readlines()
            if len(file_lines)<7:   #there should be at least 7 lines in the file
                raise InvalidFileError("This file has less than seven lines and is not valid")
            mode="start"        #start of state machine
            file_type=""
            cpu_type=""
            cpu_regs={}
            temp_reg_frame_list={}
            mem_type=""
            mem_data={}
            temp_mem_data_list={}
            for line in file_lines:
                line=str.rstrip(line)
                if mode=="start":
                    frame=line[0:5]
                    if frame!="TYPE:":
                        raise InvalidFileError("The file does not have a type field.")
                    else:
                        file_type=line[4:len(line)]
                        mode="cpu_type"
                elif mode=="cpu_type":
                    frame=line[0:4]
                    if frame!="CPU:":
                        raise InvalidFileError("The file does not have a cpu type field.")
                    else:
                        frame=line[3:len(line)]
                        cpu_type=line[3:len(line)]
                        mode="mem_type"
                elif mode=="mem_type":
                    frame=line[0:4]
                    if frame!="MEM:":
                        raise InvalidFileError("The file does not have a memory field.")
                    else:
                        frame=line[3:len(line)]
                        mem_type=line[3:len(line)]
                        mode="cpu_reg_start"
                elif mode=="cpu_reg_start":
                    if line!="-CPU-":
                        raise InvalidFileError("The file does not have a cpu reg start header.")
                    else:
                        mode="first_cpu_reg_frame"
                elif mode=="first_cpu_reg_frame":    #handle first frame
                    temp_reg_frame_list={}
                    frame=line[0:1]
                    if frame!="/":
                        raise InvalidFileError("This file does not have a cpu register frame header")
                    else:
                        temp_reg_frame_list["START"]=line[1:len(line)]    #save reg frame header
                        mode="cpu_reg_frame"
                elif mode=="cpu_reg_frame":
                    frame=line[0:6]
                    if frame=="START:": #check that the frame is not START (START is reserved)
                        raise InvalidFileError("The register frame may not have a register labeled 'START'.")
                    else:
                        frame=line[0:len(line)]
                        if frame=="-MEM-":   #jump to mem data frame mode
                            #dont forget to purge
                            reg_frame_label=temp_reg_frame_list["START"]
                            del temp_reg_frame_list["START"]
                            cpu_regs[reg_frame_label]=temp_reg_frame_list
                            mode="first_mem_data_frame"
                        else:
                            frame=line[0:1]
                            if frame=="/":   #handle a new cpu register frame
                                reg_frame_label=temp_reg_frame_list["START"]
                                del temp_reg_frame_list["START"]
                                cpu_regs[reg_frame_label]=temp_reg_frame_list   #dump data
                                temp_reg_frame_list["START"]=line[1:len(line)]  #save new reg frame header
                            else:
                                pointer=0
                                prev_pointer=0
                                at_data=False
                                for char in line:   #find first colon(delimiter)
                                    pointer=pointer+1
                                    if char==":":
                                        break
                                    else:
                                        prev_pointer=pointer
                                if prev_pointer==len(line):  #check to make sure that there is a name-data pair delimited by a colon
                                    raise InvalidFileError("The file contains an incomplete or invalid name/data pair.")
                                else:
                                    reg_name=line[0:prev_pointer]
                                    reg_data=line[pointer:len(line)]
                                    temp_reg_frame_list[reg_name]=reg_data
                elif mode=="first_mem_data_frame":
                    temp_mem_data_list={}
                    frame=line[0:1]
                    if frame!="/":
                        raise InvalidFileError("This file does not have a memory frame header.")
                    else:
                        temp_mem_data_list["START"]=line[1:len(line)]
                        mode="mem_data_frame"
                elif mode=="mem_data_frame":
                    frame=line[0:6]
                    if frame=="START:": #check that the frame is not START (START is reserved)
                        raise InvalidFileError("The register frame may not have a register labeled 'START'.")
                    else:
                        frame=line[0:len(line)]
                        frame=line[0:1]
                        if frame=="/":   #handle a new cpu register frame
                            mem_frame_label=temp_mem_data_list["START"]
                            del temp_mem_data_list["START"]
                            mem_data[mem_frame_label]=temp_mem_data_list   #dump data
                            temp_mem_data_list["START"]=line[1:len(line)]  #save new reg frame header
                        else:
                            pointer=0
                            prev_pointer=0
                            at_data=False
                            for char in line:   #find first colon(delimiter)
                                pointer=pointer+1
                                if char==":":
                                    break
                                else:
                                    prev_pointer=pointer
                            if prev_pointer==len(line):  #check to make sure that there is a name-data pair delimited by a colon
                                raise InvalidFileError("The file contains an incomplete or invalid name/data pair.")
                            else:
                                mem_name=line[0:prev_pointer]
                                mem_data_in_pair=line[pointer:len(line)]
                                temp_mem_data_list[mem_name]=mem_data_in_pair
                            if line==file_lines[len(file_lines)-1]:   #check to see if we are at the end of the file (last line)
                                mem_frame_label=temp_mem_data_list["START"]    #if so dump mem data
                                del temp_mem_data_list["START"]
                                mem_data[mem_frame_label]=temp_mem_data_list
            if mode!="mem_data_frame":
                raise InvalidFileError("This file is missing required sections/fields")
            else:
                self.settings={"TYPE":file_type,"CPU":cpu_type,"MEM":mem_type}
                self.cpu=cpu_regs
                self.memory=mem_data
                self.set=True
    def file_obj_read_settings(self):
        """This methold is used to obtain file_object settings.\n
        WARNING:This methold may not be used if the file_object is not set. """
        if self.set!=True:
            raise FileObjNotSet("This object has not been set yet.")
        else:
            return(self.settings)
    def file_obj_read_cpu(self):
        """This methold is used to obtain file_object registers.
        It does not provide for selection of cores.\n
        WARNING:This methold may not be used if the file_object is not set. """
        if self.set!=True:
            raise FileObjNotSet("This object has not been set yet")
        else:
            return(self.cpu)
    def file_obj_read_memory():
        """This methold is used to obtain file_object registers.
        It does not provide for selection of memory pages.\n
        WARNING:This methold may not be used if the file_object is not set. """
        if self.set!=True:
            raise FileObjNotSet("This object has not been set yet")
        else:
            return(self.memory)
    def check_file_obj_set(self):
        """This methold is used to check if the provided file_obj has been set\n
        NOTE:This is the ony read methold that works wether or not the file_object is set."""
        return(self.set)
    def set_file_object(self,settings,cpu,mem):
        """This methold takes a series of dictionaries and sets the given file object."""
        if isinstance(settings,dict())!=True or isinstance(cpu,dict())!=True or isinstance(memory,dict())!=True:
            raise TypeError("This methold only accepts dictionaries.")
        else:
            i=0
            for key in settings:
                if key!="CPU" and key!="MEM" and key!="TYPE":
                    raise VauleError("Provided settings should only have CPU,MEM,TYPE as keys.")
                else:
                    i=i+1
            if i!=3:
                raise ValueError("The settings do not conform with expected format.")
            else:
                self.settings=settings
                self.cpu=cpu
                self.memory=memory
                self.set=True
    def set_file_obj_settings(self,settings):
        """This methold sets the settings field.\n
        WARNING:This methold will enable reading of the file_object but may cause undefined effects."""
        if isinstance(settings,dict())!=True:
            raise TypeError("This methold only accepts a dictionary.")
        else:
            i=0
            for key in settings:
                if key!="CPU" and key!="MEM" and key!="TYPE":
                    raise VauleError("Provided settings should only have CPU,MEM,TYPE as keys.")
                else:
                    i=i+1
            if i!=3:
                raise ValueError("The settings do not conform with expected format.")
            else:
                self.settings=settings
                self.set=True
    def set_file_obj_cpu(self,cpu):
        """This methold sets the cpu field.\n
        WARNING:This methold will enable reading of the file_object but may cause undefined effects."""
        if isinstance(cpu,dict())!=True:
            raise TypeError("This methold only accepts a dictionary.")
        else:
            self.cpu=cpu
            self.set=True
    def set_file_obj_memory(self,memory):
        """This methold sets the memory field.\n
        WARNING:This methold will enable reading of the file_object but may cause undefined effects."""
        if isinstance(memory,dict())!=True:
            raise TypeError("This methold only accepts a dictionary.")
        else:
            self.memory=memory
            self.set=True
    def save_file_object(self,file_name,option = "NULL"):
        """This methold will take a file_object and a filename and will write to a file a saved version
        which is compatible with import_into_file_object.
        option defaults to creating a new file.
        option=overwrite will cause this methold to overwrite the given file.\n
        WARNING:This methold may not be used when the given file_object has not been set."""
        if self.set!=True:
            raise FileObjNotSet("")
        elif option=="new" and option=="overwrite" and option=="NULL":
            print(option)
            raise ValueError("The option is invalid.")
        elif isinstance(file_name,type(str()))!=True:
            raise TypeError("The provided file_name must be a string")
        else:
            settings=self.settings
            cpu=self.cpu
            memory=self.memory
            saved_settings=[]
            for key in settings:
                temp=key
                temp2=str(settings[key])
                temp=temp+temp2
                saved_settings.append(temp)
            saved_cpu=[]
            for frame_label in cpu:
                local_frame=["/"+frame_label]
                local_frame_dict=cpu[frame_label]
                for key in local_frame_dict:
                    temp=key
                    temp2=str(local_frame_dict[key])
                    temp=temp+":"+temp2
                    local_frame.append(temp)
            for line in local_frame:
                saved_cpu.append(line)
            saved_memory=[]
            for frame_label in memory:
                local_frame=["/"+frame_label]
                local_frame_dict=memory[frame_label]
                for key in local_frame_dict:
                    temp=key
                    temp2=str(local_frame_dict[key])
                    temp=temp+":"+temp2
                    local_frame.append(temp)
            for line in local_frame:
                saved_memory.append(line)
            if option=="new" or option=="NULL":
                try:
                    file=open(file_name+".sav","x")
                    file.close()
                except:
                    raise FileExistsError("The file "+str(file_name)+".sav already exists and can not be created")
            elif option=="overwrite":
                try:
                    file=open(file_name+".sav","r")
                    file.close()
                except:
                    raise FileNotFoundError("The file "+str(file_name)+".sav does not exists and can not be overwritten.")
            with open(file_name+".sav","w") as file:
                for line in saved_settings:
                    file.write(line+'\n')
                file.write("-CPU-\n")
                for line in saved_cpu:
                    file.write(line+"\n")
                file.write("-MEM-\n")
                for line in saved_memory:
                    file.write(line+"\n")



###Custom exceptions here###

class InvalidFileError(Exception):
    """Raised when the file is not a valid format."""
    pass



class FileObjNotSet(Exception):
    """Raised when a read is attempted on a non-set file_object."""
    pass



if __name__ == "__main__":
    help(file_object())
    help(InvalidFileError)
    help(FileObjNotSet)
