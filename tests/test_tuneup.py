"""
Unit test cases for tuneup.py
Students should not modify this file.
"""

__author__ = "madarp"

import sys
import unittest
import subprocess
import importlib
import functools
import timeit
from contextlib import redirect_stdout
from io import StringIO


# suppress __pycache__ and .pyc files
sys.dont_write_bytecode = True

# Kenzie devs: change this to 'soln.tuneup' to test solution
PKG_NAME = 'tuneup'

dup_list = ["1990\tJacob's Ladder", '1990\tThe Two Jakes', '1991\tHouse Party 2', '1992\tThe Distinguished Gentleman', '1994\tBlown Away', '1995\tMoney Train', '1999\tAmerican Pie', '2010\tEat Pray Love', '2014\tBig Hero 6']

def function_timer(func, param):
    """Our own timeit helper function"""
    f = functools.partial(func, param)
    time_cost = timeit.Timer(f).timeit(number=1)
    return time_cost


class TestTuneup(unittest.TestCase):
    """Main test fixture for copyspecial module"""
    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        cls.assertGreaterEqual(cls, sys.version_info[0], 3)
        cls.module = importlib.import_module(PKG_NAME)

    def test_timeit_helper(self):
        """Check if the timeit_helper func is working"""
        func_name = "find_duplicate_movies"
        func_param = "movies.txt"
        actual_t = self.module.timeit_helper(func_name, func_param)
        self.assertIsInstance(
            actual_t, timeit.Timer,
            "timeit_helper() should return the timeit.Timer object instance"
            )
        # Checks if the setup= part is correct    
        self.assertIn(
            f"from {PKG_NAME} import {func_name}", actual_t.src,
            "The timeit.Timer setup is incorrect"
            )
        # Checks if the stmt= part is correct
        self.assertIn(
            f"find_duplicate_movies('movies.txt')", actual_t.src,
            "The timeit.Timer stmt is incorrect"
        )

    def test_profile_decorator(self):
        """Checking the cProfile decorator function"""
        def simple_func():
            pass
        # pass a simple function to see if it gets decorated
        decorated = self.module.profile(simple_func)
        self.assertTrue(
            callable(decorated),
            "The decorator function must return a callable"
            )
        # call the decorated function.  Is it printing any pStats?    
        buffer = StringIO()
        with redirect_stdout(buffer):
            decorated()
        output = buffer.getvalue()
        self.assertIn(
            "Ordered by: cumulative time", output,
            "The cProfile results are not sorted by cumulative time"
        )
        self.assertIn(
            "ncalls  tottime  percall  cumtime  percall filename:lineno(function)", output,
            "The cProfile results are not being printed"
        )

    def test_optimized_find_duplicate_movies(self):
        """Checking the optimized algorithm"""
        opt_result = sorted(self.module.optimized_find_duplicate_movies("movies.txt"))
        self.assertIsInstance(
            opt_result, list,
            "The function is not returning a list"
            )
        self.assertListEqual(
            opt_result, dup_list,
            "The return list is incorrect"
        )

    def test_improvement_factor(self):
        """Checking if improvement is greater than 500x"""
        orig_time = function_timer(self.module.find_duplicate_movies, "movies.txt")
        optimized_time = function_timer(self.module.optimized_find_duplicate_movies, "movies.txt")
        improvement = orig_time / optimized_time
        print(f"Improvement factor is {improvement:.1f}x")
        self.assertGreater(
            improvement, 500.0,
            "The function does not appear to be optimized"
            )

    def test_flake8(self):
        """Checking for PEP8/flake8 compliance"""
        result = subprocess.run(['flake8', self.module.__file__])
        self.assertEqual(result.returncode, 0)
    
    def test_author_string(self):
        """Checking for author string"""
        self.assertIsNotNone(self.module.__author__)
        self.assertNotEqual(
            self.module.__author__, "???",
            "Author string is not completed"
            )
