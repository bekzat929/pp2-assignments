def gen(a):
    for i in range(2,a+1):
        sum=0
        for j in range(2,a+1):
            if i%j==0:
                sum=sum+1
        if sum<=1:
            yield i
n=int(input())
for num in gen(n):
    print(num,end=" ")