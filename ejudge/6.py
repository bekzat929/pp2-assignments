class Mynums:
    def __init__(self,limit,start=0):
        self.start=start
        self.limit=limit
    def __iter__(self):
        return self
    def __next__(self):
        if self.start>self.limit:
            raise StopIteration
        else:
            temp = self.start
            self.start+=2
            return temp




n=int(input())
nums=Mynums(n)
nums_iter = iter(nums)
for i, num in enumerate(nums):
    if i != 0:
        print(',', end='')
    print(num, end='')
