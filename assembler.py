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
  aTypes = {"M",   "!M", 
            "-M",  "M+1", 
            "M-1", "D+M", 
            "D-M", "M-D", 
            "D&M", "D|M"}
  dTypes = {"0",   "1", 
            "-1",  "D", 
            "A",   "!D", 
            "!A",  "-D", 
            "-A",  "D+1", 
            "A+1", "D+A", 
            "D-A", "A-D", 
            "D&A", "D|A"}
  line = line.split(";")[-1]
  line = line.rpartition('=')[-1]
  
  for op in aTypes:
      if op in line:
          return "1"
  if dTypes in line:
      return "0"
  print "Type could not be confirmed. Type set to non-A."
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
  line = line.split(';')[-1]
  for key in jumps.keys():
    if key in line:
      return jumps[key]
  #Note: This is also default for no jump. No worries!:D
  print("No parse key found for jump! Could be no jump...")
  return "000"
    
#Translates dest
#In order to find this, need to cut off all string items beyond '='.
#TODO: Fix the line splitting
def dest(line):
  dests = {"AMD": "111"
           "AM" : "101",
           "AD" : "110",
           "MD" : "011",
           "M"  : "001",
           "D"  : "010",
           "A"  : "100",}
  line = line.split('=')[-1]
  for key in dests.keys():
    if key in line:
      return dests[key]
  print("No parse key found for dest!")
  return "000"
#Translates comp
#Same deal as identify with the string splicing, but this module has a dictionary w/ keys
#Idea is to iterate the keys from left to right, with the most basal keys being at the end of
#the options. Obvious design principal, just thought I'd state.
def comp(line):
  comps = {["D+1"]       : "011111",
           ["A+1", "M+1"]: "110111",
           ["D+A", "D+M"]: "000010",
           ["D-A", "D-M"]: "010011",
           ["A-D", "M-D"]: "000111",
           ["D&A", "D&M"]: "000000",
           ["D|A", "D|M"]: "010101",
           ["-1"]        : "111010",
           ["!D"]        : "001101",
           ["!A", "!M"]  : "110001",
           ["-D"]        : "001111",
           ["-A","-M"]   : "110011",
           ["D"]         : "001100",
           ["A","M"]     : "110000",
           ["0"]         : "101010",
           ["1"]         : "111111",}
  line = line.split(";")[-1]
  line = line.rpartition('=')[-1]
  
  for key in comps.keys():
    if key in line:
      return comps[key]
  print("No parse key found for comp!")
  return "000000"
#Removes comments from the files

def processFile(contents):
  inst = []
  ids  = []
  jump = []
  dest = []
  comp = []
  temp = []
  c    = 0
  for line in contents:
    temp = identify(line)
    ids.append(temp)
    temp = jump(line)
    jump.append(temp)
    temp = dest(line)
    dest.append(temp)
    temp = comp(line)
    comp.append(temp)
    temp = "111" + ids[c] + comp[c] + dest[c] + jump[c]
    inst.append(temp)
    c += 1
  return

def main():
  for program in sys.argv[1:]:
      contents = []
      f = open(program)
      for line in f:
          if(line[0:2] != "//"):  #Checks for the line beginning with a comment.
            line = line.split     #Tokenizes the words
            line = line.strip     #Removes whitespace from the tokenized words.
            contents.append(line)
      f.close()
      contents = processFile(contents)
      
              
              
        
main()
