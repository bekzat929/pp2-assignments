class rectangle:
    def __init__(self,n,m):
        self.n = n
        self.m = m
    def area(self):
        return self.n*self.m

n,m=map(int,input().split())
rect=rectangle(n,m)
print(rect.area())
