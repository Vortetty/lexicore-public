from lexicore.sorting.sortable import sortable

def sort(length: int) -> sortable:
    sort = sortable(max(min(length, 32), 2), visual=True, gif=True)
    sort.shuffle()

    i = 0
    maxi = max(min(length, 24), 2) - 1

    while i < maxi or not sort.checkSorted():
        if i == 0:
            i += 1
        if sort.get(i) >= sort.get(i-1):
            i += 1
        else:
            sort.swap(i, i-1)
            i -= 1


    sort.closePlt()

    return sort