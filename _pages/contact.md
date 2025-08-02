---
layout: page
title: Contact
permalink: /contact/
nav: true
nav_order: 7
---

<div class="contact-intro mb-5">
  <h2 class="text-center mb-4">Get in Touch</h2>
  <p class="lead text-center">We welcome inquiries from students, researchers, and collaborators interested in arithmetic geometry and computational number theory.</p>
</div>

<div class="contact-container">
  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3>Postal Address</h3>
      <div class="address-block">
        <p><strong>Computational Arithmetic Geometry</strong></p>
        <p>IWR (Interdisciplinary Center for Scientific Computing)</p>
        <p>University of Heidelberg</p>
        <p>Im Neuenheimer Feld 205</p>
        <p>69120 Heidelberg</p>
        <p>Germany</p>
      </div>
    </div>
  </div>

  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-envelope" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3>Email</h3>
      <div class="contact-detail">
        <p><a href="mailto:sekretariat.boeckle@iwr.uni-heidelberg.de" class="email-link"><strong>sekretariat.boeckle@iwr.uni-heidelberg.de</strong></a></p>
        <small class="text-muted">Click the email address to open your email client</small>
      </div>
    </div>
  </div>

  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-phone" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3>Phone</h3>
      <div class="contact-detail">
        <p><strong>+49-6221-54-14734</strong></p>
        <small class="text-muted">Monday - Friday, 9:00 AM - 5:00 PM (CET)</small>
      </div>
    </div>
  </div>

  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-fax" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3>Fax</h3>
      <div class="contact-detail">
        <p><strong>+49-6221-54-14737</strong></p>
        <small class="text-muted">Available 24/7</small>
      </div>
    </div>
  </div>
</div>

<div class="contact-form-section mt-5">
  <div class="form-container">
    <h3 class="text-center mb-4">Send us a Message</h3>
    <form class="contact-form" action="#" method="POST" id="contactForm">
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="firstName" class="form-label">First Name *</label>
          <input type="text" class="form-control" id="firstName" name="firstName" required>
        </div>
        <div class="col-md-6 mb-3">
          <label for="lastName" class="form-label">Last Name *</label>
          <input type="text" class="form-control" id="lastName" name="lastName" required>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-6 mb-3">
          <label for="email" class="form-label">Email Address *</label>
          <input type="email" class="form-control" id="email" name="email" required>
        </div>
        <div class="col-md-6 mb-3">
          <label for="phone" class="form-label">Phone Number</label>
          <input type="tel" class="form-control" id="phone" name="phone">
        </div>
      </div>
      
      <div class="mb-3">
        <label for="organization" class="form-label">Organization/Institution</label>
        <input type="text" class="form-control" id="organization" name="organization">
      </div>
      
      <div class="mb-3">
        <label for="subject" class="form-label">Subject *</label>
        <select class="form-select" id="subject" name="subject" required>
          <option value="">Please select a subject</option>
          <option value="general">General Inquiry</option>
          <option value="research">Research Collaboration</option>
          <option value="student">Student Information</option>
          <option value="visiting">Visiting Scholar</option>
          <option value="seminar">Seminar/Conference</option>
          <option value="other">Other</option>
        </select>
      </div>
      
      <div class="mb-3">
        <label for="message" class="form-label">Message *</label>
        <textarea class="form-control" id="message" name="message" rows="6" placeholder="Please provide details about your inquiry..." required></textarea>
      </div>
      
      <div class="mb-3">
        <div class="form-check">
          <input class="form-check-input" type="checkbox" id="newsletter" name="newsletter">
          <label class="form-check-label" for="newsletter">
            Subscribe to our newsletter for updates on seminars and research activities
          </label>
        </div>
      </div>
      
      <div class="text-center">
        <button type="submit" class="btn btn-primary btn-lg">
          <i class="fas fa-paper-plane me-2" aria-hidden="true"></i>Send Message
        </button>
      </div>
    </form>
  </div>
</div>

<div class="map-section mt-5">
  <div class="map-container">
    <h3 class="text-center mb-4">Our Location</h3>
    <div class="map-wrapper">
      <iframe
        width="100%"
        height="400"
        style="border:0; border-radius: var(--radius-lg);"
        loading="lazy"
        allowfullscreen
        title="Map showing the location of AG Computational Arithmetic Geometry at University of Heidelberg"
        src="https://www.google.com/maps/embed/v1/place?q=Im+Neuenheimer+Feld+205,+69120+Heidelberg,+Germany&key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8">
      </iframe>
    </div>
    <div class="map-actions mt-3 text-center">
      <a href="https://maps.google.com/?q=Im+Neuenheimer+Feld+205,+69120+Heidelberg,+Germany" 
         target="_blank" 
         rel="noopener" 
         class="btn btn-primary">
        <i class="fas fa-external-link-alt me-2" aria-hidden="true"></i>Open in Google Maps
      </a>
    </div>
  </div>
</div>



<style>
.contact-intro {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.contact-intro h2 {
  color: var(--text-primary);
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.contact-intro .lead {
  font-size: 1.25rem;
  color: var(--text-secondary);
  line-height: 1.6;
}

.contact-container {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.contact-card {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  padding: 2rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.contact-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.contact-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.contact-card:hover .contact-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.contact-content {
  flex-grow: 1;
}

.contact-content h3 {
  color: var(--text-primary);
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--primary);
  display: inline-block;
}

.address-block p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.address-block p:first-child {
  color: var(--text-primary);
  font-weight: 600;
  font-size: 1.1rem;
}

.contact-detail p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.contact-detail small {
  font-size: 0.9rem;
}

.email-link {
  color: var(--primary);
  text-decoration: none;
  transition: all var(--transition-base);
  border-bottom: 1px solid transparent;
}

.email-link:hover {
  color: var(--heidelberg-red);
  border-bottom-color: var(--heidelberg-red);
  text-decoration: none;
}

.email-link:focus {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
  border-radius: 4px;
}

.map-section {
  max-width: 1000px;
  margin: 0 auto;
}

.map-container {
  background: var(--bg-primary);
  padding: 2rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.map-container h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.map-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.map-actions .btn {
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.map-actions .btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* Contact Form Styles */
.contact-form-section {
  max-width: 800px;
  margin: 0 auto;
}

.form-container {
  background: var(--bg-primary);
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.form-container h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 2rem;
}

.contact-form .form-label {
  color: var(--text-primary);
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.contact-form .form-control,
.contact-form .form-select {
  border: 2px solid var(--border-color);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  font-size: 1rem;
  background: var(--bg-secondary);
  color: var(--text-primary);
  transition: all var(--transition-base);
}

.contact-form .form-control:focus,
.contact-form .form-select:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--primary-rgb), 0.25);
  background: var(--bg-primary);
}

.contact-form .form-control::placeholder {
  color: var(--text-muted);
}

.contact-form textarea.form-control {
  resize: vertical;
  min-height: 120px;
}

.contact-form .form-check {
  margin-top: 1rem;
}

.contact-form .form-check-input {
  border: 2px solid var(--border-color);
  background: var(--bg-secondary);
}

.contact-form .form-check-input:checked {
  background-color: var(--primary);
  border-color: var(--primary);
}

.contact-form .form-check-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 0.2rem rgba(var(--primary-rgb), 0.25);
}

.contact-form .form-check-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  line-height: 1.5;
}

.contact-form .btn {
  padding: 1rem 2rem;
  font-weight: 600;
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  border: none;
  color: white;
}

.contact-form .btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  background: linear-gradient(135deg, var(--heidelberg-red) 0%, var(--primary) 100%);
}

.contact-form .btn:focus {
  box-shadow: 0 0 0 0.2rem rgba(var(--primary-rgb), 0.25);
}

/* Form validation styles */
.contact-form .form-control.is-invalid {
  border-color: #dc3545;
  box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
}

.contact-form .form-control.is-valid {
  border-color: #198754;
  box-shadow: 0 0 0 0.2rem rgba(25, 135, 84, 0.25);
}

.invalid-feedback {
  display: block;
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

.valid-feedback {
  display: block;
  color: #198754;
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .contact-intro h2 {
    font-size: 2rem;
  }
  
  .contact-intro .lead {
    font-size: 1.1rem;
  }
  
  .contact-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .contact-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
    padding: 1.5rem;
  }
  
  .contact-card:hover {
    transform: translateY(-2px);
  }
  
  .contact-icon {
    width: 50px;
    height: 50px;
    font-size: 1.25rem;
  }
  
  .contact-content h3 {
    font-size: 1.3rem;
  }
  
  .map-container {
    padding: 1.5rem;
  }
  
  .map-container h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .contact-card {
    padding: 1rem;
  }
  
  .contact-icon {
    width: 40px;
    height: 40px;
    font-size: 1rem;
  }
  
  .contact-content h3 {
    font-size: 1.2rem;
  }
  
  .map-container {
    padding: 1rem;
  }
  
  .form-container {
    padding: 1.5rem;
  }
  
  .form-container h3 {
    font-size: 1.5rem;
  }
  
  .contact-form .btn {
    padding: 0.75rem 1.5rem;
    font-size: 0.95rem;
  }
}
</style> 