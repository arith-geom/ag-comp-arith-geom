---
---
description: It has been observed that questions in number theory often have analogs
  over global function fields; then the ring of integers $\mathbb{Z}$ is replaced
  by rings like the polynomial ring $\mathbb{F}_p[t]$, and the field of rational numbers
  $\mathbb{Q}$ by the field of rational functions over the finite field $\mathbb{F}_p$
  of $p$ elements, where $p$ is a prime number. Because methods from algebraic geometry
  can be applied to function fields, many questions over the latter are more tractable
  than the corresponding questions over number fields. One particular instance of
  this is Drinfeld's proof of the global Langlands correspondence for $\mathrm{GL}_2$
  over function fields. In his proof Drinfeld introduced what are now called Drinfeld
  modular varieties; these are function field analogs of certain Shimura varieties.
  Their cohomology gives rise to Galois representations and these varieties have an
  interesting geometry coming from their moduli interpretation.
featured: false
layout: page
order: 999
title: Drinfeld modular varieties and Drinfeld modular forms
---


## Mathematical Background

The study of Drinfeld modular varieties involves several key mathematical concepts:

### Function Fields
In this context, we work with function fields over finite fields. The basic setup involves:
- The polynomial ring $\mathbb{F}_p[t]$ where $p$ is a prime
- The field of rational functions $\mathbb{F}_p(t)$
- Analogies with the number field case where $\mathbb{Z}$ corresponds to $\mathbb{F}_p[t]$ and $\mathbb{Q}$ corresponds to $\mathbb{F}_p(t)$

### Drinfeld Modular Forms
Drinfeld modular forms are functions on Drinfeld modular varieties that satisfy certain transformation properties. For a Drinfeld module $\phi$ of rank $r$, we consider forms of weight $k$ that transform as:

$$f(\gamma \tau) = (c\tau + d)^k f(\tau)$$

where $\gamma = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in \mathrm{GL}_2(\mathbb{F}_p[t])$.

### Galois Representations
The cohomology of Drinfeld modular varieties gives rise to Galois representations:

$$\rho: \mathrm{Gal}(\overline{\mathbb{F}_p(t)}/\mathbb{F}_p(t)) \to \mathrm{GL}_n(\mathbb{Q}_\ell)$$

These representations are crucial for understanding the arithmetic properties of function fields.