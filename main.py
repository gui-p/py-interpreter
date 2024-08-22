from enum import Enum


class Type(Enum):
    INTEGER = 1
    PLUS = 2
    EOF = 3
    SUB = 4
    MULT = 5

class Token(object):
    def __init__(self, type: Type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type = self.type,
            value = self.value
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self) -> Token:
        text = self.text

        if self.pos > len(text) - 1:
            return (Token(Type.EOF, None))
        
        current_char = text[self.pos]

        while current_char.isspace():
            text_ended = (self.pos+1 > len(text) -1)
            if not text_ended:
                self.pos+= 1
                current_char = text[self.pos]
            else:
                return (Token(Type.EOF, None))

        
        
        if current_char.isdigit():  
            digits: str = ''          
            while True:
                digits += current_char
                
                text_ended = (self.pos+1 > len(text) -1)
                if  not text_ended and (text[self.pos+1].isdigit()):
                    self.pos += 1
                    current_char = text[self.pos]
                else:
                    self.pos += 1
                    break
            return Token(Type.INTEGER, int(digits))
            
        
        if current_char == '+':
            self.pos +=1
            return Token(Type.PLUS, current_char)
        
        if current_char == '-':
            self.pos +=1
            return Token(Type.SUB, current_char)
        
        if current_char == '*':
            self.pos +=1
            return Token(Type.MULT, current_char)
        
        self.error()


    def eat(self, token_type):
        if self.current_token.type in token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat([Type.INTEGER])

        op = self.current_token 
        self.eat([Type.PLUS, Type.SUB, Type.MULT])

        right = self.current_token
        self.eat([Type.INTEGER])

        self.eat([Type.EOF])

        if (op.value == '+'):
            result = left.value + right.value
        elif(op.value == '-'):
            result = left.value - right.value
        elif(op.value == '*'):
            result = left.value * right.value
        
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        
        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

    return


if __name__ == '__main__':
    main()