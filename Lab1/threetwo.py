


U = {i for i in range(1, 61)}

def adv_subset_maker(st):
    # Make the final solution subsets into set S and D(S)
    solutions = set()
    D_set = set()
    sum_table = dict()
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

                            # Minimum Even_sum = 2 + 4 + 6 + 8 + 10  = 30
                            # Maximum Even_sum = 60 + 58 + 56 + 54 + 52 = 280
                            # That means:
                            # smallest possible odd_sum = 330 - 280 = 50
                            # largest possible odd_sum = 330 - 30 = 300
                            # We discard anything else
                            if odd_sum < 50 or odd_sum > 300:
                               continue
                            if odd_sum not in sum_table:
                                sum_table[odd_sum] = []
                            sum_table[odd_sum].append([odd1, odd2, odd3, odd4, odd5, odd6])

    

    # There are 5 even numbers, so we look for the number 330 - even_sum to find odd sum

    for even1 in even:
            even_sum = 0
            for even2 in even:
                if even1 >= even2:
                    continue
                for even3 in even:
                        if even1 >= even3 or even3 >= even2:
                              continue
                        for even4 in even:
                                if even1 >= even4 or even2 >= even4 or even3 >= even4:
                                      continue
                                for even5 in even:
                                    if even1 >= even5 or even2 >= even5 or even3 >= even5 or even4 >= even5:
                                        continue
                                    even_sum = even1 + even2 + even3 + even4 + even5
                                    evens = [even1, even2, even3, even4, even5]
    
                                    # 6 Odds Sums = 330 - 5 Even Sums, Automatically turns the "Add to 330" condition true
                                    odd_sum = 330 - even_sum

                                    # Check to see if the numbers fits the condition (Odd sums should exist in the lookup table)
                                    if odd_sum not in sum_table:
                                        continue

                                    # LOGIC:
                                    # Unpack one list at a time, add them together with the evens, check if they 
                                    # are divisible by (2^6 * 3^4 * 5^2 * 7)

                                    for odd_list in sum_table[odd_sum]:
                                            possible_solution = tuple(sorted([*odd_list, *evens]))
                                            if divisiblebynumber(possible_solution):
                                                    solutions.add(possible_solution)
                                                    D_set.add(abs(even_sum - odd_sum))
    
    solutions = tuple(sorted(solutions))
    D_set = tuple(sorted(D_set))

    return solutions, D_set


def divisiblebynumber(subset):
    if len(subset) != 11:
            return False

    term = 1

    for number in subset:
        term *= number

    num = (2**6 * 3**3 * 5**2 * 7)

    if term % num == 0:
        return True

    return False

# Unused
# def sumequals330(subset):
    if len(subset) != 11:
          return False

    sum = 0

    for number in subset:
            sum += number
    
    if sum == 330:
            return True
    
    return False

solutions, D_set = adv_subset_maker(U)
smallest_dsum,largest_dsum = D_set[0], D_set[-1]
lex_small, lex_large = solutions[0], solutions[-1]
print(len(solutions), smallest_dsum, largest_dsum, lex_small, lex_large)