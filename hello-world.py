#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 00:32:24 2022

@author: simolamine
"""
print("Hello, World!")
myVar= "Simo LAMINE"
number1 = 1
number2= 5.1
type(myVar)
type(number1)
type(number2)
print(myVar, type(myVar))
print(number1, type(number1))
print(number2, type(number2))
some_friends = """
Anne,
Sophe,
Simo
"""
print(some_friends)
# type(), dir(), help()
type(myVar)
dir(myVar)
myVar.upper()
help(myVar.upper)
monday = 1
tuesday = 1.2
wednesday = 2.5
thursday = 2.5
friday = 3
saturday = 5
sunday = 8

ave = (monday + tuesday + wednesday + thursday + friday +saturday +sunday)/7

print("the average rainfall in mm is", ave.__round__(2))


