---
layout: page
title: Arithmetic of function fields
description: >
  We study the arithmetic of function fields, which are the function fields of curves over finite fields. This is a very active area of research that has many connections to other fields, such as coding theory, cryptography, and algebraic geometry. We are interested in the study of $\\zeta$-functions, $L$-functions, and the distribution of primes in function fields.
---

## Function Fields

### Basic Setup
A function field over a finite field $\mathbb{F}_q$ is the field of rational functions on a smooth projective curve $C$ over $\mathbb{F}_q$. The most basic example is $\mathbb{F}_q(t)$, the field of rational functions in one variable.

### Zeta Functions
The zeta function of a function field $K/\mathbb{F}_q$ is defined as:

$$Z_K(s) = \prod_{P} \frac{1}{1 - q^{-s \deg(P)}}$$

where the product runs over all places $P$ of $K$. This function has a functional equation and satisfies the Riemann hypothesis (proved by Weil).

### L-Functions
For a character $\chi$ of the idele class group, the L-function is:

$$L(s, \chi) = \prod_{P} \frac{1}{1 - \chi(P) q^{-s \deg(P)}}$$

where $\chi(P)$ is the value of $\chi$ at the prime $P$.

### Distribution of Primes
The prime number theorem for function fields states that the number of primes of degree $n$ is approximately:

$$\frac{q^n}{n}$$

This is much more precise than the corresponding result for number fields, making function fields an excellent testing ground for conjectures in number theory. 