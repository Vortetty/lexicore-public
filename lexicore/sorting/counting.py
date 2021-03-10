try:
    from lexicore.sorting.sortable import sortable
except:
    from sortable import sortable

import time

def sort(length: int) -> sortable:
    sort = sortable(max(min(length, 24), 2), visual=True, gif=True)
    sort.shuffle()

    nums = list(dict.fromkeys(sort.getList()))
    numlist = list(sort.getList())
    outList = []

    while len(nums) > 0:
        minNum = min(nums)
        nums.remove(minNum)
        count = numlist.count(minNum)
        numlist.remove(minNum)
        for _ in range(count):
            outList.append(minNum)
            numlist.append(0)
        for i in range(len(numlist)):
            sort.set(i, numlist[i], renderFrame=False)
        sort.renderFrame()
    
    for i in range(len(outList)):
        sort.set(i, outList[i])

    sort.closePlt()

    return sort
