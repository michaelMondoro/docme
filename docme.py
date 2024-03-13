from dataclasses import dataclass, field
import re 
from flask import Flask, render_template

@dataclass 
class Err:
    type: str
    desc: str

@dataclass
class Arg:
    raw: str
    name: str
    type: str
    desc: str 
    isret: bool = False

    def __post_init__(self):
        self.isret = ":return " in self.raw 
    
    def __repr__(self) -> str:
        if self.isret:
            return f"ReturnArg({self.name}, {self.type}, {self.desc})"
        else:
            return f"ParamArg({self.name}, {self.type}, {self.desc})"

class DocString:
    def __init__(self, string, declaration):
        self.desc = self._parse_desc(string)
        self.name =  self._parse_name(declaration)
        self.args = self._parse_args(string)
        self.errs = self._parse_errs(string)
        self.decl = declaration.strip(":")

    def _parse_name(self, string) -> str:
        return string.split()[1].strip().split('(')[0].strip(":")
    
    def _parse_desc(self, string) -> str:
        return string.split("\n")[0].strip()

    def _parse_errs(self, string) -> list[str]:
        errs = []
        for i in string.split("\n"):
            if len(i) > 0 and (":err " in i):
                err_desc = i.split(":")[-1]
                err_type = i.split(":")[1].split()[1]
                errs.append(Err(type=err_type, desc=err_desc))

        return errs

    def _parse_args(self, string) -> list[str]:
        args = []
        for i in string.split("\n"):
            if len(i) > 0 and (":param " in i) or (":return " in i):
                arg_desc = i.split(":")[-1]
                arg_type = i.split(":")[1].split()[1:][0]
                arg_name = i.split(":")[1].split()[1:][1]
                args.append(Arg(raw=string, name=arg_name, type=arg_type, desc=arg_desc))

        return args

    def __repr__(self) -> str:
        return f"{self.name}, {self.desc}"



class DocMe:
    
    def __init__(self) -> None:
        pass

    def build():
        pass

    def run() -> list[DocString]:
        docstrings = []
        declarations = []
        read = False
        with open('test.py','r') as f:
            content = []
            for line in f.readlines():
                if '"""-' in line and not read:
                    read = True
                elif '-"""' in line and read:
                    read = False
                    docstrings.append(" ".join(i for i in content))
                    content = []
                elif read:
                    content.append(line)   
                elif re.search('class .*:', line) or re.search('def .*:', line):
                    declarations.append(line.strip())

        items = []
        for (i, docstring) in enumerate(docstrings):
            items.append(DocString(docstring, declarations[i]))

        return items
    


app = Flask(__name__)

@app.route("/")
def home():
    doc = DocMe()
    docs = DocMe.run()
    return render_template('index.html', title='DocMe', docs=docs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)