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
  aTypes = {"M", "!M", "-M", "M+1", "M-1", "D+M", "D-M", "M-D", "D&M", "D|M"}
  dTypes = {"0", "1", "-1", "D", "A", "!D", "!A", "-D", "-A", "D+1", "A+1",
            "D+A", "D-A", "A-D", "D&A", "D|A"}
  if aTypes in line:
      return 1
  if dTypes in line:
      return 0
  print "Type could not be confirmed. Type set to non-A."
  return 0

#Translates jump
def jump(line):
  
  jumps = {"JGT" : "001",
           "JEQ" : "010",
           "JGE" : "011",
           "JLT" : "100",
           "JNE" : "101",
           "JLE" : "110",
           "JMP" : "111"}
  
  return jump
#Translates dest
def dest(line):
  return dest
#Translates comp
def comp(line):
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
