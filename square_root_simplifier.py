# (Square) Root Simplifier
# Goal: For an inputted number, return the most simplified possible radical notation of its root.
# Works in two phases: Phase 1 is to extract the integer part of the root, and Phase 2 is to reduce the remainder to its prime factors

import time

number = int(input("Please select a number. -->  "))

prime_root_factors = []

root = 10 # <- Square root, Cube root etc.

# PHASE 1: EXTRACT THE INTEGER FACTOR

# Returns a list of numbers to be brute-force divided, from 2^root from n^root, where n^root < target < (n+1)^root. This allows us to factor out any integer part of the result.
# Also returns a list of the numbers (2 to n), so we can add them to the integer coefficient without doing more calculations
def get_squares_list(target):
  i = 2
  numlist = [i]
  explist = [i ** root]
  while explist[i - 2] <= target:
    i += 1
    numlist.append(i)
    explist.append(i ** root)
  return numlist[0:(i - 2)], explist[0:(i - 2)]

# Extracts the integer factor of the root.
def find_roots(target):
  
  roots, factors = get_squares_list(target)
  coefficient = 1
  remainder = target
  
  for i in range(len(factors) - 1,-1,-1):
    divide = remainder / factors[i]
    print("Current Remainder: "+str(remainder)+"   Factor: "+str(factors[i])+" ("+str(roots[i])+"^"+str(root)+")   Quotient: "+str(divide))
    if divide == int(divide):
      print("Integer Factor Found!")
      coefficient *= roots[i]
      remainder = divide
      if divide == 1:
        break
      
  return coefficient, remainder

# PHASE 2: REDUCE THE ROOT TO ITS PRIME FACTORS

# Recursive function for finding all prime factors of a number. Adds them to prime_root_factors.
def try_divide(target):
  global prime_root_factors
  found_factors = False
  
  for i in range(int(target / 2), 2, -1):
    divide = target / i
    print("Attempting division of "+str(target)+" by divisor "+str(i)+"    Result: "+str(divide))
    if divide - int(divide) == 0:
      print("Integer factor found!")
      try_divide(int(divide))
      try_divide(i)
      found_factors = True
      break
  
  if not found_factors:
    prime_root_factors.append(target)
    return target

# Puts everything together Includes Timing.
def simplify_root(target):
  global prime_root_factors
  prime_root_factors = []
  start_time = time.time()
  coefficient, remainder = find_roots(number)
  try_divide(remainder)
  total_time = time.time() - start_time
  
  print("-----------------------------\nFinal Result:   "+str(total_time)+" seconds\n\n")
  print("Integer Coefficient: "+str(coefficient)+"\n\nPrime Radical Components:\n")
  for rad in prime_root_factors:
    if rad == 1.0:
      print("None")
    else:
      print(str(root)+"√("+str(rad)+")")
  
  return total_time, coefficient, prime_root_factors
  
simplify_root(number)

