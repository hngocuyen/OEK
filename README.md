# ngocuyencoder 19/07/2008
## OEK - OBFUSCATION ENGINEERING KNOWLEDGE


Xin chào tất cả mọi người tôi là ngocuyencoder
Hôm trước tôi đã share về project outsource Velimatix
Bây giờ là tới phần chia sẻ kiến thức (tất cả mọi kiến thức của tôi về mảng này)
Vốn dĩ ở Việt Nam ít ai chia sẻ kiến thức của bản thân về cái chủ đề này cả (Cảm giác như khá là nhạy cảm)


Đầu tiên là bước khởi đầu cho một xáo trộn cơ bản , khá là dễ khi bạn làm và sử dụng , dễ fix bug nhưng tính bảo mật thì ...
> code = "print('hello world')"
> code = code.encode("utf8")
=> b"print('hello world')"

Cái raw đầu tiên cơ bản
Giờ thì chỉ việc thêm exec vào
> exec(b"print('hello world')")
> hello world

Bên trên đây chính là cái raw cơ bản nhất, dễ hiểu nhất , chung quy là sử dụng exec để thực thi


Tiếp theo chúng ta có thể mix với các thư viện như base64 , zlib
> import base64,zlib
> code = "print('hello world')"

Bug cơ bản nếu như bạn làm như này
> base64.b64encode(code) : TypeError: a bytes-like object is required, not 'str'

Cách khắc phục là 
> base64.b64encode(code.encode("utf8")) : b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='

Bây giờ chúng ta đã có một cái base64 để xáo trộn mã lên, Dùng __import__ để đẩy nhanh quá trình import thư viện
> exec(__import__("base64").b64decode(b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='))
=> hello world

Vậy thì câu hỏi bây giờ là giải mã nó như nào ? 
Giải base64 ra ư?
Câu trả lời là NO, cũng được nhưng không hiểu quả
Vì vốn dĩ nó gọi b64decode rồi tới exec thì chúng ta chỉ cần thay thế exec = print là được

> print(__import__("base64").b64decode(b'cHJpbnQoJ2hlbGxvIHdvcmxkJyk='))
>>> b"print('hello world')" Khi này nó ở dạng bytes thì tôi sẽ chuyển nó về dạng thường
>>> b"print('hello world')".decode()
=> "print('hello world')"


Bây giờ tôi sẽ mix thêm zlib và cả base64 và bz2

> import base64,bz2,zlib
> code = "print('ngocuyen')"
> code = zlib.compress(bz2.compress(base64.b64encode(code.encode("utf8"))))
>>> b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'

Bây giờ đã có một dãy byte nén cực ảo diệu tôi sẽ làm phần dịch ngược cho nó chạy được

>>> exec(__import__("base64").b64decode(__import__("bz2").decompress(__import__("zlib").decompress(b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'))))
=> ngocuyen

Thay exec = print

>>> print(__import__("base64").b64decode(__import__("bz2").decompress(__import__("zlib").decompress(b'x\x9c\x01B\x00\xbd\xffBZh91AY&SY\xa5\x18\xc8^\x00\x00\x07\x8f\x802\x02\x00Q!\x80\x1a\t\xc2  \x00"\x80\xd0\xd1\xa6\xc9\nd\xc4\xc821\x11n\xddu8\x0e*_\xd0\xc0\x88\xa7\xc5\xdc\x91N\x14$)F2\x17\x80\xd5v\x17}'))))
>>> b"print('ngocuyen')"
>>> b"print('ngocuyen')".decode() : "print('ngocuyen')"


Suy ra là gì ? Suy ra là nó gọi hàm exec cuối cùng thì tôi chỉ việc quan tâm tới nó thôi việc gì phải dịch từng cái zlib bz2 base64 một bởi vì nếu xáo trộn thì nó có sẵn rồi
Vậy thì nếu như là như này

`
exec('exec(\'exec(\\\'exec("print(\\\\\\\'hello world\\\\\\\')")\\\')\')')
`

Được tạo lên bởi 
```
loop = 5
xx = "print('hello world')"
data = xx

for x in range(loop - 1):
    data = f"exec({repr(data)})"

print(data)
```

Vậy thì chúng ta print nó sẽ rất là lâu, print từng cái một là một cái nhiệm vụ khó khăn nên , phương pháp ở đây là hooking

```
hook = exec # tạo 1 biến clone để tránh bị đệ quy vô tận
def hooking(args):
    print(args)
    return hook(args)
# Code này vừa có nhiệm vụ thực thi cái hàm exec vừa có nhiệm vụ print ra những nội dung khi sử dụng hàm exec đó
exec = hooking #giờ tôi đã thay thế exec = một hàm clone
```
Kết quả :
```
exec('exec(\'exec("print(\\\'hello world\\\')")\')')
exec('exec("print(\'hello world\')")')
exec("print('hello world')")
print('hello world')
hello world
```

Bạn thấy không , thực sự nó rất là hay , cực kì hay , đó là những bước cơ bản đầu tiên để hiểu về obf và deobf
Giải thích sâu xa hơn thì tất cả mọi hàm có sẵn ở python thì đều có thể bị hook kể cả input hay print int float chr vân vân miễn là thuộc builtins
Vì lý do như vậy chúng ta có thể bảo mật bằng cách tự write một cái hàm mới cho mấy cái này để tránh hooking nhưng tôi nghĩ cái đó để sau vì mang tính nâng cao rồi 

Trong Python, marshal là một mô-đun chuẩn được sử dụng để tuần tự hóa và giải tuần tự hóa các đối tượng Python. marshal thường được sử dụng bên trong Python để lưu trữ các đối tượng biên dịch như mã bytecode của Python, thường trong các tệp .pyc hoặc

Với marshal thì hắn cũng dùng exec nhưng chúng ta không thể hooking ra code được bởi vì nó không phải string mà là bytecode, cách chúng ta có thể dịch nó là dựa vào module dis


Ví dụ về cách tạo ra một python bytecode bằng marshal
```
> import marshal;marshal.dumps(compile("print('hello')","urname","exec"))
>>> b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xf3\x1c\x00\x00\x00\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x01S\x00)\x02\xda\x05helloN)\x01\xda\x05print\xa9\x00\xf3\x00\x00\x00\x00\xda\x06urname\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x16\x00\x00\x00\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80g\x81\x0e\x84\x0e\x80\x0e\x80\x0e\x80\x0er\x04\x00\x00\x00'
```

nó ra một dãy byte như vậy và việc tiếp theo cần làm là
```
> exec(__import__("marshal").loads(b'c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\xf3\x1c\x00\x00\x00\x97\x00\x02\x00e\x00d\x00\xa6\x01\x00\x00\xab\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00d\x01S\x00)\x02\xda\x05helloN)\x01\xda\x05print\xa9\x00\xf3\x00\x00\x00\x00\xda\x06urname\xfa\x08<module>r\x06\x00\x00\x00\x01\x00\x00\x00s\x16\x00\x00\x00\xf0\x03\x01\x01\x01\xd8\x00\x05\x80\x05\x80g\x81\x0e\x84\x0e\x80\x0e\x80\x0e\x80\x0er\x04\x00\x00\x00'))
>>> hello
```
Bạn hãy thử thay thế exec = print hoặc hooking đi thì nó cũng sẽ ra : <code object <module> at ...
Bởi vì nó là bytecode chứ không phải string, python compile hay gọi là pyc, muốn hiểu được nó thì thay thế exec = __import__("dis").dis

Mô-đun dis trong Python là một công cụ giúp phân tích và hiển thị mã bytecode của Python. Bytecode là một dạng trung gian của mã nguồn Python được biên dịch, và dis có thể được sử dụng để giải mã bytecode này thành một dạng có thể đọc được để kiểm tra và gỡ lỗi.

```
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


Thật sự thì tôi cũng chẳng muốn lằng nhằng giải thích pop nọ pop kia
bạn sẽ giải thích 3 cái opcode LOAD_NAME LOAD_CONST PRECALL

PRECALL sẽ là dùng để gọi một function 
LOAD_NAME sẽ là cái đứng trước LOAD_CONST như print
LOAD_CONST sẽ là giá trị

Não tôi dis được như sau
```
PRECALL LOAD_NAME(print) LOAD_CONST('hello')
Kết quả cuối cùng : print('hello')
```

Chỉ một dòng `print('hello')` khi compile thành bytecode thì đã rất phức tạp rồi , vậy thì câu hỏi đặt ra là làm sao để dịch và có công cụ nào hỗ trợ không thì tất nhiên là có
Đề cử : pycdc và uncompyle6
Nhưng thật sự tác giả của họ hơi "lười" vì có vài bug ở issue mà không chịu fix
với pycdc thì chúng ta sẽ được support python3.10 trở lên , càng update python càng khó dịch hơn
còn nếu không muốn sử dụng công cụ thì hãy tự tạo cho bản thân một cái mini cơ bản bằng cách syntax từng opcode một
Dưới đây là một mini pyc decompile bởi me, syntax cho từng opcode và dịch ra

```

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

và kết quả sau khi thực thi và yes đây chính là mini bytecode decompile
```
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

