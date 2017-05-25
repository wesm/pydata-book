#-*-encoding:utf-8-*-

'''
import random
position = 0
walk = [position]
steps = 1000
for i in xrange (steps):
    step = 1 if random.randint(0,1) else -1
    position +=step
    walk.append(position)
    print  position
'''
#一次模拟多个随机漫步

import  numpy as np

nwalks = 10
nsteps = 5
value = 5
draws = np.random.randint(0,2,size=(nwalks,nsteps))  # numpy的randint前两个参数一开一闭，所以此时会出现0或1
print draws
steps = np.where(draws > 0, 1, -1)
walks = steps.cumsum(1)
print walks
print walks.min()
print walks.max()
#print (np.abs(walks) >= 10).argmax()  #argmax 返回该布尔型数组第一个最大值的索引
hits30 = (np.abs(walks) >= value).any(1)
print hits30

print hits30.sum()  # 到达30或-30的数量

crossing_times = (np.abs(walks[hits30]) >= value).argmax(1)
print crossing_times.mean()




