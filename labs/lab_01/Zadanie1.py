#!/usr/bin/env python
# -*- coding: utf-8 -*-
# +
# 1
import functools
import timeit
import typing

def get_usage_time(
    *, number: int = 1, setup: str = 'pass', ndigits: int = 3
) -> typing.Callable:
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


# +
# 2
import random

N = 6

def vector_generator(n):
    vec = [random.randint(1, 100*N) for i in range(n)]
    return vec
#1.2
def summa_func(n):
    vec = vector_generator(n)
    summ = 0
    for num in vec:
        summ += num
    return summ
#1.3
def proizvedenie_func(n):
    vec = vector_generator(n)
    proizv = 1
    for num in vec:
        proizv *= num
    return proizv
#1.5
def maximum_func(n):
    vec = vector_generator(n)
    maxi = 0
    for num in vec:
        if num >= maxi:
            maxi = num
    return maxi
#1.7
# def srednee_arifm_func(vec):
#     vec = vector_generator(n)
#     summ = 0
#     lenn = 0
#     for num in vec:
#         summ += num
#         lenn += 1
#     return summ/lenn
#1.8
def srednee_garm_func(n):
    vec = vector_generator(n)
    summ = 0
    lenn = 0
    for num in vec:
        summ += num
        lenn += 1
    return lenn/summ


# +
#3
import matplotlib.pyplot as plt

N = 6
    
def five_iteration_summa(n):
    time_of_summa = []
    summa_time = get_usage_time(ndigits=5)(summa_func)
    for i in range(5):
        time_of_summa.append(summa_time(n))
    average_time_summa = sum(time_of_summa)/5
    return average_time_summa

def five_iteration_proizvedenie(n):
    time_of_proizvedenie = []
    proizvedenie_time = get_usage_time(ndigits=5)(proizvedenie_func)
    for i in range(5):
        time_of_proizvedenie.append(proizvedenie_time(n))
    average_time_proizvedenie = sum(time_of_proizvedenie)/5
    return average_time_proizvedenie

def five_iteration_maximum(n):
    time_of_maximum = []
    maximum_time = get_usage_time(ndigits=5)(maximum_func)
    for i in range(5):
        time_of_maximum.append(maximum_time(n))
    average_time_maximum = sum(time_of_maximum)/5
    return average_time_maximum

def five_iteration_srednee(n):
    time_of_srednee = []
    srednee_time = get_usage_time(ndigits=5)(srednee_garm_func)
    for i in range(5):
        time_of_srednee.append(srednee_time(n))
    average_time_srednee = sum(time_of_srednee)/5
    return average_time_srednee
    
# %matplotlib inline

items = range(1, 10**5*N+1, 1000*N)

times_summa = []
times_proizvedenie = []
times_maximum = []
times_srednee = []

j = 0

for i in items:
    times_summa.append(five_iteration_summa(i))
    times_proizvedenie.append(five_iteration_proizvedenie(i))
    times_maximum.append(five_iteration_maximum(i))
    times_srednee.append(five_iteration_srednee(i))
    if i > 1000:
        print('Среднее время произведения для', i, 'элементов:', times_proizvedenie[j])
    j += 1

#Summa
plt.figure(figsize=(10, 6))
plt.plot(items, times_summa)
plt.title('График суммы элементов')
plt.xlabel('Запуски программы')
plt.ylabel('Время, сек')
plt.grid(True)

#Proizvedenie
plt.figure(figsize=(10, 6))
plt.plot(items, times_proizvedenie)
plt.title('График произведения элементов')
plt.xlabel('Запуски программы')
plt.ylabel('Время, сек')
plt.grid(True)

#Maximum
plt.figure(figsize=(10, 6))
plt.plot(items, times_maximum)
plt.title('График максимума из элементов')
plt.xlabel('Запуски программы')
plt.ylabel('Время, сек')
plt.grid(True)

#Srednee
plt.figure(figsize=(10, 6))
plt.plot(items, times_srednee)
plt.title('График среднего гармонического элементов')
plt.xlabel('Запуски программы')
plt.ylabel('Время, сек')
plt.grid(True)
# -

