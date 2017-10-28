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
  if(line[0] == @):
      kind = 

  return kind
#Translates jump
def jump(line):
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