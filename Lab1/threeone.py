# Exercise 3.1


def subset_maker(st):

    solutions = []
    casea_solution = []
    caseb_solution = []

    # Generating 2 sets that divides the set given into an even and odd one
    even = list()
    odd = list()

    for number in st:
        if number % 2 == 0:
            even.append(number)
        else:
            odd.append(number)

    # Case A, 3 Even + 4 Odds = 105
  

    # 1. Make 3 Even values as a guess
    
    for number1 in even:
        even_sum = 0
        for number2 in even:
            if number1 == number2:
                continue
            for number3 in even:
                    if number1 == number3 or number3 == number2:
                        continue
                    even_sum = number1 + number2 + number3

                    # 2. Find the Odd Sum
                    # 4 Odds Sums = 105 - 3 Even Sums
                    Odds_sum = 105 - even_sum

                    # 3. Check to see if the numbers fits the conditions (Odd sums cannot be negative, nor can it be even)
                    if Odds_sum < 0 or Odds_sum % 2 == 0:
                        continue
                        # Skips the even_nums as we know this does NOT work

                    num1, num2, num3, num4 = 0,0,0,0

                    for n1 in odd:
                        for n2 in odd:
                            if n1 == n2:
                                continue
                            for n3 in odd:
                                if n1 == n3 or n2 == n3:
                                    continue
                                for n4 in odd:
                                    if n1 == n4 or n2 == n4 or n3 == n4:
                                        continue
                                    if n1 + n2 + n3 + n4 == Odds_sum:
                                        num1, num2, num3, num4 = n1, n2, n3, n4
                                        # num1 - num4 = Odd numbers, number 1 to number 3 = Even numbers
                                        possible_solution = sorted((num1, num2, num3, num4, number1, number2, number3))
                                        if divideby360(possible_solution) == True and sumto105(possible_solution) == True:
                                            if possible_solution not in solutions:
                                                solutions.append(possible_solution)
                                                casea_solution.append(possible_solution)

                                        
                        
                        
    # Case B

    for number1 in even:
            even_sum = 0
            for number2 in even:
                if number1 == number2:
                    continue
                for number3 in even:
                        if number1 == number3 or number3 == number2:
                            continue
                        for number4 in even:
                            if number1 == number4 or number2 == number4 or number3 == number4:
                                continue
                            even_sum = number1 + number2 + number3 + number4
    
                            # 2. Find the Odd Sum
                            # 3 Odds Sums = 105 - 4 Even Sums
                            Odds_sum = 105 - even_sum
    
                            # 3. Check to see if the numbers fits the conditions (Odd sums cannot be negative, nor can it be even)
                            if Odds_sum < 0 or Odds_sum % 2 == 0:
                               continue
                            # Skips the even_nums as we know this does NOT work
    
                            num1, num2, num3 = 0,0,0
    
                            for n1 in odd:
                                for n2 in odd:
                                    if n1 == n2:
                                        continue
                                    for n3 in odd:
                                        if n1 == n3 or n2 == n3:
                                            continue
                                        if n1 + n2 + n3 == Odds_sum:
                                            num1, num2, num3 = n1, n2, n3
                                            # num1 - num3 = Odd numbers, number 1 to number 4 = Even numbers
                                            possible_solution = sorted((num1, num2, num3, number1, number2, number3, number4))
                                            if divideby360(possible_solution) == True and sumto105(possible_solution) == True:
                                                if possible_solution not in solutions:
                                                    solutions.append(possible_solution)
                                                    caseb_solution.append(possible_solution)

    
    
    return solutions, casea_solution, caseb_solution

def divideby360(subset):
    if len(subset) != 7:
        return False
    
    term = 1

    for number in subset:
        term *= number

    if term % 360 == 0:
        return True

    return False

def sumto105(subset):
    # Check if lists length is 7
    if len(subset)!= 7:
        return False

    sum = 0

    for number in subset:
        sum += number
    
    if sum == 105:
        return True

    return False
