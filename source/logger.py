from rich.console import Console
from rich_gradient import Gradient
console = Console()

def error(msg):
    console.print(Gradient("[Error] ", colors=["#bd1722", "#4d0606"]) + str(msg))

def info(msg):
    console.print(Gradient("[Info] ", colors=["#17bda9", "#a717bd"]) + str(msg))

def sended(msg):
    console.print(Gradient("[Server] ", colors=["#14f57d", "#32f514"]) + str(msg))

def nosended(msg):
    console.print(Gradient("[Server] ", colors=["#f0db24", "#f55714"]) + str(msg))