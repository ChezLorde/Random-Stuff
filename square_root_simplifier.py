import math

number = int(input("Please select a number. -->  "))

root_factors = []
int_factors = [1]

def get_squares_list(target):
  i = 2
  numlist = [2]
  while numlist[i - 2] ** 2 <= target:
    i += 1
    numlist.append(i)
  return numlist[0:len(numlist) - 1]

def find_roots(target):
  global int_factors
  
  factors = get_squares_list(target)
  remainder = target
  
  for i in range(len(factors) - 1,-1,-1):
    divide = remainder / (factors[i] ** 2)
    print("Current Remainder: "+str(remainder)+"   Factor: "+str(factors[i])+" ("+str(factors[i] ** 2)+")   Quotient: "+str(divide))
    if divide - int(divide) == 0:
      print("Integer Factor Found!")
      int_factors.append(factors[i])
      remainder = divide
      if divide == 1:
        break
      
  return remainder
    
def try_divide(target):
  global root_factors
  found_factors = False
  
  for i in range(2, int(target / 2), 1):
    divide = target / i
    print("Attempting division of "+str(target)+" by divisor "+str(i)+"    Result: "+str(divide))
    if divide - int(divide) == 0:
      print("Integer factor found!")
      try_divide(int(divide))
      try_divide(i)
      found_factors = True
      break
  
  if not found_factors:
    root_factors.append(target)
    return target
    
def main(target):
  nonint = find_roots(number)
  try_divide(nonint)
  
  coefficient = 1
  for factor in (int_factors):
    coefficient *= factor
  
  print("-----------------------------\nFinal Result:\n\n")
  print("Integer Coefficient: "+str(coefficient)+"\n\nPrime Radical Components:\n")
  for rad in root_factors:
    print("√("+str(rad)+")")
  

main(number)

