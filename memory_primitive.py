#Hi
"""
This class handles storing information for other classes
"""



class memory_primitive():
    """
    This class handles memory for all of the other classes
    This class has no internal state that is intended to be modified externally and should not be modified
    This class has the following components:
    -list: Stores data
    -size: Limits max address value
           Must weither be a non-negative integer or -1
           -1 means no addresses are valid for writing or reading
    -set_type: Dictates valid types to be stored

    TODO Change __list to __dict
    """
    def __init__(self):
        """
        Automatically creates an instance with no data
        This instance has the following settings:
        -No data
        -size -1 (eg. no addresses are valid)
        -all types allowed
        """
        self.__list={}
        self.__size=-1
        self.__set_type="any"
    def set_size(self,size):
        """
        Sets size
        size must be an non-zero integer or -1
        """
        if isinstance(size,type(int)) == False:
            raise TypeError("size must be a integer")
        elif size<-1:
            raise ValueError("size can not be neagtive other than -1")
        self.__size=input
        data_addresses=self.__list.keys
        for address in data_addresses:
            if address>size:
                del self.__list[address]
            else:
                pass
    def set_valid_type(self,set_type):
        """
        Sets set_type
        """
        if isinstance(set_type,type(str))==False:
            # could be an tuple
            if isinstance(set_type,type(tuple))==False:
                raise TypeError("type must either be a string or tuple with only strings")
            else:
                # check to make sure that all elements of the tuple is a string
                for element in set_type:
                    if instance(set_type,type(str))==False:
                        raise ValueError("set_type must only have strings as elements if it is a tuple")
                    else:
                        pass
            # check has passed, we can proceed to checking input values
        else:
            pass
        # define all valid set_type
        # !!!Don't forget to change the internal validation functions if you change this!!!
        valid_set_types=["binary string",
                         "int","pos int","neg int","pos+0 int","neg+0 int","0 only",
                         "float","pos float","neg float","pos+0 float","neg+0 float",
                         "string",
                         "list",
                         "tuple",
                         "dict",
                         "any"]
        internal_validate_set_type(set_type,valid_set_types)
        # no error? update the appropiate attribiute
        self.__set_type=set_type
        if isinstance(set_type,type(str))==True or len(set_type)==1:
            invalid_keys=internal_valid_data_type_single_valid(self.__list,set_type)
        else:
            invalid_keys=internal_valid_data_dict_given_set_type(self.__list,set_type)
        for invalid_key in invalid_keys:
            del self.__list[invalid_key]
    def write_data(self,data,address):
        """
        Writes data to address
        Address and data must be valid
        """
        # need validation of input
        if isinstance(address,type(int))!=True:
            raise TypeError("address must be a valid int. use help(memory_primitive) to viwe requirements")
        else:
            pass
        if address<-1 or address>self.__size:
            raise ValueError("address must be a valid int.  use help(memory_primitive) to viwe requirements")
        else:
            pass
        # address validate, what about data input?
        set_type=self.__set_type
        if internal_validate_single_data_using_set_type(data.set_type)==False:
            raise TypeError("data does not match set_type")
        else:
            if data==0:
                # null option, do not write to memory
                #check to see if address has been writen to dict
                try:
                    data=self.__list[address]
                    del self.__list[address]
                except:
                    # no data there, no need to delete non-existent data
                    pass
            else:
                self.__list[address]=data
    def read_data(self,address):
        """
        Reads data from address
        Address must be valid
        """
        if isinstance(address,type(int))!=True:
            raise TypeError("address must be a valid int. use help(memory_primitive) to viwe requirements")
        else:
            pass
        if address<-1 or address>self.__size:
            raise ValueError("address must be a valid int.  use help(memory_primitive) to viwe requirements")
        else:
            pass
        dict_keys=self.__list.keys()
        key_found=False
        for key in dict_keys:
            if key==address:
                key_found=True
                break
            else:
                pass
        if key_found==True:
            # there is data at the address location
            data=self.__list[address]
        else:
            # null option which means input of zero
            data=0
        return(data)



def internal_validate_set_type(set_type,valid_set_types):
    """
    Internal function
    Do not tamper with
    Used in set_valid_type
    Automatically error out when incorrect set_type is detected
    """
    if isinstance(set_type,type(str))==True:
        #easy case, just loop over valid_set_types
        set_type_found=False
        for valid_set_type in valid_set_types:
            if set_type==valid_set_type:
                set_type_found=True
                break
            else:
                pass
        if set_type_found==False:
            raise ValueError("set_type must be a valid set_type/set. use help(memory_primitive) to view valid set_type")
        else:
            pass
    else:
        # we have a tuple here
        # now we must run checks on each element
        list_number=len(set_type)
        validated_set_type=0
        for element in set_type:
            set_type_found=False
            for valid_set_type in valid_set_types:
                if element==valid_set_type:
                    set_type_found=True
                    validated_set_type=validated_set_type+1
                    break
                else:
                    pass
            if set_type_found==False:
                raise ValueError("set_type must be a valid set_type/set. use help(memory_primitive) to view valid set_type")
            elif list_number!=validated_set_type:
                # wait, we don't have every single set_type validated
                raise ValueError("set_type must be a valid set_type/set. use help(memory_primitive) to view valid set_type")
            else:
                pass



def internal_valid_data_dict_given_set_type(data_dict,valid_types):
    """
    Internal function
    Do not tamper with
    Used in set_valid_type
    Returns list of invalid keys
    """
    addresses=data_dict.keys()
    invalid_addresses=[]
    # select address
    for address in addresses:
        # now check for correctness
        data=data_dict[address]
        if internal_validate_single_data_using_set_type(data,valid_types)==False:
            invalid_addresses.append(address)
    return(invalid_addresses)



def internal_validate_single_data_using_set_type(data,set_type):
    """
    Internal function
    Do not tamper with
    Used in !!!!TO_INCLUDE!!!!
    This function takes in a single input to be inspected with a set_type
    It returns a boolean depending on validity
    """
    valid_type_matched=False
    if isinstance(set_type,type(tuple))==True:
        for valid_type in set_type:
            if valid_type=="binary string":
                try:
                    x=int(data,2)
                    valid_type_matched=True
                    continue
                except:
                    pass
            elif valid_type=="int":
                if isinstance(data,type(int))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="pos int":
                if isinstance(data,type(int))==True and data>0:
                    valid_type_matched=True
                    continue
            elif valid_type=="neg int":
                if isinstance(data,type(int))==True and data<0:
                    valid_type_matched=True
                    continue
            elif valid_type=="pos+0 int":
                if isinstance(data,type(int))==True and data>-1:
                    valid_type_matched=True
                    continue
            elif valid_type=="neg+0 int":
                if isinstance(data,type(int))==True and data<1:
                    valid_type_matched=True
                    continue
            elif valid_type=="0 only":
                if isinstance(data,type(int))==True and data==0:
                    valid_type_matched=True
                    continue
            elif valid_type=="float":
                if isinstance(data,type(float))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="pos float":
                if isinstance(data,type(float))==True and data>float(0):
                    valid_type_matched=True
                    continue
            elif valid_type=="neg float":
                if isinstance(data,type(float))==True and data<float(0):
                    valid_type_matched=True
                    continue
            elif valid_type=="pos+0 float":
                if isinstance(data,type(float))==True and data>=float(0):
                    valid_type_matched=True
                    continue
            elif valid_type=="neg+0 float":
                if isinstance(data,type(float))==True and data<=float(0):
                    valid_type_matched=True
                    continue
            elif valid_type=="string":
                if isinstance(data,type(str))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="list":
                if isinstance(data,type(list))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="tuple":
                if isinstance(data,type(tuple))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="dict":
                if isinstance(data,type(dict))==True:
                    valid_type_matched=True
                    continue
            elif valid_type=="any":
                # liteally anything goes
                valid_type_matched=True
            else:
                raise RuntimeError("WTF? Unexpected valid type entry here")
            if valid_type_matched==False:
                return(False)
            else:
                return(True)
    else:
        # single set type
        if valid_type=="binary string":
            try:
                x=int(data,2)
                valid_type_matched=True
            except:
                pass
        elif valid_type=="int":
            if isinstance(data,type(int))==True:
                valid_type_matched=True
        elif valid_type=="pos int":
            if isinstance(data,type(int))==True and data>0:
                valid_type_matched=True
        elif valid_type=="neg int":
            if isinstance(data,type(int))==True and data<0:
                valid_type_matched=True
        elif valid_type=="pos+0 int":
            if isinstance(data,type(int))==True and data>-1:
                valid_type_matched=True
        elif valid_type=="neg+0 int":
            if isinstance(data,type(int))==True and data<1:
                valid_type_matched=True
        elif valid_type=="0 only":
            if isinstance(data,type(int))==True and data==0:
                valid_type_matched=True
        elif valid_type=="float":
            if isinstance(data,type(float))==True:
                valid_type_matched=True
        elif valid_type=="pos float":
            if isinstance(data,type(float))==True and data>float(0):
                valid_type_matched=True
        elif valid_type=="neg float":
            if isinstance(data,type(float))==True and data<float(0):
                valid_type_matched=True
        elif valid_type=="pos+0 float":
            if isinstance(data,type(float))==True and data>=float(0):
                valid_type_matched=True
        elif valid_type=="neg+0 float":
            if isinstance(data,type(float))==True and data<=float(0):
                valid_type_matched=True
        elif valid_type=="string":
            if isinstance(data,type(str))==True:
                valid_type_matched=True
        elif valid_type=="list":
            if isinstance(data,type(list))==True:
                valid_type_matched=True
        elif valid_type=="tuple":
            if isinstance(data,type(tuple))==True:
                valid_type_matched=True
        elif valid_type=="dict":
            if isinstance(data,type(dict))==True:
                valid_type_matched=True
        elif valid_type=="any":
            # liteally anything goes
             valid_type_matched=True
        else:
            raise RuntimeError("WTF? Unexpected valid type entry here")
        if valid_type_matched==False:
            return(False)
        else:
            return(True)


if __name__=="__main__":
    help(memory_primitive)