import ast
import random

randomchar = "_0x" + ''.join(random.choices([str(i) for i in range(1, 10)], k=4))

def obfstr(v):
    if v == "":
        return f"''"
    else:
        repr_chars = [repr(c) for c in v]
        tachstring = '+'.join(repr_chars)
        return f'(lambda {randomchar} : {tachstring})("{randomchar}")'

def obfint(v):
    return f"{v}"

def fm(node: ast.JoinedStr) -> ast.Call:
    return ast.Call(
        func=ast.Attribute(
            value=ast.Constant(value='{}'*len(node.values)),
            attr="format",
            ctx=ast.Load()
        ),
        args=[value.value if isinstance(value, ast.FormattedValue) else value for value in node.values],
        keywords=[]
    )

def obfuscate(node):
    for i in ast.walk(node):
        for f, v in ast.iter_fields(i):
            if isinstance(v, list):
                ar = []
                for j in v:
                    if isinstance(j, ast.Constant) and isinstance(j.value, str):
                        ar.append(ast.parse(obfstr(j.value)).body[0].value)
                    elif isinstance(j, ast.Constant) and isinstance(j.value, int):
                        ar.append(ast.parse(obfint(j.value)).body[0].value)
                    elif isinstance(j, ast.JoinedStr):
                        ar.append(fm(j))
                    elif isinstance(j, ast.AST):
                        ar.append(j)
                if any(isinstance(elem, ast.Constant) and isinstance(elem.value, bool) for elem in v):
                    setattr(i, f, v)
                else:
                    setattr(i, f, ar)
            elif isinstance(v, ast.Constant) and isinstance(v.value, str):
                setattr(i, f, ast.parse(obfstr(v.value)).body[0].value)
            elif isinstance(v, ast.Constant) and isinstance(v.value, int):
                setattr(i, f, ast.parse(obfint(v.value)).body[0].value)
            elif isinstance(v, ast.JoinedStr):
                setattr(i, f, fm(v))

def random_if_else():
    return ast.If(
        test=ast.Compare(
            left=ast.Constant(value=False, kind=None),
            ops=[ast.Is()],
            comparators=[ast.Constant(value=True, kind=None)]
        ),
        body=[
            ast.Pass()
        ],
        orelse=[
            ast.Pass()
        ]
    )

def trycatch(body, loop):
    ar = []
    for x in body:
        j = x
        for _ in range(loop):
            j = ast.Try(
                body=[random_if_else()],
                handlers=[ast.ExceptHandler(
                    type=ast.Name(id='MemoryError', ctx=ast.Load()),
                    name=None,
                    body=[j]
                )],
                orelse=[],
                finalbody=[]
            )
            j.body.append(ast.Raise(
                exc=ast.Call(
                    func=ast.Name(id='MemoryError', ctx=ast.Load()),
                    args=[ast.Str(s="Ngocuyencoder")],
                    keywords=[]
                ),
                cause=None
            ))
        ar.append(j)
    return ar

def obf(code, loop):
    tree = ast.parse(code)
    obfuscate(tree)
    tbd = trycatch(tree.body, loop)
    def ast_to_code(node):
        return ast.unparse(node)
    j = ast_to_code(tbd)
    return j

code = r"""
print("hello world")
"""
# SỐ LOOP QUÁ CAO SẼ GÂY RA LỖI SyntaxError: too many statically nested blocks
loop = int(input("Nhập số loop cho try catch và if else :"))

for i in range(int(input("Nhập số loop cho string:"))):
    code = obf(code, loop)
open("ngocuyen.py","w",encoding="utf8").write(str(code))
