---
layout: page
title: Research
permalink: /research/
nav: true
nav_order: 2
---

<div class="research-areas">
  <div class="research-area-card">
    <div class="research-icon">
      <i class="fas fa-infinity" aria-hidden="true"></i>
    </div>
    <div class="research-content">
      <h3 class="translatable-content" data-translation-key="research.galois_representations_title">Galois representations and modular forms</h3>
      <div class="research-text">
        <p class="translatable-content" data-translation-key="research.galois_representations_content">A modern way to look at algebraic number theory is to study the group G<sub>Q</sub> of symmetries of all finite extension of the rational number Q, i.e. of all number fields. One way of doing this is via p-adic (or complex) Galois representations. These are homomorphisms from G<sub>Q</sub> to GL<sub>n</sub>(K) for (the complex or) a p-adic field K.</p>
        
        <p class="translatable-content" data-translation-key="research.galois_representations_approach">If one would understand all these, one could deduce many results in number theory. The reason why this approach is promising is that the Langlands program predicts (conjectures) that many interesting Galois representation can be found in (arithmetic) geometry, for instance by studying modular forms or elliptic curves.</p>
        
        <div class="highlight-box">
          <p class="translatable-content" data-translation-key="research.fermat_theorem"><strong>The most visible success of this method has been the proof of Fermat's last theorem by Wiles and Taylor-Wiles building on work of many others.</strong></p>
        </div>
      </div>
    </div>
  </div>

  <div class="research-area-card">
    <div class="research-icon">
      <i class="fas fa-cube" aria-hidden="true"></i>
    </div>
    <div class="research-content">
      <h3 class="translatable-content" data-translation-key="research.drinfeld_title">Drinfeld modular varieties and Drinfeld modular forms</h3>
      <div class="research-text">
        <p class="translatable-content" data-translation-key="research.drinfeld_intro">It has been observed that questions in number theory often have analogs over global function fields; then the ring of integers Z is replaced by rings like the polynomial ring F<sub>p</sub>[t], and the field of rational numbers Q by the field of rational functions over the finite field F<sub>p</sub> of p elements, where p is a prime number.</p>
        
        <p class="translatable-content" data-translation-key="research.drinfeld_methods">Because methods from algebraic geometry can be applied to function fields, many questions over the latter are more tractable than the corresponding questions over number fields. One particular instance of this is Drinfeld's proof of the global Langlands correspondence for GL<sub>2</sub> over function fields.</p>
        
        <p class="translatable-content" data-translation-key="research.drinfeld_varieties">In his proof Drinfeld introduced what are now called Drinfeld modular varieties; these are function field analogs of certain Shimura varieties. Their cohomology gives rise to Galois representations and these varieties have an interesting geometry coming from their moduli interpretation.</p>
      </div>
    </div>
  </div>
</div>

<style>
/* Clean and modern research page styling */
.research-areas {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.research-area-card {
  display: flex;
  gap: 2rem;
  padding: 2.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.research-area-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.research-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.research-area-card:hover .research-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.research-area-card .research-content h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
  display: inline-block;
}

.research-text p {
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.highlight-box {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  border-left: 4px solid var(--primary);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  margin: 1.5rem 0;
  box-shadow: var(--shadow-sm);
}

.highlight-box p {
  color: var(--text-primary);
  font-size: 1.1rem;
  margin: 0;
  line-height: 1.6;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .research-intro h2 {
    font-size: 2rem;
  }
  
  .research-intro .lead {
    font-size: 1.1rem;
  }
  
  .research-area-card {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
    padding: 2rem;
  }
  
  .research-area-card:hover {
    transform: translateY(-2px);
  }
  
  .research-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .research-area-card .research-content h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .research-area-card {
    padding: 1.5rem;
  }
  
  .research-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .research-area-card .research-content h3 {
    font-size: 1.3rem;
  }
}
</style> 