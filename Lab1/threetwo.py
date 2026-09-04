U = {i for i in range(1, 61)}

def adv_subset_maker(st):


    # Create variables needed.
    solutions = 0
    D_set = set()
    sum_table = dict()
    lex_min = None
    lex_max = None
    even = list()
    odd = list()

    # Separate odds and evens
    for number in st:
            if number % 2 == 0:
                even.append(number)
            else:
                odd.append(number)

    # NOTE: GENERATE A LIST OF SUMS AND PRODUCT GROUPS FOR THE LAST 2 CONDITIONS
    
    # Loop through 6 unique numbers (if every number is bigger than the previous, 
    # it gurantees unique numbers, + we only go through them once)
    # After looping, add them together and turn the sum into a key for sum_table, that leads to a second dictionary
    # we also add their products together, and figure out how many products of 3, 5 and 7 they have.
    # Create each of those products into separate 24 groups (3^1, 0, 0, 3^2, 0 0 and so on. (4*3*2 = 24))
    # THOSE <=24 groups are turned into keys that shows up in the sum_table[odd_sums]
    # When a new odd_list is generated, check to see which one of the 24 groups it fits, and then
    # append them and their products there.
    # IMPORTANT LATER, PROMISE

    for odd1 in odd:
        for odd2 in odd:
            if odd1 >= odd2:
                continue
            for odd3 in odd:
                if odd1 >= odd3 or odd2 >= odd3:
                    continue
                for odd4 in odd:
                    if odd1 >= odd4 or odd2 >= odd4 or odd3 >= odd4:
                        continue
                    for odd5 in odd:
                        if odd1 >= odd5 or odd2 >= odd5 or odd3 >= odd5 or odd4 >= odd5:
                            continue
                        for odd6 in odd:
                            if odd1 >= odd6 or odd2 >= odd6 or odd3 >= odd6 or odd4 >= odd6 or odd5 >= odd6:
                                continue
                            odd_sum = odd1 + odd2 + odd3 + odd4 + odd5 + odd6
                            odd_product = odd1 * odd2 * odd3 * odd4 * odd5 * odd6
                            # Minimum Even_sum = 2 + 4 + 6 + 8 + 10  = 30
                            # Maximum Even_sum = 60 + 58 + 56 + 54 + 52 = 280
                            # That means:
                            # smallest possible odd_sum = 330 - 280 = 50
                            # largest possible odd_sum = 330 - 30 = 300
                            # We discard anything else
                            if odd_sum < 50 or odd_sum > 300:
                               continue
                        
                            group = (min(products_had(odd_product, 3), 3), 
                                   min(products_had(odd_product, 5), 2), 
                                   min(products_had(odd_product, 7), 1))
                            
                            if odd_sum not in sum_table:
                                sum_table[odd_sum] = {}
                            if group not in sum_table[odd_sum]:
                                 sum_table[odd_sum][group] = [] 
                            sum_table[odd_sum][group].append([odd1, odd2, odd3, odd4, odd5, odd6, odd_product])


    # NOTE: GENERATE A LIST OF USABLE EVEN_SUMS
    # 
    for even1 in even:
        even_sum = 0
        for even2 in even:
            if even1 >= even2:
                continue
            for even3 in even:
                    if even1 >= even3 or even3 >= even2:
                            continue
                    # Stop here because three fixed points is a great pruning point (middle). 
                    # Check to see if the smallest/largest possible even4 and even5 are too big or 
                    # too small, and continue/break early to avoid unnecessary calculations
                        
                    partial_sum = even1 + even2 + even3

                    if 330 - (partial_sum + (even3 + 2) + (even3 + 4)) > 300: # Yes, this is hardcoded.
                        continue # Even3 is too small, won't give a small enough oddsum. 
                        
                    if 330 - (partial_sum + even[-2] + even[-1]) < 50:
                        break # Even3 is too large, will give a too small odd_sum

                    for even4 in even:
                            if even1 >= even4 or even2 >= even4 or even3 >= even4:
                                continue

                            # Pruning Part 2.
                            partial_sum = even1 + even2 + even3 + even4

                            if 330 - (partial_sum + (even4 + 2)) > 300: 
                                continue
                            if 330 - (partial_sum + even[-1]) < 50:
                                break

                            for even5 in even:
                                    if even1 >= even5 or even2 >= even5 or even3 >= even5 or even4 >= even5:
                                        continue
                                    
                                    even_product = even1 * even2 * even3 * even4 * even5
                                    if even_product % 2**6 != 0:
                                        continue 

                                    needed_3 = max(0, 3 - products_had(even_product, 3))
                                    needed_5 = max(0, 2 - products_had(even_product, 5))
                                    needed_7 = max(0, 1 - products_had(even_product, 7))

                                    evens = [even1, even2, even3, even4, even5]
                                    
                                    even_sum = even1 + even2 + even3 + even4 + even5

                                    
                                    odd_sum = 330 - even_sum
                                    if odd_sum not in sum_table:
                                        continue


                                    # Finding the actual solutions.
                                    for product_group in sum_table[odd_sum]:   
                                        if (product_group[0] >= needed_3 and product_group[1] >= needed_5 and product_group[2] >= needed_7): 
                                            # Finding the smallest and largest possible subset by 
                                            # checking the smallest and largest odd list to 
                                            # not go through the same solution 600m times
                                            
                                            max_cand_odd = sum_table[odd_sum][product_group][-1]
                                            min_cand_odd = sum_table[odd_sum][product_group][0]

                                            max_candidate = list(sorted(max_cand_odd[:-1] + evens))
                                            min_candidate = list(sorted(min_cand_odd[:-1] + evens))

                                            if lex_min == None or lex_min > min_candidate:
                                                    lex_min = min_candidate
                                            if lex_max == None or lex_max < max_candidate:
                                                    lex_max = max_candidate
                                                
                                            solutions += len(sum_table[odd_sum][product_group])
                                            D_set.add(abs(even_sum - odd_sum))
    
    D_set = tuple(sorted(D_set))

    return solutions, D_set, lex_min, lex_max


def products_had(product, number):
    had = 0
    while product % number == 0:
        had += 1
        product = product//number

    return had


solutions, D_set, lex_min, lex_max = adv_subset_maker(U)
smallest_dsum,largest_dsum = D_set[0], D_set[-1]
print(solutions, smallest_dsum, largest_dsum, lex_min, lex_max)