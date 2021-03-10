from lexicore.sorting.sortable import sortable

def sort(length: int) -> sortable:
    sort = sortable(max(min(length, 4), 2), visual=True, gif=True)
    sort.shuffle()

    while not sort.checkSorted():
        sort.shuffleFast()

    sort.closePlt()

    return sort


