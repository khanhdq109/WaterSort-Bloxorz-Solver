def giaithua(n):
    if n == 0: return 1
    return n * giaithua(n - 1)

list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
list = list[0:9]
print(list)