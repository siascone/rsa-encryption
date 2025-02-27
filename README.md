# rsa-encryption
- This README has been converted from an interactive Jupyter Notebook. Code 
files can be found in the corresponding folders above (TODO). 

Table of contents:
1. Introduction
2. Code Package: FME
3. Code Package: Key Generation using Euclidean Algorithms
4. Code Package: En/Decode Your Message
5. Code Demo
6. Code Exchange
7. Project Narrative
8. Code Breaking
9. Code Breaking Examples
10. Custome Feature

## 1. Introduction: The RSA Encryption Algorithm
---

Welcome! This project is a deep dive into the fundamental components and processes of the RSA encryption pattern. This project aims to provide both a technical understanding and a practical application of RSA encryption by walking through a step-by-step build of the RSA algorithm.  

We begin by developing the foundational tools and components derived from the mathematical principles that make the RSA pattern possible. These tools and components include:
- ***Fast Modular Exponentiation (FME)***
    - An exponentiation pattern that will allow us to efficiently compute the exponentiation of very large numbers for use in both encoding and decoding messages.
- The ***Euclidean Algorithm*** and the ***Extended Euclidean Algorithm (EEA)***
    - Two patterns that will allow us to generate both the Public and Private Key sets necessary for message encoding and decoding.
    - With these we will explore the importance of relatively prime numbers as well as the role Bezout's Coefficients play in the RSA pattern.
- ***Find_Public_Key_e()*** and ***Find_Private_Key_d()***
    - Two methods that will leverage the Euclidean and Extended Euclidean algorithms to generate the necessary keys for encoding and decoding messages.
- ***Convet_Text()*** and ***Convert_Num()***
    - Two methods that will be used to convert text to numbers and numbers to text for use in encoding and decoding messages.
- ***Encode() and Decode()***
    - Two methods that will leverage the above conversion methods, public and private key methods and FME to encode and decode messages.
    
Following this exploration of the RSA algorithm we will demonstrate the RSA workflow through a code demo and example code exchanges that will cover:
- Generating public and private keys with the Euclidean algorithms
- Encoding messages using the generated public key
- Decoding messages securely with the generated private key

After this code demonstration we will explore the development process of this project. Here we will cover various wins and challanges that arose during the development process. 

We will then take a brief glance at the challenges of codebreaking that highlights the strength of the RSA algorithm's resilience against attacks. At first glance, working with relatively small numbers, it may seem an easy pattern to break but we will discover why even a simple approach quickly exposes computational limits to cracking the RSA pattern.

Lastly, this project concludes with an interactive feature that combines all we have discussed above and brings the RSA encryption and decryption cycle to life: a user-friendly tool to generate RAS Keys (public and private), encode and decode messages, as well as, cracking some private codes.

## 2. Code Package FME
---

The first component we will build for our RSA pattern is a ***Fast Modular Exponentiation*** or ***FME*** algorithm that can efficiently compute the exponentiation of large numbers to high powers.

You might be wondering, why do we need this? One of the essential aspects of the RSA pattern is raising numbers (converted text from a message) to a high power and then taking the resulting modulo of that number by an additional large number (don't worry, we'll have some carefully named variables to differentiate between all these different numbers). This process is essential to encrypt or decrypt characters of a message we wish to send securely. 

Without our ***FME*** algorithm, computing the calculations described above would be both time and resource-intensive, especially when considering the significantly large numbers RSA requires for secure encryption. 

It is worth noting that ***FME*** optimizes the exponentiation of large numbers and high powers by breaking down the exponentiation into a series of smaller, modular multiplications. This in turn reduces the number of operations needed to calculate large exponents. 

There are a number of ways that we can effectively code out the ***FME*** algorithm. A couple of approaches employ the use of a binary conversion of a decimal number ***pre-FME*** in order to efficiently calculate the exponentiation. A binary conversion algorithm has been provided below should we wish to take this approach in the future. Alternatively we can perform this calculation in place during the ***FME*** which is the approach taken in the ***FME(b, n, m)*** methode that follows.

### Convert_Binary_String(_int)

The binary to decimal conversion algorithm below works by repeatedly performing the following pattern on an initial integer, which we'll reference as ***n***, until that integer reaches 0:
1. Find the remainder of ***n*** and 2 via modulos (i.e. ***n*** % 2)
2. Add this remainder as the least significant binary bit to the front of a list (i.e. ***bin***)
3. Update ***n*** to the quotient of ***n*** divided by 2 (i.e. ***n // 2)

Once ***n*** reaches 0 return the resulting list as a bit string representing the binary conversion of the original integer.

```python

def Convert_Binary_String(_int):
    """
    Here, you need to define a function that converts an integer to
    a string of its binary expansion. You may or may not need this function. 
    
    For example:
    _int = 345
    bits = 101011001
    """
    
    if _int == 0:
        return '0'
    
    n = _int
    bin_lst = []
        
    while n > 0:
        bit = n % 2
        bin_lst.insert(0, str(bit))
        n = n // 2
    
    bin_str = ''.join(bin_lst)
    
    return bin_str

```

#### Test of the Convert_Binary_String(_int) Function

Below are a series of tests that demonstrate the functionality of our ***Convert_Binary_String()*** function. 
- These test cases can be verified using an outside source binary conversion tool such as [this](https://www.rapidtables.com/convert/number/decimal-to-binary.html) resource from RapidTables.

```python

# Tests for Convert_Binary_String(_int)

print('The conversion of the decimal integer 0 to binary is: ', Convert_Binary_String(0))      # => 0
print('The conversion of the decimal integer 11 to binary is: ', Convert_Binary_String(11))    # => 1011
print('The conversion of the decimal integer 243 to binary is: ', Convert_Binary_String(234))  # => 11101010
print('The conversion of the decimal integer 345 to binary is: ', Convert_Binary_String(345))  # => 101011001

```

The conversion of the decimal integer 0 to binary is:  0
The conversion of the decimal integer 11 to binary is:  1011
The conversion of the decimal integer 243 to binary is:  11101010
The conversion of the decimal integer 345 to binary is:  101011001

### FME(b, n, m)

The FME algorithm below works by taking in a base, ***b***, an exponent, ***n***, and a modulo integer, ***m***. 

The algorithm tracks both a ***result*** variable and a ***square** variable that will be updated and leveraged as the main loop of the algorithm executes.

During the execution of the main loop of the algorithm, until the exponent, ***n***, reaches 0 we perform the following pattern:
1. extract the least significant bit of the binary expansion of our exponent (i.e. 2^0, 2^1... and so on until ***n*** reaches 2).
2. If this bit is 1, update the ***result*** variable by multiplying the ***result*** and ***square*** variables then taking the modulus of that value by ***m***.
3. Update the ***square*** value by taking the modulus ***m*** of the current value of ***square*** times ***square***.
4. Update ***n*** to be the quotient of ***n*** divided by 2.

* You may notice the binary conversion pattern from above within the loop of our FME algorithm.

After the loop completes we return the result variable as the calculated exponentiation. 

#### Core mathematical Principles at work:
- Modular Arithmetic
- Binary expansion of an Exponent
- Square and Mod Pattern


Note that in the RSA pattern, ***m*** is a member of both our public and private keys. We will discuss this number and its significance in greater detail in the section that follows.

```python
def FME(b, n, m):
    """
    1. Using the fast modular exponentiation algorithm,
    the below function should return b**n mod m.
    As described on page 254. (however, you may input the exponent and 
    then convert it to a string - the book version imports the binary expansion)  
    2. You should use the function defined above Convert_Binary_String() if using the book algorithm.
    3. For this block you MUST use one of the 3 methods above.
    4. Any method using bit-shifting or copied from the internet (even changing varibale names) will result in a 0.
    
    **If you are completely stuck, you may use pow() with a 10pt penalty.**

    You may use the function you developed in your Mastery Workbook - but be sure it is your own
    work, commented, etc. and change inputs as needed.
    """  
    
    #NOTE: Based on Sriram's Algorithm from Lecture and MW
    
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

```

#### Test of the FME(b, n, m) Function

Below are a series of tests that demonstrate the functionality and efficiency of our ***FME()*** function. 

You may be wondering about the significance of the numbers in the test cases. These numbers have been chosen as a preview of how we can use FME to encrypt and decrypt a message. 

In the test cases below we have the two numbers ***1914*** and ***520***. These numbers represent the conversion of a cluster of letters to their numerical representations.
- Conversion Scheme:
    - ***A-Z*** translates ***00-25***, ***a-z*** translates to ***26-51***
- ***1914*** translates to ***19*** and ***14*** which in turn represents ***T*** and ***O***, i.e. ***TO***
- ***520*** translates to ***05*** and ***20*** which in turn represents ***F*** and ***U***, i.e. ***FU***
- Our encoded and decoded test message is ***TOFU***

The first two tests encode our ***TOFU*** message by raising their numerical translations to the power of ***13*** and taking the modulus of that number by ***2537*** to produce the resulting integers ***2367*** and ***2247***.
- If you're thinking that ***13*** and ***2367*** also have significance you would be correct.
- These numbers have specific relationships to each other and to two specific prime numbers that were used to generate them.
    - We will explore these relationships in the following section as we study the importance of the ***Euclidean Algorithm***, ***Bezout's Coefficients (i.e. modular inverses)*** and the generation of ***public and private keys*** for encoding and decoding messages.
    - For now the key relationship to know is that ***13*** and ***2537*** are ***relatively prime*** to each other; namely their Greatest Common Divisor is 1.
    
The second two test cases decode our encoded ***TOFU*** message back its original numerical translation; demonstrating that we can leverage our ***FME()*** function in both directions (i.e. to encrypt and decrypt).
- You will notice that our modulus of ***2537*** remains unchanged but the exponent we are raising our encoded message to has changed from ***13*** to ***937***.
- ***937*** is a ***Modular Inverse*** of ***13 mod 2537***. This modular inverse will allow us to convert our encoded message back to its original form.
    - In the following section we will discuss the importance of, as well as the how behind, the "magic" of this modular inverse.

NOTE:
- In these examples we have grouped letters together. We will learn later on that this is a method to help protect against pattern recognition and frequency analysis that can be used to break the RSA algorithm.

```python

# Tests for FME(b, n, m)

print('The FME of 1914^13 mod 2537 is: ', FME(1914, 13, 2537))   # 1914 => 2367
print('The FME of 520^13 mod 2537 is: ', FME(520, 13, 2537))     # 0520 => 2247
print('The FME of 2367^937 mod 2537 is: ', FME(2367, 937, 2537)) # 2367 => 1914
print('The FME of 2247^937 mod 2537 is: ', FME(2247, 937, 2537)) # 2247 => 0520

```

The FME of 1914^13 mod 2537 is:  2367
The FME of 520^13 mod 2537 is:  2247
The FME of 2367^937 mod 2537 is:  1914
The FME of 2247^937 mod 2537 is:  520

## 3. Code Package: Key Generation using Euclidean Algorithms
---

The next series of components that we will build for our RSA pattern are:
- ***The Euclidean Algorithm***
- ***The Extended Euclidean Algorithm***
- ***Find_Public_Key_e(p, q)***
- ***Find_Private_Key_d(e, p, q)***

Let's explore each one individually.

### The Euclidean Algorithm

The Euclidean Algorithm calculates the Greatest Common Divisor, ***GCD***, of two numbers, ***a*** and ***b***. 
- The algorithm does this by repeatedly calculating ***k*** = ***a mod b***, setting ***a*** to the value of ***b*** and ***b*** to the value of ***k*** until ***b*** equals 0. 
    - Once ***b*** equals 0 there are no more remainders to calculate and we have found the greatest common divisor of ***a*** and ***b***
    
In the RSA pattern we use a pairing of Public and Private Keys for encoding and decoding our messages. These keys are comprised of:
- ***Public Key (n, e)***
    - ***n*** is the product of two primes ***p*** and ***q***.
    - ***e*** is a number that is relatively prime to the product of ***(p-1)(q-1)***.
- ***Private Key (n, d)***
    - ***n*** is the same ***n*** as above.
    - ***d*** is the modular inverse of ***e mod n***.
    
So what does this mean for the Euclidean Algorithm and the RSA pattern? 
- As we have noted above ***e*** and ***(p-1)(q-1)*** must be ***relatively prime*** to one another.
- And from section 2 we learned that ***relatively prime*** means two numbers have a ***GCD*** of 1.
- So, in calculating the ***e*** of our Public Key we will using the Euclidean Algorithm to verify that an ***e*** we are looking to use is ***relatively prime*** to a ***(p-1)(q-1)*** generated by our chosen ***p*** and ***q***.

In the below implementation of the Euclidean Algorithm we have two additions to the above mentioned pattern:
1. We first check to see if either of our inputs, ***a*** or ***b***, are negative and if so raise an error.
    - We want to ensure that our inputs and outputs are positive.
2. For ease of calculating the ***GCD*** of ***a*** and ***b*** we make sure that ***a*** is always larger than ***b***.
    - Note that we are using the variable placeholders ***_a*** and ***_b*** to preserve the original input values.
        - This is not strictly necessary for our needs but is a good practice for future proofing our work should we revisit this method and decide to use the original inputs in additional calculations.

```python

def Euclidean_Alg(a, b):
    """
    1. Calculate the Greatest Common Divisor of a and b.
    
    2. This version should have only positive inputs and outputs.
    
    3. The function must return a single integer ('x') which is
    the gcd of a and b.
    
    
    """
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

```

#### Test of the Euclidean_Alg(a, b) Function

Below are a series of tests that demonstrate the functionality of our ***Euclidean_Alg()*** function. 
- The last two test cases check for the expected raised error, should a negative integer be imputed for ***a*** or ***b***
    - These are commented out to prevent any disruption of the rest of the notebook
    - Should you wish to test them simply uncomment them one at a time and rerun the cell
        - Be sure to comment them back out after you complete your testing

```python

# Tests for Euclidean_Alg(a, b)

print("The GCD of 91 and 26 is: ", Euclidean_Alg(91, 26))             # => 13
print("The GCD of 356 and 252 is: ", Euclidean_Alg(356, 252))         # => 4
print("The GCD of 144 and 89 is: ", Euclidean_Alg(144, 89))           # => 1
print("The GCD of 100001 and 1001 is: ", Euclidean_Alg(100001, 1001)) # => 11
print("The GCD of 1001 and 100001 is: ", Euclidean_Alg(1001, 100001)) # => 11, testing swap of inputs
# print("The GCD of -122 and 90 is: ", Euclidean_Alg(-122, 90))         # => error, "Inputs must be positive integers." --> can't have negative a
# print("The GCD of 901 and -233 is: ", Euclidean_Alg(901, -233))       # => error, "Inputs must be positive integers." --> can't have negative b

```

The GCD of 91 and 26 is:  13
The GCD of 356 and 252 is:  4
The GCD of 144 and 89 is:  1
The GCD of 100001 and 1001 is:  11
The GCD of 1001 and 100001 is:  11

### The Extended Euclidean Algorithm, EEA

The Extended Euclidean Algorithm operates on the same principles as the Euclidean Algorithm and additionally incorporates Bezout's Theorem of GCDs as Linear Combinations.
- Bezout's Theorem: If ***a*** and ***b*** are positive integers, then there exist integers ***s*** and ***t*** such that ***GCD(a, b) = sa + tb***.
    - ***GCD(a, b)***, also known as Bezout's Identity, is our ***Euclidean_Alg(a, b)***.
    - ***s*** and ***t*** are called Bezout's Coefficients of ***a*** and ***b***.
        - These coefficients will come in handy as they represent the modular inverses of ***a mod m*** and ***b mod m***.
        - If you recall from section 2, in order to decode a message, we need the modular inverse of the exponent used to encode a message.
        - This modular inverse (i.e. Bezout's Coefficient), will become the ***d*** in our ***Private Key (n, d)*** pair noted above.
- It is worth noting that from our implementation below, while our output includes both ***s*** and ***t*** coefficients in addition to the ***GCD*** of ***a*** and ***b***, we will only need one of the two coefficients, ***t***, for use in our RSA pattern.
    - As noted above, our use case for EEA in the RSA pattern is to calculate the modular inverse of ***e*** from our ***Public Key (n, e)*** pair.
    - Our ***EEA(a, b)*** algorithm ensures the smaller input value is always ***b*** and we input ***e*** for ***b*** in the execution of ***EEA(a, b)***.
        - ***t*** ends up being the coefficient that corresponds to ***e*** in our calculations.
- As with our implementation of the Euclidean Algorithm, our EEA(a, b) algorithm also uses placeholder variables ***_a*** and ***_b*** to preserve the original input values.

```python

def EEA(a, b):
    """
    This is a helper function utilizing Bezout's theorem as discussed in your MW.
    You will follow these same steps closely to construct this function.
    
    This version will return both: 
    1. the GCD of a, b 
    2. Bezout's coefficients in any form you wish. We recommend returning your coefficients as a list or a tuple. 
    HINT: return GCD, (s1, t1)
    
    * Ensure that your inputs are positive integers. Implement these kinds of checks.
    * It might also behoove you to consider reassigning a, b to new coefficients depending on which is greater.
    
    """
    
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

```

#### Test of the EEA(a, b) Function

Below are a series of tests that demonstrate the functionality of our ***EEA()*** function. 
- These tests use the same values as the tests for our ***Euclidean_Alg()*** function and should produce the same GCDs in addition to the corresponding Bezout Coefficients, ***s*** and ***t***
- As with our ***Euclidean_Alg()*** function the last two test cases test for expected error when either input is negative
    - Comment each test in, one at a time, to verify
        - Be sure to comment the test cases back out once complete

```python

# Tests for EEA(a, b)

print("The GCD and Bezout Coefficients of 91 and 26 are: ", EEA(91, 26)) # => [13, (1, -3)]
print("The GCD and Bezout Coefficients of 356 and 252 are: ", EEA(356, 252)) # => [4, (17, -24)]
print("The GCD and Bezout Coefficients of 144 and 89 are: ", EEA(144, 89)) # => [1, (34, -55)]
print("The GCD and Bezout Coefficients of 43 and 59 are: ", EEA(43, 59)) # => [1, (-8, 11)]
print("The GCD and Bezout Coefficients of 100001 and 1001 are: ", EEA(100001, 1001)) # => [11, (10, -999)]
print("The GCD and Bezout Coefficients of 1001 and 100001 are: ", EEA(1001, 100001)) # => [11, (10, -999)] swap values from above, should have same output    
# print("The GCD and Bezout Coefficients of -122 and 90 are: ", EEA(-122, 90)) # => error, "Inputs must be positive integers." --> can't have negative a
# print("The GCD and Bezout Coefficients of 901 and -233 are: ", EEA(901, -233)) # => error, "Inputs must be positive integers." --> can't have negative b

```

The GCD and Bezout Coefficients of 91 and 26 are:  [13, (1, -3)]
The GCD and Bezout Coefficients of 356 and 252 are:  [4, (17, -24)]
The GCD and Bezout Coefficients of 144 and 89 are:  [1, (34, -55)]
The GCD and Bezout Coefficients of 43 and 59 are:  [1, (-8, 11)]
The GCD and Bezout Coefficients of 100001 and 1001 are:  [11, (10, -999)]
The GCD and Bezout Coefficients of 1001 and 100001 are:  [11, (10, -999)]

### The Find_Public_Key_e(p, q) function

With the ***Find_Public_Key_e(p, q)*** function we are going to generate the ***Public Key (n, e)*** that will later be used in conjunction with our ***FME()*** function to encode a message

Our Public Key, as noted in our discussion of the Euclidean Algorithm above, requires 2 values:
- ***n***, the product of two different prime numbers, ***p*** and ***q***.
- ***e***, an integer that is ***relatively prime*** to ***(p-1)(q-1)***.
    - i.e. ***GCD((p-1)(q-1), e) = 1***.
    
In the implementation below:
- We begin by calculating ***n*** as the product of ***p*** and ***q***, as well as ***pq_dec*** as the product of ***(p-1)*** and ***(q-1)***.
    - ***pq_dec*** = the product of both ***p*** ***dec***remented and ***q*** ***dec***remented.
- We then set out to find an ***e*** that is ***relatively prime*** to ***pq_dec*** using a relatively simple approach.
    - To achieve this we begin with ***e*** set to the integer 2.
        - Skipping 1, as 1 is a factor of all positive integers.
    - We then use our ***Euclidean_Alg(a, b)*** to check if ***2*** and ***pq_dec*** are relatively prime (i.e. ***Euclidean_Alg(pq_dec, 2) = 1***).
        - If ***2 is NOT relatively prime*** to ***pq_dec*** then we increment ***e*** by 1 and check again (***e*** is now 3).
        - If ***2 is relatively prime*** to ***pq_dec*** then we have a valid ***e*** for our ***Public Key (n, e)***.
        - Note: if at any point ***e*** is equal to either ***p*** or ***q*** we increment ***e*** and skip the current iteration of our loop moving on to the next iteration.
            - This is a security measure to ensure that neither the ***p*** nor ***q*** used to generate our keys is exposed as the ***e*** value of our ***Public Key (n, e)***
- We then return the ***Public Key (n, e)*** pair.

```python

def Find_Public_Key_e(p, q):
    """
    Implement this function such that
    it takes 2 primes p and q.
    
    Use the gcd function that you have 
    defined before.
    
    The function should return 2 elements as follows:
    public key: n
    public key: e
    
    HINT: this function will run a loop to find e such 
    that e is relatively prime to (p - 1) (q - 1) 
    and not equal to p or q.
    
    NOTE: There are a number of ways to implement this key feature. 
    You, as the coder, can choose to how to acheive this goal.
    
    """

    # TODO: Future improvement, prime check of p and q, raise error if not prime. 
    #       Need to consider very large primes and cost of computation
    #       Helper function or existing library?
    
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
        

```

#### Test for the Find_Public_Key_e(p, q) function

The below test uses the primes 53 and 23 for ***p*** and ***q***

```python

# Tests for Find_Public_Key_e(p, q)

print("The Public Key (n, e) generated by 53 and 23 is: ", Find_Public_Key_e(53, 23))

```

The Public Key (n, e) generated by 53 and 23 is:  (1219, 3)

Awesome, now that we have a ***Public Key (1219, 3)*** let's see about finding the corresponding ***Private Key (1219, d)***.

### The Find_Private_Key_d(e, p, q) function

For our corresponding ***Private Key (n, d)*** we need two components:
- ***n*** as the product of ***p*** and ***q***.
    - We are already calculating ***n*** in our ***Find_Public_Key_e(p, q)*** function so we don't need to recalculated that value here.
- ***d*** the ***modular inverse*** of ***e mod (p - 1)(q - 1)***.
    - Recall from section 1 that ***e***, our exponent, is used to raise our numerical message before it is modded by ***n*** to generate a numerical encoding.
    - We want to be able to to turn this encoding back into the original numerical message.
    - Leveraging Modular Congruences and the Theorem of Modular Inverses we can guarantee that the ***FME*** of our encoded message raised to the modular inverse of ***e*** modded by ***n*** will result in our original numerical message.
    - What we know about modular inverses?
        - The modular inverse of ***e mod f*** is equal to ***d*** in ***ed mod f = 1***.
    - What we can do with this?
        - let ***x*** be some positive integer, and let ***r = x^e mod f***. As a result of the rules of modular inverses we can say that ***x = r^d mod f***.

In the implementation below:
- We begin by finding ***pq_dec*** just as we did before.
    - ***pq_dec = (p-1)(q-1)***.
- We then use our ***EEA()*** function to calculate the GCD and Bezout Coefficients of ***pq_dec*** and ***e*** from our ***Public Key (n, e)***.
- From here in order to complete the modular inverse calculation for ***e*** we take the modulus of the Bezout Coefficient of ***e*** by ***pq_dec***.
    - We run this final modulus to ensure that the modular inverse we end up with is a positive integer as we will be using this number as an exponent. 
        - If this exponent is negative we will get some unpredictable side effects and an incorrect output due to the fact that we'll no longer be working with whole numbers.
    - The reason this will work is due to our modular arithmetic rules regarding left side values less than the modulus.
        - If the Bezout Coefficient of ***e*** is positive and less than the modulous then the coefficient will be returned as the modular inverse. 
            - A smaller left side will always be the result when modded by a larger modulus (i.e. if n < m, then n mod m = n).
        - If the Bezout Coefficient of ***e*** is negative then taking the modulus of the negative coefficient will result in the corresponding positive modular inverse.
            - With a negative right side we use the following formula, -n mod m = m - (n mod m).
            - Note: another way to look at this is to add the modulus to the negative coefficient until the coefficient is positive.

***We now have everything we need to generate our Public Key (n, e) and Private Key (n, d). We're pretty much ready to start encoding and decoding messages!***

```python

def Find_Private_Key_d(e, p, q):
    """
    Implement this function to find the decryption exponent d, 
    such that d is the modular inverse of e. 
    
    This will use the Extended Euclidean Algorithm
    
    This function should return the following:
    d: the decryption component.
    
    This is not a single action, and there are multiple methods to create this. 
    
    You may create a helper function or have all code within this function.
    
    Plan ahead before coding this.

    """
    
    # We need to find inverse of e mod (p - 1)(q - 1)
    
    pq_dec = (p - 1) * (q - 1)
    
    # EEA returns gcd and tuple of Bezout's coeffs. We need the second coeff in the tupple
    bz_coef = EEA(pq_dec, e)[1][1] # Bezout's coef for e
   
    # to calculate the modular inverse of e we need to take the modulous of bz_coef and pq_dec
    d = bz_coef % pq_dec 
   
    return d

```

#### Test For Find_Private_Key_d(e, p, q)

In order to test our ***Find_Private_Key_d(e, p, q)*** function we are going to need to run our ***Find_Public_Key_e(p, q)*** function as ***e*** is a required input for finding ***d***

Let's go ahead and output our Public and Private Keys accordingly. 
- We'll use the same ***p*** and ***q*** as we did for our test of ***Find_Public_Key_e(53, 23)***

```python

# Tests for Find_Private_Key_d(e, p, q)

# Set p and q variables of 53 and 23
p = 53
q = 23

# Get public key (n, e)
public_key = Find_Public_Key_e(53, 23)

# Extract n and e
n = public_key[0]
e = public_key[1]

# Get private key d
d = Find_Private_Key_d(e, 53, 23)


print('Public and Private key values generated by the primes p = 53 and q = 23') 
print('-----------------------------------------------------------------------')
print('Public and Private Key n: ', n) # 1219
print('Public Key e: ', e)             # 3
print('Private Key d:', d)             # 763

```

Public and Private key values generated by the primes p = 53 and q = 23
-----------------------------------------------------------------------
Public and Private Key n:  1219
Public Key e:  3
Private Key d: 763

-------------TODO => add sections 4-10--------