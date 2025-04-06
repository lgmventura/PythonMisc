#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 00:13:23 2025

@author: luiz
"""

def divisors(n):
    divs = [1]
    for i in range(2,int(n**0.5)+1):
        if n%i == 0:
            divs.extend([i,n/i])
    divs.extend([n])
    return list(set(divs))

def is_prime(n):
    """
    Check if a number is prime.
    
    Parameters:
    n (int): The number to check
    
    Returns:
    bool: True if n is prime, False otherwise
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    # Check divisors up to sqrt(n)
    max_divisor = int(n**0.5) + 1
    for d in range(3, max_divisor, 2):
        if n % d == 0:
            return False
    return True
