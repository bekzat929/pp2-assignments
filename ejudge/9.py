def gen(a):
    f=1
    for i in range(a+1):
        yield f
        f=f*2

n=int(input())
for x in gen(n):
    print(x,end=" ")