# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 16:40:14 2017

@author: Carson

Project 6 for CSCE 312; Computer Organization
Purpose: Parses assembly code, and transfers to bytecode.
"""

#Allow for command-line arguments to be utilized.
import sys

#Translates the identity
def identify(line):
  aTypes = {"M", "!M", 
            "-M", "M+1", 
            "M-1", "D+M", 
            "D-M", "M-D", 
            "D&M", "D|M"}
  dTypes = {"0", "1", 
            "-1", "D", 
            "A", "!D", 
            "!A", "-D", 
            "-A", "D+1", 
            "A+1", "D+A", 
            "D-A", "A-D", 
            "D&A", "D|A"}
  for op in aTypes:
      if op in line:
          return 1
  if dTypes in line:
      return 0
  print "Type could not be confirmed. Type set to non-A."
  return 0

#Translates jump
#In order to find this, need to cut off all string items beyond the first semicolon.
def jump(line):
  jumps = {"JGT" : "001",
           "JEQ" : "010",
           "JGE" : "011",
           "JLT" : "100",
           "JNE" : "101",
           "JLE" : "110",
           "JMP" : "111"}
  line = line.split(";")[0]
  
  return jump
#Translates dest
def dest(line):
  dests = {"M"  : "001",
           "D"  : "010",
           "MD" : "011",
           "A"  : "100",
           "AM" : "101",
           "AD" : "110",
           "AMD": "111"}
  return dest
#Translates comp
def comp(line):
  comps = {["0"]         : "101010",
           ["1"]         : "111111",
           ["-1"]        : "111010",
           ["D"]         : "001100",
           ["A","M"]     : "110000",
           ["!D"]        : "001101",
           ["!A", "!M"]  : "110001",
           ["-D"]        : "001111",
           ["-A","-M"]   : "110011",
           ["D+1"]       : "011111",
           ["A+1", "M+1"]: "110111",
           ["D+A", "D+M"]: "000010",
           ["D-A", "D-M"]: "010011",
           ["A-D", "M-D"]: "000111",
           ["D&A", "D&M"]: "000000",
           ["D|A", "D|M"]: "010101"}
  return comp
#Removes comments from the files
def processFile(contents):
  ids  = []
  jump = []
  dest = []
  comp = []
  temp = []
  for line in contents:
    temp = identify(line)
    ids.append(temp)
    temp = jump(line)
    jump.append(temp)
    temp = dest(line)
    dest.append(temp)
    temp = comp(line)
    comp.append(line)
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
