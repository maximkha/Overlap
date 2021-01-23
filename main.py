import numpy as np
from numba import cuda

file = open('covid1.aminseq',mode='r')
strA = file.read()
strA = strA.replace("\n", "")
file.close()

file = open('spike.aminseq',mode='r')
strB = file.read()
strB = strB.replace("\n", "")
file.close()

keys = ["T", "A", "G", "C"]
keyMap = {keys[i]:i for i in range(len(keys))}

@cuda.jit
def increment_by_one(an_array):
    pos = cuda.grid(1)
    if pos < an_array.size:
        an_array[pos] += 1

@cuda.jit
def same(haystack, needle, outp):
    pos = cuda.grid(1)
    if pos + needle.size < haystack.size:
        for i in range(needle.size):
            outp[pos] += min(abs(haystack[pos + i] - needle[i]), 1)#*(haystack.size - 1)

hay = np.array(list(map(keyMap.__getitem__, strA)))
print(hay)

need = np.array(list(map(keyMap.__getitem__, strB)))
print(need)

outpArr = np.zeros((hay.size - need.size,), dtype=np.float)

threadsperblock = 32
blockspergrid = (hay.size - need.size + 1 + (threadsperblock - 1)) // threadsperblock
same[blockspergrid, threadsperblock](hay, need, outpArr)

from collections import Counter
tCounter = Counter(strA)
tcounts = [tCounter[k] for k in keys]

outpArr /= need.size
outpArr = 1 - outpArr

bestIndex = np.argmax(outpArr)
print(f"Total Length {hay.size}, Needle Length: {need.size}, TotalOut: {outpArr.size}")
print(f"Best Match: {bestIndex} with value of {outpArr[bestIndex]}")
# print(f"Technically {outpArr[21563]} or {outpArr[21562]} or {outpArr[21564]}")

print(outpArr)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.figure()
plt.title("% Match Allignment")
plt.xlabel("Basepair #")
plt.ylabel("% Match")
plt.vlines(bestIndex, min(outpArr), outpArr[bestIndex]*1.1, color="red")
plt.hlines(outpArr[bestIndex], 0, outpArr.size, color="red")
plt.plot(range(outpArr.size), outpArr)

plt.figure()
plt.title("Base Counts")
plt.xlabel("Base")
plt.ylabel("Total Count")
plt.bar(keys, tcounts)

# generate diff of best
plt.figure()
plt.title("Diff")
plt.xlabel("Basepair offset")
ax = plt.gca()

for i in range(len(need)):
    if min(abs(hay[bestIndex + i] - need[i]), 1) > 0:
        pat = patches.Rectangle((i, 0), 1, 1, fill=True, color="red")
        ax.add_patch(pat)
        #plt.vlines(i, 0, 4, color="red")
    else:
        pat = patches.Rectangle((i, 0), 1, 1, fill=True, color="green")
        ax.add_patch(pat)
        #plt.vlines(i, 0, 4, color="green")

handles, labels = ax.get_legend_handles_labels()
pat = patches.Patch(color='green', label='Same')
handles.append(pat)
pat = patches.Patch(color='red', label='Diff')
handles.append(pat) 
plt.legend(handles=handles, loc='upper right')

plt.xlim([0, len(need)])
plt.ylim([0, 1])

# plt.plot(range(len(need)), need)
# plt.plot(range(len(diffMarkers)), diffMarkers)

plt.show()