import numpy
from pandas import Period


"""-
Hello World class
-"""
class HelloWorld:
    
    """-
    Initialize

    :param str msg: Message to send
    :param str again: Message to send

    :err ThrowableError: Big bad error
    -"""
    def __init__(self, msg: str) -> None:
    
        self.msg = msg

    """-
    Say hello

    :return str msg: Hello message
    -"""
    def say_hello(self) -> str:
        return f"Hello!!"
    
    """-
    Print a message

    :return str msg: message to print
    -"""
    def print_msg(self) -> str:
        return f"msg: f{self.msg}"


