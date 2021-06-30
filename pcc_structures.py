from pcc_utils import *
from enum import Enum

class pcc_base_table:
    def __init__(self):
        self._items = []
    
    def __getitem__(self, _name):
        for item in self._items:
            if item._name == _name: return item
        return None
    
    def __contains__(self, _name):
        return self[_name] is not None

class pcc_type:
    def __init__(self, _name, _size, _is_compatible):
        assert(is_str(_name) and is_int(_size) and is_lambda(_is_compatible))
        self._name = _name
        self._size = _size
        # self._is_compatible("lalala") == checks if string "lalala" is compatible with type
        self._is_compatible = _is_compatible
    
    def can_cast_to(self, other_type):
        assert(type(other_type)==pcc_type)
        return self._size <= other_type._size 

class pcc_type_table(pcc_base_table):
    def __init__(self):
        super().__init__()
        self.typedef("void", 0, (lambda x: False))
        self.typedef("char", 4, (lambda x: is_str(x)))
        # TODO: complete
    
    def typedef(self, _name, _size, _assign_valid):
        if _name in self: raise Exception("Cannot override existing type")
        self._items.append(pcc_type(_name, _size, _assign_valid))


class pcc_operator:
    def __init__(self, _symbol, _single, _parse):
        assert(is_str(_symbol) and is_lambda(_parse) and type(_single)==bool)
        self._symbol = _symbol
        self.single = _single
        self.parse = _parse


class pcc_identifier:
    def __init__(self, _type, _name):
        assert(is_str(_name))
        if not is_valid_identifier(_name): raise Exception("Invalid identifier")
        self._type = _type
        self._name = _name

class pcc_identifier_table(pcc_base_table):
    def __init__(self):
        super().__init__()
    
    def define(self, _identifier):
        if _identifier._name in self: raise Exception("Identifier already defined")
        self._items.append(_identifier)
        # TODO dont allow defining after existing pcc type


class pcc_expression:
    def __init__(self, _exp1, _operator=None, _exp2=None, _cast=None):
        assert(type(_cast)==pcc_type)
        assert((_operator is None and _exp2 is None) or (_operator is not None and _exp2 is not None))
        self._exp1 = _exp1
        self._exp2 = _exp2
        self._operator = _operator
        self._return_type = _exp1._type
        if _exp2 is not None and _exp1._size>=_exp2._size: self._return_type =_exp2._type
        self._size = self._return_type._size
        if _cast: self._return_type = _cast


class pcc_literal:
    def __init__(self, _content):
        self._content = _content
    
    def __add__(self, other):
        self._content += other._content
    def __radd__(self, other): self.__add__(other)


class pcc_literal_table:
    def __init__(self):
        self._literals = []
    
    def __add__(self, _literal):
        self._literals.append(_literal)
    def __radd__(self,_literal):
        self.__add__(_literal)
    def __getitem__(self,i):
        return self._literals[i]
    
    def join(self, i, j):
        literals = self._literals[:i]
        newliteral = self._literals[i]
        i+=1
        while i<j:
            newliteral+=self._literal[i]
            i+=1
        literals.append(newliteral)
        literals += self._literals[j:]
        self._literals = literals


class pcc_operator_table(pcc_base_table):
    def __init__(self):
        super().__init__()
    
    def append(self, _operator):
        assert(type(_operator)==pcc_operator)
        self._items.append(_operator)



class pcc_single_expression(pcc_expression):
    def __init__(self, _identifier, _operator=None, _cast=None):
        assert(type(_identifier)==pcc_identifier)
        assert(_operator==None or (type(_operator)==pcc_operator and _operator.single))
        assert(_cast==None or (type(_cast)==pcc_type))
        _return_type = _identifier._type if not _cast else _cast
        super().__init__(_return_type, _operator)
        self._identifier = _identifier
        self._operator = _operator

    def eval(self):
        super().eval()
        pass

class pcc_double_expression(pcc_expression):
    def __init__(self, _exp1, _operator, _exp2):
        assert(_exp1 is not None and issubclass(type(_exp1),pcc_expression))
        assert(_exp2 is not None and issubclass(type(_exp2),pcc_expression))
        assert(type(_operator)==pcc_operator and not _operator.single)
        _return_type = _exp1._return_type if _exp1._size>=_exp2._size else _exp2._return_type
        super().__init__(_return_type, _operator)
        self._exp1 = _exp1
        self._exp2 = _exp2
    
    def eval(self):
        super().eval()
        pass

class pcc_declaration:
    pass


'''class pcc_double_expression:
    # can only be initialized with an identifier
    # this way we can nest expressions
    def __init__(self, _identifier, _self_operator=None, _cast=None):
        assert(type(_identifier)==pcc_identifier)
        assert(_self_operator==None or \
            (type(_self_operator)==pcc_operator and _self_operator.single))
        assert(_cast==None or type(_cast)==pcc_type)
        self._return_type = _identifier._type
        self._size = self._return_type._size
        self._identifier = _identifier
        self._operator = _self_operator
        self._expression = None # provided in join
        if _cast:
            if _cast._size < self._size: raise Exception("Invalid cast")
            self._return_type = self._cast
            self._size = self._return_type._size
    
    def join(self, _operator, _expression):
        assert(_operator is None) # must be appended from outside
        if type(_expression)==pcc_identifier: _expression = pcc_expression(_expression)
        assert(type(_expression)==pcc_expression)
        if self._expression is None:
            self._operator = _operator
            self._expression = _expression
        else:
            self._expression.join(_operator, _expression)
    
    def eval(self):
        if self._operator == None:
            return ""
        return "\n"

class pcc_expression:
    def __init__(self, _exp1=None, _operand=None, _exp2=None, _cast=None):
        self._return_type = _exp1._type
        self._size = self._return_type._size
        self._exp1 = _exp1
        self._operand = _operand
        self._exp2 = None
        self.append(_operand, _exp2)
        self.cast(_cast)

        self._exp2 = _exp2
        self._operand = _operand
        if _operand is None:
            assert(_exp2 is None)
            self._return_type == _exp1._type
            self._size = self._return_type._size
        else: # take type of larger expression, I guess, or first if same
            assert(type(_exp2)==pcc_expression or type(_exp2)==pcc_identifier)
            if type(_exp2)==pcc_identifier: _exp2 = pcc_expression(_exp2)
            
        self._return_type = _cast
    
    def append(self, _operand, _exp):
        assert(self._exp1 is not None)
        assert((type(_operand)==str and type(_exp)==pcc_expression) or \
            (_operand==None and _exp==None))
        if type(_operand)==str and type(_exp)==pcc_expression:
            self._operand = _operand
            self._exp2 = _exp2


    def add(self, _operand, _exp2):
        assert(type(_operand)==str)
        assert(type(_exp2)==pcc_expression)
        self._operand = _operand
        self._exp2 = _exp2
    
    def parse(self): # convert to instructions
        return ""'''