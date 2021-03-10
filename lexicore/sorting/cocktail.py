from lexicore.sorting.sortable import sortable

def sort(length: int) -> sortable:
    sort = sortable(max(min(length, 16), 2), visual=True, gif=True)
    sort.shuffle()

    while not sort.checkSorted():
        for i in range(sort.size-1):
            if sort.get(i) > sort.get(i+1):
                sort.swap(i, i+1)

        for i in range(1, sort.size-1):
            if sort.get(sort.size-1-i) > sort.get(sort.size-i):
                sort.swap(sort.size-1-i, sort.size-i)

    sort.closePlt()

    return sort


