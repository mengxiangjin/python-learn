import random
iv = ''.join(['%x' % random.randint(1,15) for i in range(16)])
print(iv)