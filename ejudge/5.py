class Account:
    def __init__(self,B,W):
        self.B = B
        self.W = W

    def dep(self,amount):
            self.balance += amount

    def calc(self):
        if self.W>self.B:
            print("influence")
        else:
            print(self.W)

B,W = map(int,input().split())
acc = Account(B,W)
acc.calc()