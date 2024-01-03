#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from functools import update_wrapper, wraps

count = {}

def disable():
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    return


def decorator():
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    return


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''

    # count[func.__name__] = 0
    count = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        # count[func.__name__] += 1
        # print(count[func.__name__])
        count[func] = count.get(func, 0) + 1
        # wrapper.count += 1
        print(f'Функция {func.__name__} вызвана {count[func]} раз ')
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper


def memo():
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    return


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    def wrapper(*args):
        # print('n_ary')
        value = args[0]
        for i in args[1:]:
            value = func(value, i)
        return value
    return wrapper


def trace():
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    return


# @memo
@n_ary
@countcalls
def foo(a, b):
    return a + b


# @countcalls
# @memo
# @n_ary
# def bar(a, b):
#     return a * b
#
#
# @countcalls
# @trace("####")
# @memo
# def fib(n):
#     """Some doc"""
#     return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    # main()
    print(foo(2, 3, 4))
