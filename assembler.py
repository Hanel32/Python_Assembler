# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 16:40:14 2017
@author: Carson
Project 6 for CSCE 312; Computer Organization
Purpose: Parses assembly code, and transfers to bytecode.
"""

#
#TODO:
#  - Create and account for a symbol table for address instructions.
#  - Account for (JUMP) places and gotos.
#  - Fix the string splitting. The dictionaries are good, just confirm that the string split the correct way.

#Allow for command-line arguments to be utilized.
import sys

#Translates the identity
#In order to find this, need to cut off all string items before "=" and after ";"
def identify(line):
  #A-type commands to search for
  #TODO: Just make this a search for "M".
  #      String processing and whatnot not actually necessary, not sure why I didn't see this at first.
  line = line.split(';')[0]       #Everything before ;
  line = line.rpartition('=')[-1] #Everything after  =

  
  if "M" in line:
    return "1"
  return "0"

#Translates jump
#In order to find this, need to cut off all string items _before_the first semicolon.
#TODO: Fix the line splitting
def jump(line):
  jumps = {"JGT" : "001",
           "JEQ" : "010",
           "JGE" : "011",
           "JLT" : "100",
           "JNE" : "101",
           "JLE" : "110",
           "JMP" : "111"}
  line = line.split(';')[-1]       #Everything after ;
  
  for key in jumps.keys():
    if key in line:
      return jumps[key]
  return "000"
    
#Translates dest
#In order to find this, need to cut off all string items beyond '='.
#TODO: Fix the line splitting
def dest(line):
  dests = {"AMD": "111",
           "AM" : "101",
           "AD" : "110",
           "MD" : "011",
           "M"  : "001",
           "D"  : "010",
           "A"  : "100",}
  if "=" not in line:
      return "000"
  
  line = line.split('=')[0]         #Everything before =
  line = line.split(';')[-1]       #Everything after ;
  matches = []
  match   = ""
  
  for key in dests.keys():
    if key in line:
      matches.append(key)
  for m in matches:
      if len(m) > len(match):
          match = m
          
  if len(match) == 0:
      return "000"
  else:
      return dests[match]

#Translates comp
#Same deal as identify with the string splicing, but this module has a dictionary w/ keys
#Idea is to iterate the keys from left to right, with the most basal keys being at the end of
#the options. Obvious design principal, just thought I'd state.
def comp(line):
  comps = {"A-1": "110010","D-1": "001110",
           "D+1": "011111","A+1": "110111",
           "M+1": "110111","D+A": "000010",
           "D+M": "000010","D-A": "010011",
           "D-M": "010011","A-D": "000111",
           "M-D": "000111","D&A": "000000",
           "D&M": "000000","D|A": "010101",
           "D|M": "010101","-1" : "111010",
           "!D" : "001101","!A" : "110001",
           "!M" : "110001","-D" : "001111",
           "-A" : "110011","-M" : "110011",
           "D"  : "001100","A"  : "110000",
           "M"  : "110000","0"  : "101010",
           "1"  : "111111","M-1": "110010"}
  line = line.split(";")[0]
  line = line.rpartition('=')[-1]
  line = "".join(line)
  matches = []
  match   = ""
  
  for key in comps.keys():
    if key in line:
      matches.append(key)
  for m in matches:
      if len(m) > len(match):
          match = m
  if len(match) == 0:
      return "000000"
  else:
      return comps[match]
#Removes comments from the files

def processLine(line):
    kind  = identify(line)
    jumps = jump(line)
    dests = dest(line)
    comps = comp(line)
    return "111" + kind + comps + dests + jumps

#Gets the location of the memory address.
def clean(line):
  #For R0 -> R15 removes R to explicity call the register by its location.
  primitives = [ "R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8",
                 "R9", "R10", "R11", "R12", "R13", "R14", "R15",]
  for p in primitives:
      if p in line:
        line = line.replace("R", "")
  
  if('@' in line):
    line = line.split('@')[-1]       #Removes the @
  if('(' in line):
    line = line.split('(')[-1]       #Removes the left parenthesis
    line = line.split(')')[0]        #Removes right parenthesis and beyond.

  return line

def int2bin(i):
    i = int(i)
    
    if i == 0: return "0000000000000000"
    s = ''
    while i:
        if i & 1 == 1:
            s = "1" + s
        else:
            s = "0" + s
        i /= 2
    while len(s) < 16:
        s = "0" + s
    return s
         

#TODO: If line starts with ( or @, it's an A-instruction. Process differently than D instructions.
#      Create the symbol table with goto for the ( instructions as well as the @ instructions.
def main():
  #Symbol table
  stable = {"0" : "0000000000000000",
            "SP": "0000000000000000",
            "1" : "0000000000000001",
           "LCL": "0000000000000001",
            "2" : "0000000000000010",
           "ARG": "0000000000000010",
            "3" : "0000000000000011",
          "THIS": "0000000000000011",
            "4" : "0000000000000100",
          "THAT": "0000000000000100",
            "5" : "0000000000000101",
            "6" : "0000000000000110",
            "7" : "0000000000000111",
            "8" : "0000000000001000",
            "9" : "0000000000001001",
            "10": "0000000000001010",
            "11": "0000000000001011",
            "12": "0000000000001100",
            "13": "0000000000001101",
            "14": "0000000000001110",
            "15": "0000000000001111",
        "SCREEN": "0100000000000000",
           "KBD": "0110000000000000",
           }
  base   = 16
  inst   = -1

  #Program assembling.
  for program in sys.argv[1:]:
      contents  = []
      unmatched = []
      solo      = []
      f = open(program)
      for line in f:
          line = line.strip("\r")     #Removes all \r
          line = line.strip("\n")     #Removes all \n
          line = line.split("//")[0]  #Removes everything beyond a comment in a line.
          line = line.strip()
          line = "".join(line)

          
          #Builds the symbol table
          if line:
            inst += 1
            if('@' in line or '(' in line):
              location = clean(line)
              #Only add to the symbol table if the location is not there, and the location is not an integer.
              if location not in stable and not location.isdigit():
                #Holding memory location
                if('@' in line):
                  #print "Added to dictionary!"
                  #stable[location] = int2bin(base) #take to binary
                  #base += 1
                  unmatched.append(location)
                #Holding instruction location
                if('(' in line):
                  stable[location] = int2bin(inst)
                  inst -= 1 #take away an event. Non-event.
              else:
                #If it's a digit, assign itself to itself
                if location.isdigit():
                    if location not in stable.keys():
                        stable[location] = int2bin(location)     
      for u in unmatched:
          if u in stable.keys():
            pass
          else:
              solo.append(u)
              stable[u] = int2bin(base)
              base += 1
      f.close()
      f = open(program)
      for line in f:
          line = line.strip("\n")     #Removes all \n
          line = line.split("//")[0]  #Removes everything beyond a comment in a line.
          line = line.strip()
          line = "".join(line)
          if line and '(' not in line:
            if('@' in line): 
              location = clean(line)
              if location in stable.keys():
                contents.append(stable[location]) 
              else:
                pass
            else:
              line = processLine(line)
              contents.append(line)
      f.close()
      program = program.split(".")[0]
      program = program + ".hack"
      f = open(program, 'w')
      for event in contents:
        f.write(event)
        f.write("\n")
      f.close()
      #TODO: implement an output stream. Need to extract file name and turn from asm type to assembled type.
      #Selfnote: Before for splitting is [0], and after is [-1]. Important distinction.
              
              
        
main()
