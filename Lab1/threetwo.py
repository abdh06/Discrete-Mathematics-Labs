
U = {i for i in range(1, 61)}

def adv_subset_maker(st):
    # Make the final solution subsets into set S and D(S)
    solutions = list()
    D_sub = list()

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

    # there are 5 even numbers, so we look for the number 330 - even_sum to find odd sum

    for even1 in even:
            even_sum = 0
            for even2 in even:
                if even1 == even2:
                    continue
                for even3 in even:
                        if even1 == even3 or even3 == even2:
                              continue
                        for even4 in even:
                                if even1 == even4 or even2 == even4 or even3 == even4:
                                      continue
                                for even5 in even:
                                    if even1 == even5 or even2 == even5 or even3 == even5 or even4 == even5:
                                        continue
                                    even_sum = even1 + even2 + even3 + even4 + even5
                                    evens = [even1, even2, even3, even4, even5]
    
                                    # 6 Odds Sums = 330 - 5 Even Sums
                                    odd_sum = 330 - even_sum
    
                                    # 3. Check to see if the numbers fits the conditions (Odd sums cannot be negative, nor can it be even)
                                    if odd_sum < 0 or odd_sum % 2 == 0:
                                        continue
                            # Skips the even_nums as we know this does NOT work
    
                        num1, num2, num3, num4, num5, num6 = 0,0,0,0,0,0

                        for odd1 in odd:
                            for odd2 in odd:
                                if odd1 == odd2:
                                    continue
                                for odd3 in odd:
                                    if odd1 == odd3 or odd2 == odd3:
                                        continue
                                    for odd4 in odd:
                                        if odd1 == odd4 or odd2 == odd4 or odd3 == odd4:
                                            continue
                                        for odd5 in odd:
                                            if odd1 == odd5 or odd2 == odd5 or odd3 == odd5 or odd4 == odd5:
                                                continue
                                            for odd6 in odd:
                                                if odd1 == odd6 or odd2 == odd6 or odd3 == odd6 or odd4 == odd6 or odd5 == odd6:
                                                    continue
                                                if odd1 + odd2 + odd3 + odd4 + odd5 + odd6 == odd_sum:
                                                    odds = [odd1, odd2, odd3, odd4, odd5, odd6]
                                                    possible_solution = sorted((*odds, *evens))
                                                    if divisiblebynumber(possible_solution) and sumequals330(possible_solution):
                                                        if possible_solution not in solutions:
                                                            solutions.append(possible_solution)
                                                            D_sub.append(abs(even_sum - odd_sum))

    return solutions, D_sub


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

def sumequals330(subset):
    if len(subset) != 11:
          return False

    sum = 0

    for number in subset:
            sum += number
    
    if sum == 330:
            return True
    
    return False

solutions, d_sub = adv_subset_maker(U)
print(len(solutions))