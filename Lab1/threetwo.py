U = {i for i in range(1, 61)}

def adv_subset_maker(st):
    # Make the final solution number and D Subsets into S and D(S)
    solutions = 0
    D_set = set()
    sum_table = dict()
    lex_min = None
    lex_max = None
    # Create even and odd lists
    even = list()
    odd = list()

    for number in st:
            if number % 2 == 0:
                even.append(number)
            else:
                odd.append(number)

    # Make them into tuples so we don't change the values
    even = tuple(even)
    odd = tuple(odd)


    # GENERATE A LIST OF SUMS
    
    # Loop through 6 unique numbers (if every number is bigger than the previous, it gurantees unique numbers, + that we go through all of the lists)
    # After looping, add them together and turn it into a key for sum_table
    # that key is then used to add other types of lists that adds to the same sum
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


   


    # GENERATE A LIST OF USABLE EVEN_SUMS
    for even1 in even:
            even_sum = 0
            for even2 in even:
                if even1 >= even2:
                    continue
                for even3 in even:
                        if even1 >= even3 or even3 >= even2:
                              continue
                        # Stop here because three fixed points is a very middle starting point. 
                        # Also, if u hate, go away
                        # Check to see if the smallest/largest possible even4 and even5 are too big or 
                        # too small, and continue/break early to avoid unnecessary calculations
                        
                        partial_sum = even1 + even2 + even3
                        #partial_product = even1 * even2 * even3

                        if 330 - (partial_sum + (even3 + 2) + (even3 + 4)) > 300:
                            # Even3 is too small, won't give a small enough oddsum. 
                            continue
                        
                        if 330 - (partial_sum + even[-2] + even[-1]) < 50: #or (partial_product * even[-2] * even[-1]) % 2**6 != 0:
                            # Even3 is too large, won't give a large enough oddsum.
                            # if Even3 is too large, everything that comes from even4 and even5 is useless. 

                            # OR

                            # the best case for E3 doesn't give the required amount of 2**6, e3 is useless
                            break

                        

                        # NOTE: only works for this assignment SOLELY bc we know 
                        # even and odd are spaced by 2 here. 
                        # that's why we can afford to do even3+2 or +4

                        for even4 in even:
                                if even1 >= even4 or even2 >= even4 or even3 >= even4:
                                      continue

                                # Stop here as well to make sure to skip EVEN more unusable sums.
                                partial_sum = even1 + even2 + even3 + even4
                                partial_sum = even1 + even2 + even3 + even4
                                if 330 - (partial_sum + (even4 + 2)) > 300: 
                                    continue
                                if 330 - (partial_sum + even[-1]) < 50:
                                    break

                                for even5 in even:
                                    if even1 >= even5 or even2 >= even5 or even3 >= even5 or even4 >= even5:
                                        continue
                                    even_sum = even1 + even2 + even3 + even4 + even5
                                    even_product = even1 * even2 * even3 * even4 * even5
                                    if even_product % 2**6 != 0:
                                        continue 
                                    evens = [even1, even2, even3, even4, even5, even_product]

                                    # Omptimization Attempt 3:
                                    # oddlist reducer

                                    
                                    

                                    needed_3 = max(0, 3 - products_had(even_product, 3))
                                    needed_5 = max(0, 2 - products_had(even_product, 5))
                                    needed_7 = max(0, 1 - products_had(even_product, 7))

                                    # 6 Odds Sums = 330 - 5 Even Sums, Automatically turns the "Add to 330" condition true
                                    odd_sum = 330 - even_sum

                                    # Check to see if the numbers fits the condition (Odd sums should exist in the lookup table)
                                    if odd_sum not in sum_table:
                                        continue
                                    
                                    # LOGIC:
                                    # Unpack one list at a time, add them together with the evens, check if they 
                                    # are divisible by (2^6 * 3^4 * 5^2 * 7)
                                    
                                    for product_group in sum_table[odd_sum]:   
                                        if product_group[0] >= needed_3 and product_group[1] >= needed_5 and product_group[2] >= needed_7:
                                            max_cand_odd = sum_table[odd_sum][product_group][-1]
                                            min_cand_odd = sum_table[odd_sum][product_group][0]

                                            max_candidate = list(sorted(max_cand_odd[:-1] + evens[:-1]))
                                            min_candidate = list(sorted(min_cand_odd[:-1] + evens[:-1]))

                                            if lex_min == None or lex_min > min_candidate:
                                                    print(f"NEW MIN FOUND: Changing {lex_min} to {min_candidate}")
                                                    lex_min = sorted(min_candidate)
                                            if lex_max == None or lex_max < max_candidate:
                                                    print(f"NEW MAX FOUND: Changing {lex_max} to {max_candidate}")
                                                    lex_max = sorted(max_candidate)
                                                
                                            solutions += len(sum_table[odd_sum][product_group])
                                            D_set.add(abs(even_sum - odd_sum))
    
    D_set = tuple(sorted(D_set))

    return solutions, D_set, lex_min, lex_max

def divisiblebynumber(number):
    return number % (2**6 * 3**3 * 5**2 * 7) == 0


def products_had(product, number):
    had = 0
    while product % number == 0:
        had += 1
        product = product//number

    return had


solutions, D_set, lex_min, lex_max = adv_subset_maker(U)
smallest_dsum,largest_dsum = D_set[0], D_set[-1]
print(solutions, smallest_dsum, largest_dsum, lex_min, lex_max)