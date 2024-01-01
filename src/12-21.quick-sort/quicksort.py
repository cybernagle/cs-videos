def quick(arr):
    if len(arr) <=1:
        return arr
    pivot = arr[0]
    smaller = [i for i in arr if i < pivot]
    larger = [i for i in arr if i > pivot]
    return quick(smaller) + [pivot] + quick(larger)