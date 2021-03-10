try:
    from lexicore.sorting.sortable import sortable
except:
    from sortable import sortable

import time

def sort(length: int) -> sortable:
    sort = sortable(max(min(length, 32), 2), visual=True, gif=True)
    sort.shuffle()
    
    while not sort.checkSorted():
        for i in range(sort.size):
            sort.swap(i, sort.get(i)-1)

    sort.closePlt()

    return sort
