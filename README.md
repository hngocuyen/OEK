# ngocuyencoder 19/07/2008
## OEK - OBFUSCATION ENGINEERING KNOWLEDGE


- Xin chào tất cả mọi người mình là ngocuyencoder
- Hôm trước mình đã share về project outsource Velimatix
- Bây giờ là tới phần chia sẻ kiến thức (tất cả mọi kiến thức của mình về mảng này)
- Vốn dĩ ở Việt Nam ít ai chia sẻ kiến thức của bản thân về cái chủ đề này cả (Cảm giác như khá là nhạy cảm)
## Các part

- [BUILTINS FUNCTION](#builtins-function)
- [PYTHON BYTECODE](#python-bytecode)
- [SỬ DỤNG AST ĐỂ TẠO OBF CODE](#sử-dụng-ast-để-tạo-obf-code)
- [TƯ DUY VỀ OBF ,DEOBF](#gi-do-khong-biet)
- [HÀNH TRÌNH THAM GIA VÀO MẢNG NÀY CỦA NGOCUYENCODER](#Idk)
## BUILTINS FUNCTION
Đầu tiên là bước khởi đầu cho một xáo trộn cơ bản , khá là dễ khi bạn làm và sử dụng , dễ fix bug nhưng tính bảo mật thì ...
```python
> code = "print('hello world')"
> code = code.encode("utf8")
=> b"print('hello world')"
```
Cái raw đầu tiên cơ bản
Giờ thì chỉ việc thêm exec vào
```python
> exec(b"print('hello world')")
> hello world
```
Bên trên đây chính là cái raw cơ bản nhất, dễ hiểu nhất , chung quy là sử dụng exec để thực thi


Tiếp theo chúng ta có thể mix với các thư viện như base64 , zlib
```python
> import base64,zlib
> code = "print('hello world')"
```
Bug cơ bản nếu như bạn làm như này
```python
> base64.b64encode(code) : TypeError: a bytes-like object is required, not 'str'
```
Cách khắc phục là 
```python
> base64.b64encode(code.encode("utf8")) : b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='
```
Bây giờ chúng ta đã có một cái base64 để xáo trộn mã lên, Dùng __import__ để đẩy nhanh quá trình import thư viện
```python
> exec(__import__("base64").b64decode(b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='))
=> hello world
```

Vậy thì câu hỏi bây giờ là giải mã nó như nào ? 
Giải base64 ra ư?
Câu trả lời là NO, cũng được nhưng không hiểu quả
Vì vốn dĩ nó gọi b64decode rồi tới exec thì chúng ta chỉ cần thay thế exec = print là được
```python
> print(__import__("base64").b64decode(b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='))
>>> b"print('hello world')" Khi này nó ở dạng bytes thì mình sẽ chuyển nó về dạng thường
>>> b"print('hello world')".decode()
=> "print('hello world')"
```

Bây giờ mình sẽ mix thêm zlib và cả base64 và bz2
```python
> import base64,bz2,zlib
> code = "print('ngocuyen')"
> code = zlib.compress(bz2.compress(base64.b64encode(code.encode("utf8"))))
>>> b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'
```
Bây giờ đã có một dãy byte nén cực ảo diệu mình sẽ làm phần dịch ngược cho nó chạy được
```python
>>> exec(__import__("base64").b64decode(__import__("bz2").decompress(__import__("zlib").decompress(b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'))))
=> ngocuyen
```
Thay exec = print
```python
>>> print(__import__("base64").b64decode(__import__("bz2").decompress(__import__("zlib").decompress(b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'))))
>>> b"print('ngocuyen')"
>>> b"print('ngocuyen')".decode() : "print('ngocuyen')"
```

Suy ra là gì ? Suy ra là nó gọi hàm exec cuối cùng thì mình chỉ việc quan tâm tới nó thôi việc gì phải dịch từng cái zlib bz2 base64 một bởi vì nếu xáo trộn thì nó có sẵn rồi
Vậy thì nếu như là như này

```python
exec('exec(\'exec(\\\'exec("print(\\\\\\\'hello world\\\\\\\')")\\\')\')')
```

Được tạo lên bởi 
```python
loop = 5
xx = "print('hello world')"
data = xx

for x in range(loop - 1):
    data = f"exec({repr(data)})"

print(data)
```

Vậy thì chúng ta print nó sẽ rất là lâu, print từng cái một là một cái nhiệm vụ khó khăn nên , phương pháp ở đây là hooking

```python
hook = exec # tạo 1 biến clone để tránh bị đệ quy vô tận
def hooking(args):
    print(args)
    return hook(args)
# Code này vừa có nhiệm vụ thực thi cái hàm exec vừa có nhiệm vụ print ra những nội dung khi sử dụng hàm exec đó
exec = hooking #giờ mình đã thay thế exec = một hàm clone
```
Kết quả :
```python
exec('exec(\'exec("print(\\\'hello world\\\')")\')')
exec('exec("print(\'hello world\')")')
exec("print('hello world')")
print('hello world')
hello world
```

Bạn thấy không , thực sự nó rất là hay , cực kì hay , đó là những bước cơ bản đầu tiên để hiểu về obf và deobf
Giải thích sâu xa hơn thì tất cả mọi hàm có sẵn ở python thì đều có thể bị hook kể cả input hay print int float chr vân vân miễn là thuộc builtins
Vì lý do như vậy chúng ta có thể bảo mật bằng cách tự write một cái hàm mới cho mấy cái này để tránh hooking nhưng mình nghĩ cái đó để sau vì mang tính nâng cao rồi 
## PYTHON BYTECODE
Trong Python, marshal là một mô-đun chuẩn được sử dụng để tuần tự hóa và giải tuần tự hóa các đối tượng Python. marshal thường được sử dụng bên trong Python để lưu trữ các đối tượng biên dịch như mã bytecode của Python, thường trong các tệp .pyc hoặc

Với marshal thì hắn cũng dùng exec nhưng chúng ta không thể hooking ra code được bởi vì nó không phải string mà là bytecode, cách chúng ta có thể dịch nó là dựa vào module dis


Ví dụ về cách tạo ra một python bytecode bằng marshal
```python
> import marshal;marshal.dumps(compile("print('hello')","urname","exec"))
>>> b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xf3\x1c\x00\x00\x00\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x01S\x00)\x02\xda\x05helloN)\x01\xda\x05print\xa9\x00\xf3\x00\x00\x00\x00\xda\x06urname\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x16\x00\x00\x00\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80g\x81\x0e\x84\x0e\x80\x0e\x80\x0e\x80\x0er\x04\x00\x00\x00'
```

nó ra một dãy byte như vậy và việc tiếp theo cần làm là
```python
> exec(__import__("marshal").loads(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xf3\x1c\x00\x00\x00\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x01S\x00)\x02\xda\x05helloN)\x01\xda\x05print\xa9\x00\xf3\x00\x00\x00\x00\xda\x06urname\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x16\x00\x00\x00\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80g\x81\x0e\x84\x0e\x80\x0e\x80\x0e\x80\x0er\x04\x00\x00\x00'))
>>> hello
```python
Bạn hãy thử thay thế exec = print hoặc hooking đi thì nó cũng sẽ ra : <code object <module> at ...
Bởi vì nó là bytecode chứ không phải string, python compile hay gọi là pyc, muốn hiểu được nó thì thay thế exec = __import__("dis").dis

Mô-đun dis trong Python là một công cụ giúp phân tích và hiển thị mã bytecode của Python. Bytecode là một dạng trung gian của mã nguồn Python được biên dịch, và dis có thể được sử dụng để giải mã bytecode này thành một dạng có thể đọc được để kiểm tra và gỡ lỗi.

```python
  0           0 RESUME                   0

  1           2 PUSH_NULL
              4 LOAD_NAME                0 (print)
              6 LOAD_CONST               0 ('hello')
              8 PRECALL                  1
             12 CALL                     1
             22 POP_TOP
             24 LOAD_CONST               1 (None)
             26 RETURN_VALUE
```


Thật sự thì mình cũng chẳng muốn lằng nhằng giải thích pop nọ pop kia
bạn sẽ giải thích 3 cái opcode LOAD_NAME LOAD_CONST PRECALL

PRECALL sẽ là dùng để gọi một function 
LOAD_NAME sẽ là cái đứng trước LOAD_CONST như print
LOAD_CONST sẽ là giá trị

Não mình dis được như sau
```python
PRECALL LOAD_NAME(print) LOAD_CONST('hello')
Kết quả cuối cùng : print('hello')
```

Chỉ một dòng `print('hello')` khi compile thành bytecode thì đã rất phức tạp rồi , vậy thì câu hỏi đặt ra là làm sao để dịch và có công cụ nào hỗ trợ không thì tất nhiên là có
Đề cử : pycdc và uncompyle6
Nhưng thật sự tác giả của họ hơi "lười" vì có vài bug ở issue mà không chịu fix
với pycdc thì chúng ta sẽ được support python3.10 trở lên , càng update python càng khó dịch hơn
còn nếu không muốn sử dụng công cụ thì hãy tự tạo cho bản thân một cái mini cơ bản bằng cách syntax từng opcode một
Dưới đây là một mini pyc decompile bởi me sử dụng vm để thực thi, syntax cho từng opcode và dịch ra

```python

x = __import__("marshal").loads(yourbytemarshal)
k = (
x.co_code,x.co_consts,x.co_names
)

LOAD_CONST = 100
LOAD_NAME = 101
BINARY_OP = 122
POP_TOP = 1
STORE_NAME = 90
RETURN_VALUE = 83
STORE_NAME    = 90
PRECALL = 166
MAKE_FUNCTION = 132
src = []
def vm(code, consts, name):
    j = 0
    v = []
    push = v.append
    pop = v.pop
    varp = vars(__builtins__)
    while j < len(code):
        opcode = code[j]
        arg = code[j + 1]
        if opcode==LOAD_CONST:
            const = consts[arg]
            push(const)
            #src.append(const)
        if opcode == POP_TOP:
                pop()
        if opcode == BINARY_OP:
                x = pop()
                y = pop()
                push(y+x)
                z = (f"({y} + {x})")

        if opcode == LOAD_NAME:
                names = name[arg]
                names = varp[names]
                push(names)
                #src.append(names)
        if opcode == STORE_NAME:
                a=pop()
                names = name[arg]
                varp[names] = a
                src.append(f"{names} = {varp[names]}")
        if opcode == RETURN_VALUE:
                return pop()
        if opcode == PRECALL:
                stdcargs = []
                num_args = arg
                for cx in range(arg):
                        stdcargs.insert(0, pop())
                function = pop()
                push(function(*stdcargs))
                if type(stdcargs[0]) == str:
                    src.append(f"{function.__name__}('{stdcargs[0]}')")
                elif type(stdcargs[0]) == int or type(stdcargs[0]) == float:
                    src.append(f"{function.__name__}({stdcargs[0]})")
        #if opcode == MAKE_FUNCTION:

        print(opcode)
        j += 2
vm(*k)
print('\n'.join(map(str,src)))
```
Mình đã thay thế biến yourbytemarshal bằng `b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xf3\x1c\x00\x00\x00\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x01S\x00)\x02\xda\x05helloN)\x01\xda\x05print\xa9\x00\xf3\x00\x00\x00\x00\xda\x06urname\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x16\x00\x00\x00\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80g\x81\x0e\x84\x0e\x80\x0e\x80\x0e\x80\x0er\x04\x00\x00\x00'`

và kết quả sau khi thực thi và yes đây chính là my mini bytecode decompile
```python
151
2
101
100
hello
166
0
171
0
0
0
0
1
100
print('hello')
```

Để có thể write được một pyc decompile thực sự rất khó nhai, mình syntax từng opcode mà mất tận 5 tiếng để fix bug lmao mà chỉ là mini thôi đấy



# SỬ DỤNG AST ĐỂ TẠO OBF CODE
Tiếp theo là AST , một module tuyệt vời để write ra python obf

Bước đầu là tạo cây bằng AST
```
import ast

def x(src):
    tree = ast.parse(src)
    print(ast.dump(tree, indent=2))

code = """python
def ngocuyencoder(n):
    abc = 1 + n
    print(abc)

print("hello")
"""

x(code)
```
>
```python
Module(
  body=[
    FunctionDef(
      name='ngocuyencoder',
      args=arguments(
        posonlyargs=[],
        args=[
          arg(arg='n')],
        kwonlyargs=[],
        kw_defaults=[],
        defaults=[]),
      body=[
        Assign(
          targets=[
            Name(id='abc', ctx=Store())],
          value=BinOp(
            left=Constant(value=1),
            op=Add(),
            right=Name(id='n', ctx=Load()))),
        Expr(
          value=Call(
            func=Name(id='print', ctx=Load()),
            args=[
              Name(id='abc', ctx=Load())],
            keywords=[]))],
      decorator_list=[]),
    Expr(
      value=Call(
        func=Name(id='print', ctx=Load()),
        args=[
          Constant(value='hello')],
        keywords=[]))],
  type_ignores=[])
```

Vậy bây giờ chúng ta có cú pháp rồi thì chúng ta làm cái gì?, cái dễ nhất là OBF STRING thành lambda
```python

def ngocuyencoder(n):
    abc = int1 + n
    print(200 + abc)
print("hello")
print(['hello'],["abc"])

```
=> 
```python
def ngocuyencoder(n):
    abc = int1 + n
    print(int((lambda: '200')()) + abc)
print((lambda: 'hello')())
print([(lambda: 'hello')()], [(lambda: 'abc')()])
```

Xác định string thuộc ast.Contast, tạo một function để obf nó

```python
import ast
# OBF STRING
def obfstr(v):
    # Tạo một cái lambda sẵn
    return f'(lambda : "{v}")()' 
# BIẾN SỐ NGUYÊN THÀNH STRING ĐỂ OBF
def obfint(v):
    return f'int("{v}")' # Trick khá hay về tư duy, khi mình sử dụng int và string , mình chỉ việc obf cái string bên trong int thôi
# Tạo thêm một hàm mới để thực hiện ast
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
                    elif isinstance(j, ast.AST):
                        ar.append(j)
                setattr(i, f, ar)
            elif isinstance(v, ast.Constant) and isinstance(v.value, str):
                setattr(i, f, ast.parse(obfstr(v.value)).body[0].value)
            elif isinstance(v, ast.Constant) and isinstance(v.value, int):
                setattr(i, f, ast.parse(obfint(v.value)).body[0].value)
                
def obf(src):
    tree = ast.parse(src)
    obfuscate(tree)
    return ast.unparse(tree)

code = """
print(1000)
print("ngocuyen")
"""

print(obf(code))


```
Kết quả thu được là
```python
print(int('1000'))
print((lambda: 'ngocuyen')())
```
Nếu như ta thay thế `print(obf(code))` thành
```python
for i in range(5):
    code = obf(code)
```
Thì kết quả thu được sau khi obf string là
```python
print(int((lambda: (lambda: (lambda: (lambda: '1000')())())())()))
print((lambda: (lambda: (lambda: (lambda: (lambda: 'ngocuyen')())())())())())
```
**Nhưng trước tiên là cùng giải thích hàm obfuscate**:
   - Đối với mỗi (`f`) và giá trị (`v`) trong  (`i`):
     - Nếu `v` là một danh sách (`isinstance(v, list)`), nó xử lý từng phần tử (`j`) trong danh sách:
       - Nếu `j` là một constant str (`ast.Constant` với `j.value` là một chuỗi), mình gọi `obfstr(j.value)` để obf và thay `j` thành (`ast.parse(obfstr(j.value)).body[0].value`).
       - Nếu `j` là một constant str (`ast.Constant` với `j.value` là một số nguyên), nó gọi `obfint(j.value)` để obf constant số nguyên tương tự.
       - Nếu `j` là một nút AST khác (`ast.AST`), nó giữ nguyên `j`.
     - Đặt danh sách đã xử lý `ar` trở lại `f` của `i`.
   - Nếu `v` là một constant str (`ast.Constant` với `v.value` là một chuỗi), gọi `obfstr(v.value)` và đặt lại `f` của `i`.
   - Nếu `v` là một constant int (`ast.Constant` với `v.value` là một số nguyên), `gọi obfint(v.value)` và đặt lại `f` của `i`.

Bạn đã hiểu về hàm này rồi thì chúng ta sẽ tới phần làm đẹp cho cái obf của mình , yes , là làm đẹp bởi vì bạn nhìn đống lambda kia thực sự vô hồn , mình hãy thêm tí vị cho nó bằng cách thay đổi hàm `obfint` và `obfstr` 
Mình sẽ thêm hán tự cho nó nhé
Ví dụ
```python 
import ast


randomchar = ''.join(__import__('random').choices([chr(i) for i in range(0x4e00, 0x9fff)], k=4))

def obfstr(v):
    return f'(lambda {randomchar} : "{v}")("{randomchar}")' 

def obfint(v):
    return f"int('{v}')"
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
                    elif isinstance(j, ast.AST):
                        ar.append(j)
                setattr(i, f, ar)
            elif isinstance(v, ast.Constant) and isinstance(v.value, str):
                setattr(i, f, ast.parse(obfstr(v.value)).body[0].value)
            elif isinstance(v, ast.Constant) and isinstance(v.value, int):
                setattr(i, f, ast.parse(obfint(v.value)).body[0].value)
                
def obf(src):
    tree = ast.parse(src)
    obfuscate(tree)
    return ast.unparse(tree)

code = """
print(1000)
print("ngocuyen")
"""

for i in range(3):
    code = obf(code)
print(code)

```
Kết quả :
```python
print(int((lambda 駹穯污揭: (lambda 駹穯污揭: '1000')('駹穯污揭'))((lambda 駹穯污揭: '駹穯污揭')('駹穯污揭'))))
print((lambda 駹穯污揭: (lambda 駹穯污揭: (lambda 駹穯污揭: 'ngocuyen')('駹穯污揭'))((lambda 駹穯污揭: '駹穯污揭')('駹穯污揭')))((lambda 駹穯污揭: (lambda 駹穯污揭: '駹穯污揭')('駹穯污揭'))((lambda 駹穯污揭: '駹穯污揭')('駹穯污揭'))))
```

Cũng có thể mix hàm obfstr thành như này 
```python
def obfstr(v):
    tachstring = '+'.join([f'"{c}"' for c in v])
    return f'(lambda {randomchar} : {tachstring})("{randomchar}")'
```
NOTES : cho vòng lặp càng nhiều thì lambda càng nhiều
Kết quả :
```python
print(int((lambda 骑嫚璹敇: (lambda 骑嫚璹敇: '1')('骑嫚璹敇') + (lambda 骑嫚璹敇: '0')('骑嫚璹敇') + (lambda 骑嫚璹敇: '0')('骑嫚璹敇') + (lambda 骑嫚璹敇: '0')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇'))))
print((lambda 骑嫚璹敇: (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'n')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'g')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'o')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'c')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'u')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'y')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'e')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')) + (lambda 骑嫚璹敇: (lambda 骑嫚璹敇: 'n')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇')))((lambda 骑嫚璹敇: (lambda 骑嫚璹敇: '骑')('骑嫚璹敇') + (lambda 骑嫚璹敇: '嫚')('骑嫚璹敇') + (lambda 骑嫚璹敇: '璹')('骑嫚璹敇') + (lambda 骑嫚璹敇: '敇')('骑嫚璹敇'))((lambda 骑嫚璹敇: '骑' + '嫚' + '璹' + '敇')('骑嫚璹敇'))))
```
Hoặc có thể làm cho nó tây tí là
```python

randomchar = "_0x"+''.join(__import__('random').choices([str(i) for i in range(1, 10)], k=4))

```

Kết quả :
```python
print(int((lambda _0x3327: (lambda _0x3327: '1')('_0x3327') + (lambda _0x3327: '0')('_0x3327') + (lambda _0x3327: '0')('_0x3327') + (lambda _0x3327: '0')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327'))))
print((lambda _0x3327: (lambda _0x3327: (lambda _0x3327: 'n')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'g')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'o')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'c')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'u')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'y')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'e')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')) + (lambda _0x3327: (lambda _0x3327: 'n')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327')))((lambda _0x3327: (lambda _0x3327: '_')('_0x3327') + (lambda _0x3327: '0')('_0x3327') + (lambda _0x3327: 'x')('_0x3327') + (lambda _0x3327: '3')('_0x3327') + (lambda _0x3327: '3')('_0x3327') + (lambda _0x3327: '2')('_0x3327') + (lambda _0x3327: '7')('_0x3327'))((lambda _0x3327: '_' + '0' + 'x' + '3' + '3' + '2' + '7')('_0x3327'))))
```

Nhưng có một vấn đề bất cập đó chính là với f string
```python
hello = 5
print(f"{hello}")
```
Kết quả
```python
a = int((lambda _0x1788: (lambda _0x1788: '5')('_0x1788'))((lambda _0x1788: '_' + '0' + 'x' + '1' + '7' + '8' + '8')('_0x1788')))
print(f'{a}')
```
Nhưng mình nghĩ như này không thỏa mãn lắm , Vậy nên mình đã tìm hiểu về ast.JoinedStr
và write một hàm để biến f string thành .format để cho việc obf string trở lên thuận tiện hơn
```py
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
```
Cập nhật lại code chúng ta có
Và tiện thể fix bug với `\n và \r escape` và [True] [False] thì skip va bug với cả "" (Rỗng)
```py
import ast

randomchar = "_0x" + ''.join(__import__('random').choices([str(i) for i in range(1, 10)], k=4))

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
def obf(src):
    tree = ast.parse(src)
    obfuscate(tree)
    return ast.unparse(tree)
code = r"""
a = 5
print(f"{a}")
print("\n")
print([True])
print([False])
def a():return True
    
"""

for i in range(3):
    code = obf(code)
print(code)
```
Và kết quả là 
```py
a = int((lambda _0x8292: (lambda _0x8292: '5')('_0x8292'))((lambda _0x8292: '_' + '0' + 'x' + '8' + '2' + '9' + '2')('_0x8292')))
print((lambda _0x8292: (lambda _0x8292: '{')('_0x8292') + (lambda _0x8292: '}')('_0x8292'))((lambda _0x8292: '_' + '0' + 'x' + '8' + '2' + '9' + '2')('_0x8292')).format(a))
print((lambda _0x1744: (lambda _0x1744: (lambda _0x1744: '\n')('_0x1744'))((lambda _0x1744: '_' + '0' + 'x' + '1' + '7' + '4' + '4')('_0x1744')))((lambda _0x1744: (lambda _0x1744: '_')('_0x1744') + (lambda _0x1744: '0')('_0x1744') + (lambda _0x1744: 'x')('_0x1744') + (lambda _0x1744: '1')('_0x1744') + (lambda _0x1744: '7')('_0x1744') + (lambda _0x1744: '4')('_0x1744') + (lambda _0x1744: '4')('_0x1744'))((lambda _0x1744: '_' + '0' + 'x' + '1' + '7' + '4' + '4')('_0x1744'))))
print([True])
print([False])
def a():
    return True
```



Bạn thấy đây trông nó đã thỏa mãn hơn rồi vậy là chúng ta đã làm xong obf cho string , nó chỉ có vậy thôi
Tiếp theo là OBF Try-Catch
```py

print("hello world")
def hello(x):
	x = 5
	print(x)
hello(10)
```
Thành 
```py
try:
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                raise MemoryError('Ngocuyencoder')
            except MemoryError:
                print('hello world')
try:
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                raise MemoryError('Ngocuyencoder')
            except MemoryError:

                def hello(x):
                    x = 5
                    print(x)
try:
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                raise MemoryError('Ngocuyencoder')
            except MemoryError:
                hello(10)
```

                    

CODE : 
```py
import ast

def trycatch(body, loop):
    ar = []
    for x in body:
        j = x
        for _ in range(loop):
            j = ast.Try(
                body=[],
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
    tbd = trycatch(tree.body, loop)
    def ast_to_code(node):
        return ast.unparse(node)
    j = ast_to_code(tbd)
    return j

loop = 4

# Original code
code = """

print("hello world")
def hello(x):
    x = 5
    print(x)
hello(10)
"""

j = obf(code, loop)
print(j)
```

**`ast.Try`**:
   - `ast.Try(...)` tạo ra một node AST đại diện cho khối `try-except`:
     - `body=[]`: Tạo phần thân của khối này, chúng ta có thể mix nó thêm sau
     - `handlers=[ast.ExceptHandler(...)]`: Chúng ta định nghĩa Exception:
       - `type=ast.Name(id='MemoryError', ctx=ast.Load())`: Thêm `MemoryError`.
       - `name=None` Có thể thay bằng cái bạn thích ví dụ là `name="NgocUYENCUTEVL` sẽ là `MemoryError` as `NgocUYENCUTEVL`
       - `body=[j]`: Thực thi câu lệnh ban đầu trong khối `except`.
     - `orelse=[]`: Để trống vì mình không thêm else 
     - `finalbody=[]`: Để trống vì mình không thêm finally

**Thêm `raise`**:
   - `j.body.append(ast.Raise(...))` thêm một câu lệnh `raise` vào trong `except`:
     - `exc=ast.Call(...)`: Gọi để call `MemoryError`.
     - `args=[ast.Str(s="Ngocuyencoder")]`: Cung cấp một string tùy chỉnh `"Ngocuyencoder"` khi call `MemoryError`.
     - `cause=NONE`:  kiểu như raise Exception from {cause} đó thường thì là from None  

Cái try catch như trên vừa dễ làm vừa ít bug vả lại còn khá là hiệu quả, nhưng mình thấy thế là chưa đủ nên chúng ta hãy đi tiếp phần if else bằng cách code thêm một function mới
```py
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
```




sửa lại def trycatch thành
```py
def trycatch(body, loop):
    ar = [random_if_else()] # Được Rồi giờ chúng ta đã có thuộc tính
    for x in body:
        j = x
        for _ in range(loop):
            j = ast.Try(
                body=[],
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
```
Dưới đây là giải thích  về đoạn mã đã cho:

**AST If Node:**
   - `ast.If` đại diện cho một câu lệnh `if` trong Abstract Syntax Tree (AST).
   - Nó cần ba đối số: `test`, `body`, và `orelse`.

**Điều kiện kiểm tra (test condition):**
   - Đối số `test` là một đối tượng `ast.Compare`, đại diện cho một phép so sánh.
   - `ast.Compare` cần ba đối số: `left`, `ops`, và `comparators`.

**Toán hạng bên trái (left operand):**
   - `left` là một đối tượng `ast.Constant` với giá trị `False`.
   - Điều này đại diện cho phía bên trái của phép so sánh, là hằng số `False`.

**Tạo toán tử so sánh**
   - `ops` là một danh sách chứa một đối tượng `ast.Lt()`.
   - `ast.Lt()` đại diện cho toán tử bằng (`<`).
Các toán tử trong ast
1. `Eq` (==)
2. `NotEq` (!=)
3. `Lt` (<)
4. `LtE` (<=)
5. `Gt` (>)
6. `GtE` (>=)
7. `Is` (is)
8. `IsNot` (is not)
9. `In` (in)
10. `NotIn` (not in)



7. **Toán hạng bên phải (right operand):**
   - `comparators` là một danh sách chứa một đối tượng `ast.Constant` với giá trị `True`.
   - Điều này đại diện cho phía bên phải của phép so sánh, là hằng số `True`.

8. **Thân if (body):**
   - `body` là một danh sách chứa một đối tượng `ast.Pass()`.
   - `ast.Pass` đại diện cho lệnh `pass` trong Python, có nghĩa là không làm gì cả.

9. **Thân else (orelse):**
   - `orelse` là một danh sách chứa một đối tượng `ast.Pass()`.
   - Tương tự như trên, điều này đại diện cho lệnh `pass` trong nhánh `else`.

Bây giờ hãy sử dụng nó nào
Kết quả :
```py
print("hello world")
def hello(x):
    x = 5
    print(x)
hello(10)
```
Thành
```py
try:
    if False is True:
        pass
    else:
        pass
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        if False is True:
            pass
        else:
            pass
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            if False is True:
                pass
            else:
                pass
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                if False is True:
                    pass
                else:
                    pass
                raise MemoryError('Ngocuyencoder')
            except MemoryError:
                print('hello world')
try:
    if False is True:
        pass
    else:
        pass
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        if False is True:
            pass
        else:
            pass
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            if False is True:
                pass
            else:
                pass
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                if False is True:
                    pass
                else:
                    pass
                raise MemoryError('Ngocuyencoder')
            except MemoryError:

                def hello(x):
                    x = 5
                    print(x)
try:
    if False is True:
        pass
    else:
        pass
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        if False is True:
            pass
        else:
            pass
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            if False is True:
                pass
            else:
                pass
            raise MemoryError('Ngocuyencoder')
        except MemoryError:
            try:
                if False is True:
                    pass
                else:
                    pass
                raise MemoryError('Ngocuyencoder')
            except MemoryError:
                hello(10)
```


Chúng ta đã hoàn thành được 3 chức năng 
- OBF STRING
- OBF TRY CATCH
- OBF IF ELSE

Và dưới đây là code sau khi gộp lại
Vậy là bước đầu thành công trên con đường obf rồi đó
```py
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
print(code)
```
Kết quả
```py
try:
    if False is True:
        pass
    else:
        pass
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        if False is True:
            pass
        else:
            pass
        raise MemoryError('Ngocuyencoder')
    except MemoryError:
        try:
            if False is True:
                pass
            else:
                pass
            raise MemoryError((lambda _0x1452: 'N' + 'g' + 'o' + 'c' + 'u' + 'y' + 'e' + 'n' + 'c' + 'o' + 'd' + 'e' + 'r')('_0x1452'))
        except MemoryError:
            try:
                if False is True:
                    pass
                else:
                    pass
                raise MemoryError((lambda _0x1452: 'N' + 'g' + 'o' + 'c' + 'u' + 'y' + 'e' + 'n' + 'c' + 'o' + 'd' + 'e' + 'r')('_0x1452'))
            except MemoryError:
                try:
                    if False is True:
                        pass
                    else:
                        pass
                    raise MemoryError((lambda _0x1452: (lambda _0x1452: 'N')('_0x1452') + (lambda _0x1452: 'g')('_0x1452') + (lambda _0x1452: 'o')('_0x1452') + (lambda _0x1452: 'c')('_0x1452') + (lambda _0x1452: 'u')('_0x1452') + (lambda _0x1452: 'y')('_0x1452') + (lambda _0x1452: 'e')('_0x1452') + (lambda _0x1452: 'n')('_0x1452') + (lambda _0x1452: 'c')('_0x1452') + (lambda _0x1452: 'o')('_0x1452') + (lambda _0x1452: 'd')('_0x1452') + (lambda _0x1452: 'e')('_0x1452') + (lambda _0x1452: 'r')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))
                except MemoryError:
                    try:
                        if False is True:
                            pass
                        else:
                            pass
                        raise MemoryError((lambda _0x1452: (lambda _0x1452: 'N')('_0x1452') + (lambda _0x1452: 'g')('_0x1452') + (lambda _0x1452: 'o')('_0x1452') + (lambda _0x1452: 'c')('_0x1452') + (lambda _0x1452: 'u')('_0x1452') + (lambda _0x1452: 'y')('_0x1452') + (lambda _0x1452: 'e')('_0x1452') + (lambda _0x1452: 'n')('_0x1452') + (lambda _0x1452: 'c')('_0x1452') + (lambda _0x1452: 'o')('_0x1452') + (lambda _0x1452: 'd')('_0x1452') + (lambda _0x1452: 'e')('_0x1452') + (lambda _0x1452: 'r')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))
                    except MemoryError:
                        try:
                            if False is True:
                                pass
                            else:
                                pass
                            raise MemoryError((lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'N')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'g')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'c')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'u')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'y')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'e')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'n')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'c')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'd')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'e')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'r')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))))
                        except MemoryError:
                            try:
                                if False is True:
                                    pass
                                else:
                                    pass
                                raise MemoryError((lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'N')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'g')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'c')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'u')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'y')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'e')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'n')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'c')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'd')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'e')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'r')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))))
                            except MemoryError:
                                print((lambda _0x1452: (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'h')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'e')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'l')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'l')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: ' ')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'w')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'o')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'r')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'l')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))) + (lambda _0x1452: (lambda _0x1452: (lambda _0x1452: 'd')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452'))))((lambda _0x1452: (lambda _0x1452: (lambda _0x1452: '_')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: '0')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: 'x')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: '1')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: '4')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: '5')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')) + (lambda _0x1452: (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))((lambda _0x1452: (lambda _0x1452: '_')('_0x1452') + (lambda _0x1452: '0')('_0x1452') + (lambda _0x1452: 'x')('_0x1452') + (lambda _0x1452: '1')('_0x1452') + (lambda _0x1452: '4')('_0x1452') + (lambda _0x1452: '5')('_0x1452') + (lambda _0x1452: '2')('_0x1452'))((lambda _0x1452: '_' + '0' + 'x' + '1' + '4' + '5' + '2')('_0x1452')))))
```

Thật tuyệt vời phải không ạ? Không quá khó mà lại rất mạnh, thời gian debug còn lâu hơn thời gian write nữa :)

## TƯ DUY VỀ OBF ,DEOBF
Đây là cái phần cần động não cực kì, bởi lẽ nếu không có thì việc làm obf cũng hơi cực 
Như ở phần builtins function thì mình đã giới thiệu qua về cơ thế hooking, tức là mọi hàm builtins đều bị hook cả
Thông thường thì sẽ làm một cái anti để check xem có hàm nào đấy bị rewrite không thì sẽ block
Ví dụ về exec
```py
type(exec) = <class 'builtin_function_or_method'>
```
nếu như mình rewrite cái hàm này thì cái type của nó sẽ bị thay đổi
```
c = exec
def h(x):
    v = c(x)
    print(x)
    return v
exec = h

```
bây giờ `print(type(exec)`
thì nó ra `<class 'function'>`

như vậy chúng ta tạo được một cái anti đầu tiên
```py
if str(type(exec)) != "<class 'builtin_function_or_method'>":
    raise MemoryError("Phát hiện hook")
```
về raise thì chúng ta không thể bypass được vì nó là keyword, chúng ta phải làm sao cho cái anti khi check thì nó không ra được 
với code trên thì bypass cực kì dễ
```py
c = exec
def h(x):
    v = c(x)
    print(x)
    return v
exec = h

def type(x):
        return "<class 'builtin_function_or_method'>"


if str(type(exec)) != "<class 'builtin_function_or_method'>":
    raise MemoryError("Detect hook")
```
>>> 5
```py
c = exec
def h(x):
    v = c(x)
    print(x)
    return v
exec = h

if str(type(exec)) != "<class 'builtin_function_or_method'>":
    raise MemoryError("Detect hook")
exec("print(5)")
```
>>> MemoryError: Detect hook

Tới đây rồi thì bạn có nghĩ là chỉ việc xóa cái chỗ anti đi là được đúng không? , không , không đơn giản như vậy vì thường anti sẽ được nhét vào trong marshal và chúng ta phải bắt buộc phải đọc dis 
```py
  0           0 RESUME                   0

  1           2 LOAD_NAME                0 (exec)
              4 STORE_NAME               1 (c)

  2           6 LOAD_CONST               0 (<code object h at 0x0000026214A1AE30, file "v", line 2>)
              8 MAKE_FUNCTION            0
             10 STORE_NAME               2 (h)

  6          12 LOAD_NAME                2 (h)
             14 STORE_NAME               0 (exec)

 12          16 PUSH_NULL
             18 LOAD_NAME                3 (str)
             20 PUSH_NULL
             22 LOAD_NAME                4 (type)
             24 LOAD_NAME                0 (exec)
             26 PRECALL                  1
             30 CALL                     1
             40 PRECALL                  1
             44 CALL                     1
             54 LOAD_CONST               1 ("<class 'builtin_function_or_method'>")
             56 COMPARE_OP               3 (!=)
             62 POP_JUMP_FORWARD_IF_FALSE    11 (to 86)

 13          64 PUSH_NULL
             66 LOAD_NAME                5 (MemoryError)
             68 LOAD_CONST               2 ('Detect hook')
             70 PRECALL                  1
             74 CALL                     1
             84 RAISE_VARARGS            1

 15     >>   86 PUSH_NULL
             88 LOAD_NAME                0 (exec)
             90 PUSH_NULL
             92 LOAD_NAME                6 (print)
             94 LOAD_CONST               3 (5)
             96 PRECALL                  1
            100 CALL                     1
            110 PRECALL                  1
            114 CALL                     1
            124 POP_TOP
            126 LOAD_CONST               4 (None)
            128 RETURN_VALUE

Disassembly of <code object h at 0x0000026214A1AE30, file "v", line 2>:
  2           0 RESUME                   0

  3           2 LOAD_GLOBAL              1 (NULL + c)
             14 LOAD_FAST                0 (x)
             16 PRECALL                  1
             20 CALL                     1
             30 STORE_FAST               1 (v)

  4          32 LOAD_GLOBAL              3 (NULL + print)
             44 LOAD_FAST                0 (x)
             46 PRECALL                  1
             50 CALL                     1
             60 POP_TOP

  5          62 LOAD_FAST                1 (v)
             64 RETURN_VALUE
```

Với pyc thì chúng ta không thể edit trực tiếp mà phải qua các công cụ decompile như `pycdc` nah dù họ lười fix bug thật sự và thiếu nhiều opcode (hứa hẹn tương lai mình sẽ write một cái pyc decompile và share lên) đó là lý tại sao sinh ra code bypass để nhắm tới một hàm builtins nào đó trong python
Bây giờ
Mình sẽ thử deobf code này chỉ bằng cách hooking exec
```py
__builtins__.__dict__[''.join(["c","e","x","e"][::-1])](")'olleh'(tnirp"[::-1])
```
>>> hello

mình đã thực hiện che giấu đi exec bằng string rồi nhé và đảo ngược cả chuỗi nhưng chúng ta phải hiểu là nó gọi hàm exec thì
```py
c = exec
def h(x):
    print(x)
    v = c(x)
    return v
exec = h
__import__("builtins").exec = h
__builtins__.__dict__[''.join(["c","e","x","e"][::-1])](")'olleh'(tnirp"[::-1])
```

>>> "print('hello')"

Đó là top 1 các lý do bạn không dùng obf có exec hoặc eval (trừ khi đó là marshal bởi vì nó là bytecode)

Mình sẽ không đi quá sâu vào anti vì đơn giản là nó rất mệt , căn bản thì cái nào cũng bypass được nếu đúng điều kiện
Mình sẽ chỉ share những cái kết hợp để nốc out đối thủ 
Raise
```py
if <điều kiện> == False : raise MemoryError ("Đòi Hook à")
```
Hoặc Tràn ram (cực kì khốn nạn)
```py
if <điều kiện> == False : deptrai = [[0]*10**9]
```
Chỉ cần bạn biết cách check thôi là khiến đối thủ khó chịu rồi

Bây giờ là phần cách tạo ra một cái obf mà khiến người khác nản và rất lười để deobf lại
Đó chính là kết hợp ast và marshal lại

Hãy xem đây là khi kết hợp và kết quả cho ra dis của nó
```py
source = """
try:
    if False is True:
        pass
    else:
        pass
    raise MemoryError('Ngocuyencoder')
except MemoryError:
    try:
        if False is True:
            pass
        else:
            pass
        raise MemoryError((lambda _0x7359: 'N' + 'g' + 'o' + 'c' + 'u' + 'y' + 'e' + 'n' + 'c' + 'o' + 'd' + 'e' + 'r')('_0x7359'))
    except MemoryError:
        print((lambda _0x7359: (lambda _0x7359: 'h')('_0x7359') + (lambda _0x7359: 'e')('_0x7359') + (lambda _0x7359: 'l')('_0x7359') + (lambda _0x7359: 'l')('_0x7359') + (lambda _0x7359: 'o')('_0x7359') + (lambda _0x7359: ' ')('_0x7359') + (lambda _0x7359: 'w')('_0x7359') + (lambda _0x7359: 'o')('_0x7359') + (lambda _0x7359: 'r')('_0x7359') + (lambda _0x7359: 'l')('_0x7359') + (lambda _0x7359: 'd')('_0x7359'))((lambda _0x7359: '_' + '0' + 'x' + '7' + '3' + '5' + '9')('_0x7359')))
"""
import marshal
x = marshal.dumps(compile(source,"ngocuyen.py","exec")
```
>>> b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\xf3\xc8\x00\x00\x00\x97\x00\t\x00d\x0.....

sau khi dis nó ra thì 
```py
  0           0 RESUME                   0

  2           2 NOP

  3           4 LOAD_CONST               0 (False)
              6 LOAD_CONST               1 (True)
              8 IS_OP                    0
             10 POP_JUMP_FORWARD_IF_FALSE     1 (to 14)

  4          12 JUMP_FORWARD             1 (to 16)

  6     >>   14 NOP

  7     >>   16 PUSH_NULL
             18 LOAD_NAME                0 (MemoryError)
             20 LOAD_CONST               2 ('Ngocuyencoder')
             22 PRECALL                  1
             26 CALL                     1
             36 RAISE_VARARGS            1
        >>   38 PUSH_EXC_INFO

  8          40 LOAD_NAME                0 (MemoryError)
             42 CHECK_EXC_MATCH
             44 POP_JUMP_FORWARD_IF_FALSE    73 (to 192)
             46 POP_TOP

  9          48 NOP

 10          50 LOAD_CONST               0 (False)
             52 LOAD_CONST               1 (True)
             54 IS_OP                    0
             56 POP_JUMP_FORWARD_IF_FALSE     1 (to 60)

 11          58 JUMP_FORWARD             1 (to 62)

 13     >>   60 NOP

 14     >>   62 PUSH_NULL
             64 LOAD_NAME                0 (MemoryError)
             66 PUSH_NULL
             68 LOAD_CONST               3 (<code object <lambda> at 0x0000021F751B16B0, file "ngocuyen.py", line 14>)
             70 MAKE_FUNCTION            0
             72 LOAD_CONST               4 ('_0x7359')
             74 PRECALL                  1
             78 CALL                     1
             88 PRECALL                  1
             92 CALL                     1
            102 RAISE_VARARGS            1
        >>  104 PUSH_EXC_INFO

 15         106 LOAD_NAME                0 (MemoryError)
            108 CHECK_EXC_MATCH
            110 POP_JUMP_FORWARD_IF_FALSE    36 (to 184)
            112 POP_TOP

 16         114 PUSH_NULL
            116 LOAD_NAME                1 (print)
            118 PUSH_NULL
            120 LOAD_CONST               5 (<code object <lambda> at 0x0000021F74C432D0, file "ngocuyen.py", line 16>)
            122 MAKE_FUNCTION            0
            124 PUSH_NULL
            126 LOAD_CONST               6 (<code object <lambda> at 0x0000021F751B1FB0, file "ngocuyen.py", line 16>)
            128 MAKE_FUNCTION            0
            130 LOAD_CONST               4 ('_0x7359')
            132 PRECALL                  1
            136 CALL                     1
            146 PRECALL                  1
            150 CALL                     1
            160 PRECALL                  1
            164 CALL                     1
            174 POP_TOP
            176 POP_EXCEPT
            178 POP_EXCEPT
            180 LOAD_CONST               7 (None)
            182 RETURN_VALUE

 15     >>  184 RERAISE                  0
        >>  186 COPY                     3
            188 POP_EXCEPT
            190 RERAISE                  1

  8     >>  192 RERAISE                  0
        >>  194 COPY                     3
            196 POP_EXCEPT
            198 RERAISE                  1
ExceptionTable:
  4 to 36 -> 38 [0]
  38 to 46 -> 194 [1] lasti
  50 to 102 -> 104 [1]
  104 to 174 -> 186 [2] lasti
  176 to 176 -> 194 [1] lasti
  184 to 184 -> 186 [2] lasti
  186 to 192 -> 194 [1] lasti

Disassembly of <code object <lambda> at 0x0000021F751B16B0, file "ngocuyen.py", line 14>:
 14           0 RESUME                   0
              2 LOAD_CONST               1 ('Ngocuyencoder')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F74C432D0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 PUSH_NULL
              4 LOAD_CONST               1 (<code object <lambda> at 0x0000021F751B1770, file "ngocuyen.py", line 16>)
              6 MAKE_FUNCTION            0
              8 LOAD_CONST               2 ('_0x7359')
             10 PRECALL                  1
             14 CALL                     1
             24 PUSH_NULL
             26 LOAD_CONST               3 (<code object <lambda> at 0x0000021F751B1830, file "ngocuyen.py", line 16>)
             28 MAKE_FUNCTION            0
             30 LOAD_CONST               2 ('_0x7359')
             32 PRECALL                  1
             36 CALL                     1
             46 BINARY_OP                0 (+)
             50 PUSH_NULL
             52 LOAD_CONST               4 (<code object <lambda> at 0x0000021F751B18F0, file "ngocuyen.py", line 16>)
             54 MAKE_FUNCTION            0
             56 LOAD_CONST               2 ('_0x7359')
             58 PRECALL                  1
             62 CALL                     1
             72 BINARY_OP                0 (+)
             76 PUSH_NULL
             78 LOAD_CONST               5 (<code object <lambda> at 0x0000021F751B19B0, file "ngocuyen.py", line 16>)
             80 MAKE_FUNCTION            0
             82 LOAD_CONST               2 ('_0x7359')
             84 PRECALL                  1
             88 CALL                     1
             98 BINARY_OP                0 (+)
            102 PUSH_NULL
            104 LOAD_CONST               6 (<code object <lambda> at 0x0000021F751B1A70, file "ngocuyen.py", line 16>)
            106 MAKE_FUNCTION            0
            108 LOAD_CONST               2 ('_0x7359')
            110 PRECALL                  1
            114 CALL                     1
            124 BINARY_OP                0 (+)
            128 PUSH_NULL
            130 LOAD_CONST               7 (<code object <lambda> at 0x0000021F751B1B30, file "ngocuyen.py", line 16>)
            132 MAKE_FUNCTION            0
            134 LOAD_CONST               2 ('_0x7359')
            136 PRECALL                  1
            140 CALL                     1
            150 BINARY_OP                0 (+)
            154 PUSH_NULL
            156 LOAD_CONST               8 (<code object <lambda> at 0x0000021F751B1BF0, file "ngocuyen.py", line 16>)
            158 MAKE_FUNCTION            0
            160 LOAD_CONST               2 ('_0x7359')
            162 PRECALL                  1
            166 CALL                     1
            176 BINARY_OP                0 (+)
            180 PUSH_NULL
            182 LOAD_CONST               9 (<code object <lambda> at 0x0000021F751B1CB0, file "ngocuyen.py", line 16>)
            184 MAKE_FUNCTION            0
            186 LOAD_CONST               2 ('_0x7359')
            188 PRECALL                  1
            192 CALL                     1
            202 BINARY_OP                0 (+)
            206 PUSH_NULL
            208 LOAD_CONST              10 (<code object <lambda> at 0x0000021F751B1D70, file "ngocuyen.py", line 16>)
            210 MAKE_FUNCTION            0
            212 LOAD_CONST               2 ('_0x7359')
            214 PRECALL                  1
            218 CALL                     1
            228 BINARY_OP                0 (+)
            232 PUSH_NULL
            234 LOAD_CONST              11 (<code object <lambda> at 0x0000021F751B1E30, file "ngocuyen.py", line 16>)
            236 MAKE_FUNCTION            0
            238 LOAD_CONST               2 ('_0x7359')
            240 PRECALL                  1
            244 CALL                     1
            254 BINARY_OP                0 (+)
            258 PUSH_NULL
            260 LOAD_CONST              12 (<code object <lambda> at 0x0000021F751B1EF0, file "ngocuyen.py", line 16>)
            262 MAKE_FUNCTION            0
            264 LOAD_CONST               2 ('_0x7359')
            266 PRECALL                  1
            270 CALL                     1
            280 BINARY_OP                0 (+)
            284 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1770, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('h')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1830, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('e')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B18F0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('l')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B19B0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('l')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1A70, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('o')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1B30, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 (' ')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1BF0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('w')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1CB0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('o')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1D70, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('r')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1E30, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('l')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1EF0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('d')
              4 RETURN_VALUE

Disassembly of <code object <lambda> at 0x0000021F751B1FB0, file "ngocuyen.py", line 16>:
 16           0 RESUME                   0
              2 LOAD_CONST               1 ('_0x7359')
              4 RETURN_VALUE
```
Yes đây chính xác là những gì đối thủ của bạn cần dịch ngược lại về, cảm giác vừa phải dịch đống bytecode lại còn phải syntax lại :)
Vẫn có thể lấy được source của các hàm bằng hook nhưng còn keyword thì chắc chắn phải decompile pyc ra mới được

Đó là lý do tại sao ở Việt Nam đa số khi làm obf (không tính convert sang exe elf vân vân) thì sẽ sử dụng cách này vì nó thông dụng , dễ làm dễ trúng thưởng , dần dần thì các công cụ decompile pyc lại lỗi nên là vẫn được áp dụng nhiều (kể cả mình)

PART NÀY VẪN CÒN NHÉ CÁC BÁC EM BỔ SUNG SAU  GIỜ LƯỜI QUÁ + )))

# HÀNH TRÌNH 
Học cái này ở đâu thì nó là nhân duyên đời mình rồi
Mình bắt đầu tham gia vào mảng này vào tháng 7 2023
Cũng không hiểu tại sao mà lại thích tới vậy , chỉ là nhìn mấy cái obf nó rất đẹp kiểu xáo trộn tùm lum trông hay
Mình đã lên github và mò dần dần , quãng thời gian đi bú code
Chỉ trong 2 ngày mà đào hết sạch 50 tabs github để mix các obf lại với nhau (Mình vẫn nhớ tên được hết nếu nó được up lên github)
Từ đấy mình bắt đầu đâm đầu vào mix , chế các kiểu nó thành đam mê rồi
Câu hỏi đặt ra là làm sao để test được độ mạnh của obf thì chân thành gửi lời cảm ơn tới KhanhNguyen9872 với 2 repo:
> https://github.com/KhanhNguyen9872/kramer-specter_deobf
> https://github.com/KhanhNguyen9872/dump_marshal_py
Trong đây có cái gì thì nó là tool để deobf , nah rất hữu dụng để test mọi loại obf (trừ ast)
Sau khi mình làm đi làm lại gần 2 tháng với số lần sử dụng 2 tool này thì mình đã nhận ra một cách làm khó đối thủ bằng spam và compile marshal
Cách thực hiện thì đơn giản thôi
Cứ spam tất cả những gì có trong bộ não của bạn rồi compile lại là tự dưng người khác lười, thực sự lười để deobf ra vì nhìn đống dis toàn ...
2 tháng sau tới tháng 11 thì mình vẫn tiếp tục spam nhưng rồi nghĩ lại không hợp lí tí nào cả , cứ spam như vậy thì tới bao giờ mới làm ra hồn được một cái obf 
Cái tự dưng mình vào được nhóm của tây lông khi lang thang trên github và chỉ 1 tháng sau mình đã claim được kiến thức về

> Hooking
> Bytecode (VM)
> Ast Work

Tức là từ trước là bản thân chỉ là thằng bú code thôi , về sau mới được thông não và trở thành như bây giờ
Cảm ơn mấy anh tây mà mình mất discord rồi không tìm được mấy ảnh nữa 


Có nhiều thứ giác ngộ , mình bắt đầu phá đảo python bằng hook =)))))))
Vầng ấy ạ là khai thác hàm , Mình hook input của thằng khác và thay tên thành tên của mình mà không cần decode ra , trò này cực kì vui
Thì bắt đầu mình đi làm quen và làm quen được bạn và sau này đã build project Velimatix với mình tên Minh Nguyễn

Mình bắt đầu chia sẻ cho bạn ấy về kiến thức của mình (nhiều lắm đó) và bắt đầu bọn mình hợp tác làm obf với nhau

Lúc đầu là bạn ấy làm anti và mình sẽ là người bypass để kiểm tra tính bảo mật

Về sau này mình lười quá đâm ra mình cho riêng bạn ấy làm tầm 1 tháng gì đó tại mình cũng lười 

Thời gian trôi qua 3,4 tháng của đầu năm 2024 thì mình chả làm gì cả, tức là 3,4 tháng đó mình ngồi chơi

và 2 tháng 5 , 6 quay trở lại đây là mình với bạn Minh Nguyễn khởi động lại làm obf với nhau

Bọn mình chia nhau ra là 
Mình sẽ ra mấy cái ý tưởng độc lạ cho obf nó hay hơn (đưa cách làm)
Minh Nguyễn sẽ là người thực hiện những ý tưởng đó

Hai thằng bù đắp cho nhau để đi lên cùng nhau

Nah chỉ vậy thôi , hành trình 1 năm tóm tắt trong 50 dòng , Thank u vì đã đọc docs này nha



