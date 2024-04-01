def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    string = s.strip()
    if is_len(string) and is_alphanum(string) and first_two(string) and ends_num(string): 
       return True 
    else: 
       return False

def is_len(s): 
    slen = len(s)
    return slen > 1 and slen < 7

def is_alphanum(s): 
    return s.isalnum()

def first_two(s): 
    i = 0
    while(i < 2):
      if s[i].isalpha():
        i += 1
        continue
      else: 
        return False
    return True      

def ends_num(s): 
   i = 0
   slen = len(s)
   while i < slen: 
      if s[i].isalpha():
         i += 1
      else: 
         break
   if i < slen and int(s[i]) == 0:
      return False
   while i < slen:
      if s[i].isdigit():
         i += 1
      else: 
         return False
   return True

main()
