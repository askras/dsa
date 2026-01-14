#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Usage Time

Project: TryPython
A collection of educational materials for learning the Python

Author: Alexander Krasnikov aka askras

License: BSD 3 clause
"""

import functools
import timeit
import typing


def get_usage_time(
    *, number: int = 1, setup: str = 'pass', ndigits: int = 3
) -> typing.Callable:
    """Decorator for measuring the speed of the function (in seconds)

    Parameters
    ----------
    number : int, optional
        Number of code repetitions.
    setup : str, optional
        Code executed once before timing.
    ndigits : int, optionalgit status
        Number of decimal places in the returned value.

    Returns
    -------
    decorator: typing.Callable
        Decorator for measuring the time of the function in seconds.

    See Also
    --------
    timeit
        Measure execution time of small code snippets.

    References
    ----------
    [1] timeit documentation : https://docs.python.org/3/library/timeit.html

    Examples
    --------
    Decorating an existing function:

    >>> import time
    >>> def sleep_func(n):
    ...     time.sleep(n)
    ...     return n
    ...
    >>> get_usage_time_sleep_func = get_usage_time()(sleep_func)
    >>> time_sleep_func = get_usage_time_sleep_func(2)
    >>> print(f'The function was executed for {time_sleep_func} seconds')
    The function was executed for 2.0 seconds
    >>> get_usage_time(number=5)(sleep_func)(4)
    4.0

    Measuring the running time of a function for different parameter values:

    >>> import time
    >>> def sleep_func(n):
    ...     time.sleep(n)
    ...     return n
    ...
    >>> for n in range(1,4):
    ...    get_usage_time_sleep_func = get_usage_time(number=2)(sleep_func)
    ...    print(get_usage_time_sleep_func(n))
    1.0
    2.0
    3.0

    Using the `setup` option:

    >>> import time
    >>> def sleep_func(n):
    ...     time.sleep(n)
    ...     return n
    ...
    >>> setup = 'print("Start setup"); time.sleep(10); print("End setup")'
    >>> get_usage_time_sleep_func = get_usage_time(setup=setup)(sleep_func)
    >>> print(get_usage_time_sleep_func(3))
    Start setup
    End setup
    3.0

    Decoding the generated function:

    >>> import time
    >>> @get_usage_time(number=2, setup='print("Start");', ndigits=0)
    ... def sleep_func(n):
    ...    time.sleep(n)
    ...    return n
    ...
    >>> time_sleep_func = sleep_func(3)
    Start
    >>> print(time_sleep_func)
    3.0
    """

    def decorator(func: typing.Callable) -> typing.Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> float:
            usage_time = timeit.timeit(
                lambda: func(*args, **kwargs),
                setup=setup,
                number=number,
            )
            return round(usage_time / number, ndigits)

        return wrapper

    return decorator


if __name__ == '__main__':
    import time

    def sleep_func(n):
        time.sleep(n)
        return n

    for i in range(1, 4):
        time_sleep_func = get_usage_time(number=3)(sleep_func)
        print(time_sleep_func(i))
