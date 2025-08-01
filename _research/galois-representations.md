---
layout: page
title: "Galois representations and modular forms"
description: "A modern way to look at algebraic number theory is to study the group $G_{\\mathbb{Q}}$ of symmetries of all finite extension of the rational number $\\mathbb{Q}$, i.e. of all number fields. One way of doing this is via $p$-adic (or complex) Galois representations. These are homomorphisms from $G_{\\mathbb{Q}}$ to $\\mathrm{GL}_n(K)$ for (the complex or) a $p$-adic field $K$. If one would understand all these, one could deduce many results in number theory. The reason why this approach is promising is that the Langlands program predicts (conjectures) that many interesting Galois representation can be found in (arithmetic) geometry, for instance by studying modular forms or elliptic curves. The most visible success of this method has been the proof of Fermat's last theorem by Wiles and Taylor-Wiles building on work of many others."
---

## Galois Representations

### Basic Definitions
A Galois representation is a continuous homomorphism:

$$\rho: G_{\mathbb{Q}} \to \mathrm{GL}_n(K)$$

where $G_{\mathbb{Q}} = \mathrm{Gal}(\overline{\mathbb{Q}}/\mathbb{Q})$ is the absolute Galois group of $\mathbb{Q}$ and $K$ is either $\mathbb{C}$ or a $p$-adic field $\mathbb{Q}_p$.

### Modular Forms and Galois Representations
The Langlands program predicts a correspondence between:
- Modular forms of weight $k$ and level $N$
- Galois representations $\rho: G_{\mathbb{Q}} \to \mathrm{GL}_2(\mathbb{Q}_p)$

For a modular form $f(z) = \sum_{n=1}^{\infty} a_n q^n$ with $q = e^{2\pi i z}$, the associated Galois representation satisfies:

$$\mathrm{tr}(\rho(\mathrm{Frob}_\ell)) = a_\ell$$

for almost all primes $\ell$, where $\mathrm{Frob}_\ell$ is the Frobenius element at $\ell$.

### Elliptic Curves
For an elliptic curve $E/\mathbb{Q}$ with conductor $N$, the $p$-adic Tate module $T_p(E)$ gives rise to a Galois representation:

$$\rho_{E,p}: G_{\mathbb{Q}} \to \mathrm{GL}_2(\mathbb{Z}_p)$$

The modularity theorem (proved by Wiles and Taylor-Wiles) states that this representation is modular, i.e., it comes from a modular form of weight 2 and level $N$. 