---
description: The modularity theorem, proved by Wiles and Taylor-Wiles, states that
  every semistable elliptic curve over $\mathbb{Q}$ is modular. This means that the
  Galois representation attached to the $p$-adic Tate module of the curve comes from
  a modular form. This result has been generalized in various directions, including
  the proof of the full modularity theorem by Breuil, Conrad, Diamond, and Taylor.
  We study generalizations of these results to other Galois representations and their
  applications to Diophantine equations.
featured: false
layout: page
order: 999
title: Modularity of Galois representations
---

## Modularity Theorems

### Wiles-Taylor-Wiles Theorem
The original modularity theorem states that every semistable elliptic curve $E/\mathbb{Q}$ is modular. This means there exists a modular form $f$ of weight 2 such that:

$$\rho_{E,p} \cong \rho_f$$

where $\rho_{E,p}$ is the Galois representation attached to the $p$-adic Tate module $T_p(E)$ and $\rho_f$ is the Galois representation attached to the modular form $f$.

### Serre's Conjecture
Serre's conjecture (now a theorem due to Khare-Wintenberger) states that every odd, irreducible, continuous representation:

$$\rho: G_{\mathbb{Q}} \to \mathrm{GL}_2(\overline{\mathbb{F}_p})$$

is modular, i.e., comes from a modular form mod $p$.

### Fontaine-Mazur Conjecture
The Fontaine-Mazur conjecture predicts that every irreducible, continuous, odd representation:

$$\rho: G_{\mathbb{Q}} \to \mathrm{GL}_2(\mathbb{Q}_p)$$

that is unramified outside finitely many primes and potentially semistable at $p$ is modular.

## Applications

### Fermat's Last Theorem
The proof of Fermat's Last Theorem by Wiles and Taylor-Wiles relies on showing that the Frey curve:

$$y^2 = x(x - a^p)(x + b^p)$$

associated to a putative solution $a^p + b^p = c^p$ is modular, which leads to a contradiction.

### Diophantine Equations
Modularity results have been applied to solve various Diophantine equations, including:
- The equation $x^p + y^p = z^p$ for $p \geq 3$
- Generalized Fermat equations
- Catalan's conjecture (Mihăilescu's theorem)