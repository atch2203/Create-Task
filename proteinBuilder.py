# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 08:39:46 2023

Converts an mRNA or DNA sequence to a polypeptide

Instructions:
    1. Write the mRNA or DNA sequence (with A,T,U,G,C) with no spaces or newlines in sequence1
    2. Run proteinBuilder.py and specify DNA or mRNA
    3. The resulting polypeptide sequence will be printed and a histogram of each amino acid will be displayed
"""

import re
import matplotlib.pyplot as plt
from collections import Counter


sequence = "" #sequence to translate
acids = {} #dictionary corresponding codons to amino acid
polypeptide = []#resulting amino acid sequence

def main():
    isDNA = input("Is sequence1 DNA (Y or N)?")
    if isDNA == "Y":
        load_acids("aminoAcidsDNA")
    else:
        load_acids("aminoAcids")
    sequence = load_sequence("sequence1")
    translate_sequence(sequence)
    print(polypeptide)
    plot()
    
"""
Reads the file located at fileName and returns it

parameters: fileName: str - location of the sequence file
returns: str - sequence read
"""
def load_sequence(file_name):
    with open(file_name) as file:
        sequence = file.readline()
        return sequence

"""
Loads the acids into the acid list variable

parameters: fileName: str - file to read from
returns: None
"""
def load_acids(fileName):
    #populate acids with null dictionaries
    for c0 in "ATUCG":
        acids[c0] = {}
        for c1 in "ATUCG":
            acids[c0][c1] = {}
            for c2 in "ATUCG":
                acids[c0][c1][c2] = "not found"
                
    #read the acids in from aminoAcids    
    #each line is in the from "c1 c2 c3 resulting_amino_acid", where c3 can include multiple/all bases        
    with open(fileName) as file:
        line = file.readline()
        while line != "":
            line = line.split()
            
            if line[2] == '*': #replaces * with all the bases (like a wildcard)
                line[2] = "ATUCG"
                
            for c2 in line[2]:
                acids[line[0]][line[1]][c2] = line[3]
                
            line = file.readline()
    
"""
Gets the corresponding amino acid given the three base sequence

parameters: sequence: str - three character long string containing A, U, C, or G
returns: str - the corresponding amino acid if parameter is correct
                "not found" if the parameter is invalid (eg "AU" or "ACCC" or "BDF")
"""
codon_checker = re.compile("^[ATUCG][ATUCG][ATUCG]$")
def get_amino_acid(sequence):
    if not codon_checker.match(sequence):
        return "not found"
    return acids[sequence[0]][sequence[1]][sequence[2]]

"""
Translates an entire sequence

parameters: sequence: str - complete sequence to translate
returns: list[str] - list of corresponding amino acids, representing a polypeptide
"""
def translate_sequence(sequence):
    while sequence[:3] != "AUG" and sequence[:3] != "TAC" and len(sequence) > 0:
        sequence = sequence[1:]
    while len(sequence) > 2:
        amino_acid = get_amino_acid(sequence[:3])
        polypeptide.append(amino_acid)
        if amino_acid == "stop":
            return polypeptide
        sequence = sequence[3:]
    polypeptide.append("not complete")
    return polypeptide

"""
plots the total number of each amino acid in the sequence

parameters: None
returns: None
"""
def plot():
    totals = Counter(polypeptide)
    for k in totals:
        plt.bar(k, totals[k])
    plt.show()
    
    
if __name__ == "__main__":
    main()
    