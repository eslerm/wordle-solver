#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Wordled - Wordle Solver
Author: Mark Esler
Date: 2022-03-26
"""

import string
import re
import argparse

parser = argparse.ArgumentParser(description="Wordle Sovler")
parser.add_argument(
    "-w",
    type=str,
    default="",
    help="string of the known word\n\tnon alpha characters are wildcards",
)
parser.add_argument(
    "-r",
    type=str,
    default="",
    help="out of sequence known letters\n\toptionally prefix with 0-4 to specify invalid sequence",
)
parser.add_argument("-i", type=str, default="", help="string of invalid characters")

args = parser.parse_args()
w = args.w
r = args.r
i = args.i

with open("five-letter-words.txt") as f:
    five_letter_words = f.read().splitlines()


def wordled(word, required, invalid):
    """
    any word 5 characters or less is accepted
      all non-alpha characters are wild cards
      e.g., '??e' containes the letter 'e' as the thrid character
    required are letters known to be in the solution
      optionally prefix required letters with known invalud positions
      e.g., 's4d' means 's' and 'd' are part of the solution
                  and that 'd' is not the fifth letter
    invalid are characters that are not part of the solution
      e.g., 'axyz' all four chracters are not part of the solution
    """
    if len(word) > 5:
        print("word is too long")
        return
    any_letters = set(string.ascii_lowercase[:26])
    allowed_letters = any_letters.difference(invalid)
    letters = []
    for i in range(5):
        if len(word) > i and word[i].isalpha():
            letters.append(word[i])
            required += word[i]
        else:
            letters.append(allowed_letters)
    required_invalids = re.findall(r"\d*[a-z]{1}", required)
    for l in required_invalids:
        if len(l) == 1:
            break
        for i in l[:-1]:
            if len(letters[int(i)]) > 1:
                letters[int(i)] = letters[int(i)].difference(l[-1])
    required = "".join([i for i in required if i.isalpha()])
    result = []
    for w in five_letter_words:
        approve = True
        for i in range(5):
            if w[i] in letters[i]:
                pass
            else:
                approve = False
                break
        for i in required:
            if i not in w:
                approve = False
        if approve:
            result.append(w)
    return result


def wordledGuess(input, word, required):
    """
    nb: invalid letters do not appear in input
    letters_known is the set of known letters shared by everything in input
    novel_count counts letters that are not yet known
    scores assigns weighted value to letters based on relative abundance
    rank assigns words by summing value of letter scores
    result returns ordered rank keys
    """
    letters_known = set("".join([i for i in word + required if i.isalpha()]))
    novel_count = {x: 0 for x in string.ascii_lowercase[:26]}
    for w in input:
        w_set = set(w).difference(letters_known)
        for ws in w_set:
            novel_count[ws] += 1
    novel_count = sorted(novel_count.items(), key=lambda kv: kv[1], reverse=True)
    scores = {}
    max_score = novel_count[0][1]
    for l in novel_count:
        if l[1] > 0:
            scores[l[0]] = l[1] / max_score
    rank = []
    for w in input:
        w_set = set(w).difference(letters_known)
        i = 0
        for c in w_set:
            i += scores[c]
        rank.append((w, i))
    result = [x[0] for x in sorted(rank, key=lambda kv: kv[1], reverse=True)]
    return result


def wordled(word, required, invalid):
    """
    any word 5 characters or less is accepted
      all non-alpha characters are wild cards
      e.g., '??e' containes the letter 'e' as the thrid character
    required are letters known to be in the solution
      optionally prefix required letters with known invalud positions
      e.g., 's4d' means 's' and 'd' are part of the solution
                  and that 'd' is not the fifth letter
    invalid are characters that are not part of the solution
      e.g., 'axyz' all four chracters are not part of the solution
    """
    if len(word) > 5:
        print("word is too long")
        return
    any_letters = set(string.ascii_lowercase[:26])
    allowed_letters = any_letters.difference(invalid)
    letters = []
    for i in range(5):
        if len(word) > i and word[i].isalpha():
            letters.append(word[i])
            required += word[i]
        else:
            letters.append(allowed_letters)
    required_invalids = re.findall(r"\d*[a-z]{1}", required)
    for l in required_invalids:
        if len(l) == 1:
            break
        for i in l[:-1]:
            if len(letters[int(i)]) > 1:
                letters[int(i)] = letters[int(i)].difference(l[-1])
    required = "".join([i for i in required if i.isalpha()])
    result = []
    for w in five_letter_words:
        approve = True
        for i in range(5):
            if w[i] in letters[i]:
                pass
            else:
                approve = False
                break
        for i in required:
            if i not in w:
                approve = False
        if approve:
            result.append(w)
    return result


def wordledGuess(input, word, required):
    """
    nb: invalid letters do not appear in input
    letters_known is the set of known letters shared by everything in input
    novel_count counts letters that are not yet known
    scores assigns weighted value to letters based on relative abundance
    rank assigns words by summing value of letter scores
    result returns ordered rank keys
    """
    letters_known = set("".join([i for i in word + required if i.isalpha()]))
    novel_count = {x: 0 for x in string.ascii_lowercase[:26]}
    for w in input:
        w_set = set(w).difference(letters_known)
        for ws in w_set:
            novel_count[ws] += 1
    novel_count = sorted(novel_count.items(), key=lambda kv: kv[1], reverse=True)
    scores = {}
    max_score = novel_count[0][1]
    for l in novel_count:
        if l[1] > 0:
            scores[l[0]] = l[1] / max_score
    rank = []
    for w in input:
        w_set = set(w).difference(letters_known)
        i = 0
        for c in w_set:
            i += scores[c]
        rank.append((w, i))
    result = [x[0] for x in sorted(rank, key=lambda kv: kv[1], reverse=True)]
    return result


while True:
    w, i, r = "", "", ""
    while True:
        if w != "" or i != "" or r != "":
            print(wordledGuess(wordled(w, r, i), w, r)[0:10])
        print("press ctrl+c to exit or type 'new' to reset")
        print(f"set word ({w})")
        _w = input()
        if _w == "new":
            break
        elif _w != "":
            w = _w
        print(f"append to required letters ({r})")
        r = r + input()
        print(f"append to invalid letters ({i})")
        i = i + input()
