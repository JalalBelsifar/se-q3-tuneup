#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tuneup assignment
Use the timeit and cProfile libraries to find bad code.
"""
__author__ = "Jalal, help from John"
import cProfile
import pstats
import timeit
from collections import Counter


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    def wrapper_funct(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        outcome = func(*args, **kwargs)
        pr.disable()
        prof_stats = pstats.Stats(pr).sort_stats('cumulative')
        prof_stats.print_stats()
        return outcome
    return wrapper_funct


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


def optimized_find_duplicate_movies(src):
    movies = read_movies(src)
    movies_counter = Counter(movies)
    duplicates = [movie for movie, v in movies_counter.items() if v > 1]
    return duplicates


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    setup = f"from {__name__} import {func_name}"
    stmt = func_name + "('"+func_param+"')"

    t = timeit.Timer(stmt, setup)
    repeat = 3
    num = 5
    outcome = t.repeat(repeat, num)
    print(outcome)
    average = map(lambda x: x/3, outcome)
    m_list = list(average)
    timing = min(m_list)
    print(f"func={func_name}  num ={num}\
        repeat={repeat} timing={timing:.3f} sec")
    return t


def main():
    """Computes a list of duplicate movie entries."""
    filename = 'movies.txt'
    print("--- Before optimization ---")
    outcome = find_duplicate_movies(filename)
    print(f'Found {len(outcome)} duplicate movies:')
    print('\n'.join(outcome))
    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)
    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)
    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)
    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    main()
    print("Completed.")
