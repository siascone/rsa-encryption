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

-------------TODO => add sections 3-10--------