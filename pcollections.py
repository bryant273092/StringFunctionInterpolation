#Submitter: bryanth1(Hernandez, Bryant)

import re, traceback, keyword

def pnamedtuple(type_name, field_names, mutable= False):
    def show_listing(s):
        for line_num, line_text in enumerate(s.split('\n'), 1):
            print(f' {line_num: >3} {line_text.rstrip()}')

    # put your code here
    def is_legal(name):
        if type(name) is str:
            if name not in keyword.kwlist:
                if re.match('[a-zA-Z]\w*', name):
                    return True
        return False
    def unique(iterable):
        iterated = set()
        for i in iterable:
            if i not in iterated:
                iterated.add(i)
                yield i
    
    if not is_legal(type_name):           
        raise SyntaxError('illegal type name')
    
    if type(field_names) is str:
        field_names = field_names.replace(',', ' ').split()
        field_names = list(unique(field_names))
        for name in field_names:
            if not is_legal(name):
                raise SyntaxError('illegal field name')   
    elif type(field_names) is list:
        for name in field_names:
            if not is_legal(name):
                raise SyntaxError('illegal field name')   
    else:
        raise SyntaxError('illegal field names')
    
    class_template = ''' 
    
class {type_name}:
    def __init__(self, {field_names}):
        {gen_init}
        self._fields = [{field_names2}]
        self._mutable = {mutable}
    def __repr__(self):
        return '{type_name}({param})'.format({param_fmt})
    {get_methods}
    def __getitem__(self,index):
        if type(index) not in [int,str]:
            raise IndexError('Object.__getitem__: index('+str(index)+') must be str or int('+type_as_str(index)+')')
        if type(index) is str: 
            if index in self.__dict__: 
                return self.__dict__[index]
            else:
                raise IndexError('Object.__getitem__: index('+str(index)+') does not exist)')
        if type(index) is int: 
            if index < len(self._fields):
                return self._fields[index]
            else:
                raise IndexError('Object.__getitem__: index('+str(index)+') out of index range')
    def __eq__(self, object2):
        if type(self) == type(object2):
            try:
                for item in self._fields:
                    if self._fields[item] != object2._fields[item]:
                        return False 
                return True
            except IndexError:
                return False
        else:
            return False
                
    
                
              '''          
        
        
        
        
    init_template = 'self.{field_name} = {field_name}'   
    get_template = '''
    def get_{attr_name}(self):
        return self.{attr_name}
        '''
    class_definition = class_template.format(
        type_name = type_name,
        field_names = ', '.join(name for name in field_names),
        mutable = mutable,
        gen_init = '\n        '.join([init_template.format(field_name = field_name) for field_name in field_names]),
        param = ','.join("{var}=".format(var = var)+ '{'+'{var}'.format(var = var)+'}' for var in field_names), 
        param_fmt = ','.join('{var} = self.{var}'.format(var = var) for var in field_names),
        get_methods = '          '.join(get_template.format(attr_name = attr_name) for attr_name in field_names),
        field_names2 =','.join(str(name)for name in field_names)
         )
    # bind class_definition (used below) to the string constructed for the class



    # While debugging, remove comment below showing source code for the class
    # show_listing(class_definition)
    
    # Execute this class_definition str in a local name space; then, bind the
    #   source_code attribute to class_defintion; after that try, return the
    #   class object created; if there is a syntax error, list the class and
    #   also show the error
    name_space = dict(__name__  =  f'pnamedtuple_{type_name}'.format(type_name = type_name))
    try:
        exec(class_definition,name_space)
        name_space[type_name].source_code = class_definition
    except (TypeError,SyntaxError):   
        show_listing(class_definition)
        traceback.print_exc()
    return name_space[type_name]


    
if __name__ == '__main__':
    Triple1 = pnamedtuple('Triple1', 'a b c')
    t1 = Triple1(1,2,3)
    
    # Test pnamedtuple in script below: use 

    #driver tests
    import driver
    driver.default_file_name = 'bscp3S18.txt'
#     driver.default_show_exception= True
#     driver.default_show_exception_message= True
#     driver.default_show_traceback= True
    driver.driver()
