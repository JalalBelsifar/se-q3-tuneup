<img height="120px" src="img/sluggish.jpg" />

# Tuneup Time
In this project, you will tune up some code that is not performing well. By "not performing" we mean that it's terribly inefficient at what it is trying to do: Eliminating duplicate entries in a list of popular movie titles. Although the code is bad, it's representative of what you might encounter in the Real World&#8482;.

## Objectives
- Hands-on experience with the `timeit` module
- Hands-on experience with `cProfile`
- Writing a decorator function
- Using profile results to enhance performance

There is a lot of material wrapped up in this seemingly sparse exercise. You are not expected to know how to use all of these tools and modules as you engage in this exercise. The important part is that you know where to look to begin figuring it out. Remember the objective is to use the profiling tools rather than rushing in to just fix the code because you can visually see why it's broken.

## Part A
The goal here is to isolate and run the `find_duplicate_movies` function multiple times, and figure out the time cost of running the function once.

The `find_duplicate_movies` function runs as-is, out of the box &mdash; but not well. As part of its "batteries included" philosophy, Python has a module named [`timeit`](https://docs.python.org/3/library/timeit.html#module-timeit) that allows rudimentary timing of small code snippets. Please review the documentation on this standard library module.

For the first part of this assignment, complete the `timeit_helper` function. Use the [`timeit.Timer.repeat`](https://docs.python.org/3/library/timeit.html#timeit.Timer.repeat) convenience function to measure the total amount of CPU time required to run the `find_duplicate_movies` function of the program before you optimize it. Use the `timeit` module within your code as opposed to the command line version. You will need to `import timeit` to do this. After you have collected the cumulative timing results, use basic math to calculate the time cost of a single run of the function.  Print your results to the console in a format like this
      "Fastest time across 7 repeats of 5 runs per repeat: {best_time} sec"

When profiling a function using `timeit`, the best practice is to take the "minimum of the average" of several measurements of execution time.
 - The `timeit.Timer.repeat` method returns a list of floating point numbers that represents the TOTAL number of CPU seconds consumed over multiple runs of your function.  Each float represents a single 'repeat'.  A repeat is an accumulation of runs.
 - If you set `number=10` when using `timeit.Timer.repeat`, you'll need to divide each float in the list reading by 10. This will give you the average time cost for that run.
 - If you set `repeat=3` when using `timeit.TImer.repeat`, you will get a list of 3 resulting cumulative time readings.

The timeit interface can be a bit confusing to use from within a program, so here are some tips.
 - Create a `timeit.Timer()` object and assign it the name `t`. You'll need to supply the `stmt=` and `setup=` parameters when creating `t`.  The setup statement is from the perspective of an outside process that wants to run your function.  Typically this involves some kind of import statement so a function name can be found for example "from XXXXXXX import YYYYYYY"
 - Create two control variables named runs_per_repeat=5 and num_repeats=3.
 - Using your `t` object, call its `repeat()` method and supply the `repeat=` and `number=` parameters. For example, `result = t.repeat(repeat=num_repeats, number=runs_per_repeat)`
 - `result` will be a list (or "vector") of 5 floating point numbers. Each float represents the cumulative time required to run the function 3 times.
 - To condense into a single numerical result, compute the average of each group of three, and take the minimum of those 5 averages.

There is a reason for using the minimum of the averages. The fastest time represents the best an algorithm can perform when the caches are loaded and the system isn't busy with other tasks (e.g. Garbage Collection). All the timings are "*noisy*" &mdash; the fastest time is the least noisy. It is easy to show that the fastest timings are the most reproducible and, therefore, the most useful when timing different implementations of an algorithm.

Your timing measurement should have an output message that looks like this:
```
func=find_duplicate_movies  num_repeats=5 runs_per_repeat=3 time_cost=0.491 sec
```

## Part B
Complete the missing decorator function to create a profiler which can be used to "decorate" any function and profile its CPU performance to expose bottlenecks.
 - Create a `cProfile()` object inside the decorator's inner function
 - Enable the `cProfile()` object to start its timers
 - Invoke the original function, passing all args and kwargs to the original function
 - Disable the `cProfile()` object after the original function returns
 - Use the `pstats` module to create a `Stats` object which will collect statistics from the `cProfile` object
 - Sort the stats by 'cumulative' time so you can see which functions are costing the most time
 - Use the `Stats` object's `print_stats()` method to print the statistics
 - Restrict the stats output to show only the first 10 rows.


## Part C
Once you are satisfied with your decorator, apply it to the `find_duplicate_movies()` function to see where the most time is being spent. Use your knowlege of Python and reasoning powers to devise better algorithm for finding duplicates.  Note that we are not asking for a "case-insensitive" algorithm.  You can be assured that if there are duplicates, their casing will be identical.

## Expected Output
```
python soln/tuneup.py

--- Before optimization ---
Reading file: movies.txt
Found 9 duplicate movies:
1990    The Two Jakes
1990    Jacob's Ladder
1991    House Party 2
1992    The Distinguished Gentleman
1994    Blown Away
1995    Money Train
1999    American Pie
2010    Eat Pray Love
2014    Big Hero 6

--- Timeit results, before optimization ---
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
func=find_duplicate_movies  num_repeats=5 runs_per_repeat=3 time_cost=0.491 sec

--- Timeit results, after optimization ---
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
Reading file: movies.txt
func=optimized_find_duplicate_movies  num_repeats=5 runs_per_repeat=3 time_cost=0.001 sec

--- cProfile results, before optimization ---
Reading file: movies.txt
         6808576 function calls in 1.268 seconds

   Ordered by: cumulative time
   List reduced from 17 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.002    0.002    1.268    1.268 tuneup.py:54(find_duplicate_movies)
     2609    0.720    0.000    1.266    0.000 tuneup.py:44(is_duplicate)
  6803336    0.547    0.000    0.547    0.000 {method 'lower' of 'str' objects}
     2609    0.000    0.000    0.000    0.000 {method 'pop' of 'list' objects}
        1    0.000    0.000    0.000    0.000 tuneup.py:37(read_movies)
        1    0.000    0.000    0.000    0.000 {method 'splitlines' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        1    0.000    0.000    0.000    0.000 {method 'read' of '_io.TextIOWrapper' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}



--- cProfile results, after optimization ---
Reading file: movies.txt
         20 function calls in 0.001 seconds

   Ordered by: cumulative time
   List reduced from 20 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.001    0.001 tuneup.py:65(optimized_find_duplicate_movies)
        1    0.000    0.000    0.000    0.000 tuneup.py:37(read_movies)
        1    0.000    0.000    0.000    0.000 __init__.py:540(__init__)
        1    0.000    0.000    0.000    0.000 __init__.py:608(update)
        1    0.000    0.000    0.000    0.000 {built-in method _collections._count_elements}
        1    0.000    0.000    0.000    0.000 tuneup.py:70(<listcomp>)
        1    0.000    0.000    0.000    0.000 {method 'splitlines' of 'str' objects}
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        1    0.000    0.000    0.000    0.000 {method 'read' of '_io.TextIOWrapper' objects}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}


Completed.
```

You should be able to achieve at least a 670x improvement in the performance of `find_duplicate_movies()`.


## Submitting your work
To submit your solution for grading, you will need to create a github [Pull Request (PR)](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).  Refer to the `PR Workflow` article in your course content for details.