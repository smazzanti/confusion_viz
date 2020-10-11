def find_closest(look_in, look_for):
    """
    Find elements of array 'look_in' that are as close as possible to the elements of array 'look_for'.
    Both 'look_in' and 'look_for' are assumed to be sorted in descending order.
    Example: look_in = [1., 3.5, 5.0, 6.9], look_for = [-2., .8, 4.9] -> i_found = [0, 2]
    
    Args:
        look_in: iterable
        look_for: iterable
        
    Returns:
        i_found: list containing indexes of elements that are in 'look_in'
    """

    i_found = []
    i_in, i_for = 0, 0
    midpoint_before = float('Inf')

    while i_for < len(look_for):  
        midpoint_after = sum(look_in[i_in : i_in + 2]) / 2 if i_in < len(look_in) - 1 else float('-Inf')
        if look_for[i_for] <= midpoint_after:
            i_in += 1
            midpoint_before = midpoint_after
        elif look_for[i_for] > midpoint_before:
            i_for += 1
        else:
            i_found += [i_in]
            i_for += 1
            i_in += 1
            midpoint_before = midpoint_after 

    return i_found
