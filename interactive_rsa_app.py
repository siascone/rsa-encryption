# imported modules
import math # Math module, used below for interger type casting
import time # Time module, used below for impression of computation time by bot
import ast # Abstract Syntax Trees, used below to convert string versions of lists to lists literals

# Fast Modular Exponentiation
def FME(b, n, m):        
    # b = base being raised, n exponent, m = divisor for mod
    result = 1 # result variable
    square = b # power variable set to base
    
    while n > 0: # loop convert n to binary
        k = n % 2 # extract least significatn bit from n
        
        if k == 1: # current least sig bit is not zero, 2^that power has significance
            result = (result * square) % m # increment result
        
        square = (square * square) % m # square and mod square for next iteration
        
        n = n // 2 # int divs of n by same value n was moded by, without this loop will never end
        
    return result

# Euclidean Algorithm
def Euclidean_Alg(a, b):
    # Check for negative inputs and raise error
    if a < 0 or b < 0:
        raise "Inputs must be positive integers."
        
    if b > a: # Check input values for max and min
        _a = b # assign max val to _a and preserve original a
        _b = a # assign min val to _b and preserve original b
    else: # otherwise a is already max and b is already min
        _a = a # preserve original a
        _b = b # preserve original b
    
    while (_b > 0): #TODO give reason for _b as iteration
        k = _a % _b # calculate remainder of _a and _b
        # q = _b // _a # Save q(uotient) of _a and _b NOT NEEDED HERE
        
        _a = _b # set next _a to be modded to current _b
        _b = k # set current _b to k to use as next modulous

    return _a

# Extended Euclidean Algorithm
def EEA(a, b):
    # Check for negative inputs and raise error
    if a < 0 or b < 0:
        raise "Inputs must be positive integers."
        
    if b > a: # Check input values for max and min
        _a = b # assign max val to _a and preserve original a
        _b = a # assign min val to _b and preserve original b
    else: # otherwise a is already max and b is already min
        _a = a # preserve original a
        _b = b # preserve original b
    
    s1, t1 = 1, 0 # starting linear coefs for a (i.e. a = 1 * a + 0 * b)
    s2, t2 = 0, 1 # starting linear coefs for b (i.e. b = 0 * a + 1 * b)
    
    while (_b > 0): # TODO give reason why using _b for loop
        k = _a % _b # calculate remainder of _a and _b
        q = _a // _b # calculate (q)uotient of _a and _b
        
        _a = _b # set next _a to current _b
        _b = k # set next _b to current k (remainder of _a and _b)
        
        s1_hat, t1_hat = s2, t2 # temp value of new s1, t1
        s2_hat, t2_hat = s1 - q * s2, t1 - q * t2 # temp value of new s2 and t2
        
        s1, t1 = s1_hat, t1_hat # update s1, t1 with new values from s1_hat, t1_hat (old _b 
                                # coefs)
        s2, t2 = s2_hat, t2_hat # update s2, t2 with new values modified by quotient s2_hat
                                # t2_hat (i.e. new _b coefs)
        
    return [_a, (s1, t1)] # return collection of _a as GCD and s1 and t1 as bezout's coefs
    
# Generate Public Key (n, e)
def Find_Public_Key_e(p, q):
    
    n = p * q # n as a product of two primes p and q
    
    pq_dec = (p - 1) * (q - 1) # product of the decrement of p and q for use in calculating e
    # print(p-1, q-1)
    # print(prod_pq_dec)
    
    # e must satisfy 1 < e < (p - 1)(q - 1), use as loop bounds
    # e must also satisfy e != p and e !=q
    e = 2
    
    while e < pq_dec: # potential costly loop for large numbers
        # if e is ever equal to p or q, increment it and move on to the next iteration
        if e == p or e == q:
            e += 1
            continue
        # check if GCD of e and prod_pq_dec == 1 (i.e. rel prime)
        if Euclidean_Alg(pq_dec, e) == 1: 
            break
        
        e += 1
    
    return (n, e)

# Generate Private Key (n,  d)
def Find_Private_Key_d(e, p, q):
    # We need to find inverse of e mod (p - 1)(q - 1)
    
    pq_dec = (p - 1) * (q - 1)
    
    # EEA returns gcd and tuple of Bezout's coeffs. We need the second coeff in the tupple
    bz_coef = EEA(pq_dec, e)[1][1] # Bezout's coef for e
   
    # to calculate the modular inverse of e we need to take the modulous of bz_coef and pq_dec
    d = bz_coef % pq_dec 
   
    return d

# Convert Text to Integer List
def Convert_Text(_string):
    # initialize an empty list to store int representation of string characters
    integer_list = [] 
    

    for char in _string: # examine each character of the string one at a time
        integer_list.append(ord(char)) # convert character to integer and push into storage list
                                       # preserve original character order
    return integer_list

# Convert Integer List to Text String
def Convert_Num(_list):
    _string = ''
    
    for num in _list:
        _string += chr(num)

    return _string


# Encode a message
def Encode(n, e, message):
    message_nums = Convert_Text(message) # get list of message characters as numbers to encode
    
    cipher_text = [] # setup return list to hold encrypted numbers form message_nums
    
    for num in message_nums: # iterate through each number
        encoded_num = FME(num, e, n) # perform fast modular exponentiation to encode each number
        cipher_text.append(encoded_num) # add each encoded number to output list
    
    return cipher_text

# Decode a message
def Decode(n, d, cipher_text):    
    # initialize empty return string,
    message = '' # could be left for initilization at converstion of num to letter
    
    decoded_nums = [] # initialize empty integer list for decoded numbers
    
    # iterate through each integer in input cipher_text
    for num in cipher_text:
        decoded_num = FME(num, d, n) # perform fast modular exponentiation to encode each number
                                     # pass in d, modular inverse of e, to decode encoded FME
        decoded_nums.append(decoded_num) # add decoded_num to decoded_nums list
        
    message = Convert_Num(decoded_nums) # convert decoded_nums integer list to character string
    
    return message

def factorize(n):
    for i in range(2, int(math.sqrt(n))): # iterate from 2 to sqrt(n) to find a factor p
        if n % i == 0: # check for factors, if n / i has no remainder then it is a factor
            p = i # set p to i (factor of n)
            q = n // p # calculate q as corresponding factor to p
            
            return (p, q)
    
    return False # if we don't find any factors return False

# useful for relatively small primes
# used to check for prime number entries
def is_prime(num):
    for i in range(2, int(math.sqrt(num))): 
        if num % i == 0: # if i devides num i is a factor and n is not prime
            return False
        
    return True

# Dictionary for reused print statements
prompts = {
    0: """Welcome, I am an RSA helper bot. How can I help you?
    1. Generate Public and Private Keys
    2. Encrypt a message
    3. Decrypt a message
    4. Crack a code
    5. Exit the program""",
    1:  """How would you like to proceed?
    1. Generate Public and Private Keys
    2. Encrypt a message
    3. Decrypt a message
    4. Crack a code
    5. Exit the program""",
    2: "------------------------------------------------------"
}

# Generate Keys upon user request
def process_1_generate_keys():
    print(prompts[2])
    print("Awesome! Let's generate some encryption keys.")
    
    # Get user input for primes p and q
    p = int(input("Please enter a prime number: "))
    q = int(input("Please enter a differnt second prime number: "))
    
    # Check if p or q is not prime
        # have user start over if not prime
        # continue on to generate keys if prime
    if not is_prime(p) or not is_prime(q):
        print("     Your p or q was not prime. Please try again!")
    else:
        print(prompts[2])
        print("Generating keys...")
        time.sleep(1) # Give user the feeling of computations occuring
        
        # Get public keys n and e, and extract
        pub_keys = Find_Public_Key_e(p, q)
        n = pub_keys[0]
        e = pub_keys[1]
        
        # Get private key d
        d = Find_Private_Key_d(e, p, q)

        print("     Your Public Key n is: ", n)
        print("     Your Public Key e is: ", e)
        print("     Your Private Key d is: ", d)
    
    
def process_2_encode():
    print(prompts[2])
    print("Alright! Let's encrypt a message.")
    
    # Get user input for n and e Public Keys
    n = int(input("Please enter your Public Key n: "))
    e = int(input("Please enter your Public Key e: "))
    
    # Get user input for message to be encrypted
    message = input("What is your message you'd like to encrypt? ")
                    
    print(prompts[2])
    print("Encrypting your message...")
    time.sleep(1) # Give user the feeling of computations occuring

    # Encode message
    encrypted_message = Encode(n, e, message)
    print("     Your encrypted message: ", encrypted_message)
    

def process_3_decode():
    print(prompts[2])
    print("Sweet! Let's decrypt a message")
    
    # Get user input for n and d Private Keys
    n = int(input("Please enter your Public Key n: "))
    d = int(input("Please enter your Private Key d: "))
    
    # Get user input for message to be decrypted
    encrypted_message = ast.literal_eval(input("What would you like to decrypt? "))
    
    print(prompts[2])
    print("Decrypting your message...")
    time.sleep(1) # Give user the feeling of computations occuring
    
    # Decode message
    decrypted_message = Decode(n, d, encrypted_message)
    print("     Your decrypted message: ", decrypted_message)
    
          
def process_4_crack():
    print(prompts[2])
    print("Ooh, Exciting! Let's see what we can do.")
    
    # Get user input for n and e Public Keys
    n = input("Please enter your intercepted Public Key n: ") # take in as string to check digit count
    e = int(input("Please enter your intercepted Public Key e: "))
    
    # Get user input for message to be decrypted
    encrypted_message = ast.literal_eval(input("Please enter your intercepted encrypted message: "))
    
    print(prompts[2])
    print("Cracking codes...")
    time.sleep(1) # Give user the feeling of computations occuring
        
    # Check if n is larger than 18 digits
        # If so let user know this may take some time 
    if len(n) > 18:
        print("Ah!, that's a big number. This may take some time.")
        print("Please stand by... ")
    
    # Convert n to int for calculations
    n = int(n)
    # Factor n and extract factors p and q
    factored_n = factorize(n)
    p = factored_n[0]
    q = factored_n[1]
    
    # Generate private key d
    d = Find_Private_Key_d(e, p, q)
    print("Code cracked! Decrypting message...")
    time.sleep(1) # Give user the feeling of computations occuring
    
    # Decode message
    decrypted_message = Decode(n, d, encrypted_message)
    print("     Your cracked and decrypted message is: ", decrypted_message)
    
          
def main():
    
    # Initial value to control our user input loop
    running = True
    
    # Initialize output message welcome to user
    display_output = prompts[0]
    
    # Application loop, get user input until running == False
    while running:
        # Welcome user to application
        print(prompts[2])
        print(display_output)
        print(prompts[2])
        
        # Get user choice for process 
        user_input = int(input("Enter your selection: "))
        
        # Check input for choice 
        match user_input:
            case 1:
                display_output = ""
                process_1_generate_keys()
                # Switch output message to inquire about next action
                display_output = prompts[1]
            case 2:
                display_output = ""
                process_2_encode()
                # Switch output message to inquire about next action
                display_output = prompts[1]
            case 3:
                display_output = ""
                process_3_decode()
                # Switch output message to inquire about next action
                display_output = prompts[1]
            case 4:
                display_output = ""
                process_4_crack()
                # Switch output message to inquire about next action
                display_output = prompts[1]
            case 5:
                # Flip running flag ot False to terminate loop and thank user
                running = False
                print(prompts[2])
                print("Thank you! Have a nice day!")
                print(prompts[2])
    

if __name__ == "__main__":
    main()