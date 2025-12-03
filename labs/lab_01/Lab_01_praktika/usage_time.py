# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# # %load -y -n -r 14:17 usage_time.py
import functools
import timeit
import typing

# # %load -y -n -s get_usage_time usage_time.py
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
    ndigits : int, optional
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
