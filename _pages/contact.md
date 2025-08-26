---
layout: page
title: Contact
permalink: "/contact/"
nav: true
nav_order: 7
order: 100
---
<div class="contact-sections">
  <div class="location-section mt-5">
  <div class="location-container">
    <div class="location-header">
      <div class="location-icon">
        <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
      </div>
      <h3 class="translatable-content" data-translation-key="contact.our_location">Our Location</h3>
    </div>
    <div class="location-content">
      <div class="address-info">
        <h4 class="translatable-content" data-translation-key="contact.postal_address">Postal Address</h4>
        <div class="address-block">
          <p><strong>Computational Arithmetic Geometry</strong></p>
          <p>IWR (Interdisciplinary Center for Scientific Computing)</p>
          <p>Heidelberg University</p>
          <p>Im Neuenheimer Feld 205</p>
          <p>69120 Heidelberg</p>
          <p>Germany</p>
        </div>
        <div class="map-actions mt-3">
          <a href="https://maps.google.com/?q=Im+Neuenheimer+Feld+205,+69120+Heidelberg,+Germany"
             target="_blank"
             rel="noopener"
             class="btn btn-outline-primary map-btn">
            <i class="fas fa-external-link-alt me-2" aria-hidden="true"></i><span class="translatable-content" data-translation-key="contact.open_in_google_maps">Open in Google Maps</span>
          </a>
        </div>
      </div>
      <div class="map-wrapper">
        <iframe
          width="100%"
          height="300"
          style="border:0; border-radius: var(--radius-lg);"
          loading="lazy"
          allowfullscreen
          title="Map showing the location of AG Computational Arithmetic Geometry at Heidelberg University"
          src="https://www.google.com/maps/embed/v1/place?q=Im+Neuenheimer+Feld+205,+69120+Heidelberg,+Germany&key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8">
        </iframe>
      </div>
    </div>
  </div>
</div>

<div class="contact-container mt-5">
  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-phone" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3 class="translatable-content" data-translation-key="contact.phone">Phone</h3>
      <div class="contact-detail">
        <p><strong>+49-6221-54-14734</strong></p>
      </div>
    </div>
  </div>

  <div class="contact-card">
    <div class="contact-icon">
      <i class="fas fa-fax" aria-hidden="true"></i>
    </div>
    <div class="contact-content">
      <h3 class="translatable-content" data-translation-key="contact.fax">Fax</h3>
      <div class="contact-detail">
        <p><strong>+49-6221-54-14737</strong></p>
      </div>
    </div>
  </div>
</div>

<div class="contact-form-section mt-5">
  <div class="form-container">
    <div class="form-header">
      <div class="form-icon">
        <i class="fas fa-envelope" aria-hidden="true"></i>
      </div>
      <h3 class="translatable-content" data-translation-key="contact.send_message">Get in Touch</h3>
    </div>
    <div class="form-content">
      <div class="email-info">
        <div class="contact-options">
          <div class="contact-buttons" style="display: inline-block; margin-right: 1rem; vertical-align: middle;">
            <a href="mailto:sekretariat.boeckle@iwr.uni-heidelberg.de" class="btn btn-outline-primary">
              <i class="fas fa-envelope me-2" aria-hidden="true"></i>Send Email
            </a>
          </div>
          <div class="contact-detail" style="display: inline-block; vertical-align: middle;">
            <p><a href="mailto:sekretariat.boeckle@iwr.uni-heidelberg.de" class="email-link"><strong>sekretariat.boeckle@iwr.uni-heidelberg.de</strong></a></p>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>
</div>

<style>
/* Contact Sections - Full Screen Layout */
.contact-sections {
  width: 100%;
  margin: 0;
  padding-left: 1rem;
  padding-right: 1rem;
}

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
  width: 100%;
  margin: 0;
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
  color: white !important;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
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

.location-section {
  width: 100%;
  margin: 0;
}

.location-container {
  background: var(--bg-primary);
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.location-container:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.location-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--primary);
}

.location-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white !important;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.location-container:hover .location-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.location-header h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.location-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}

.address-info h4 {
  color: var(--text-primary);
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.map-wrapper {
  position: relative;
  overflow: hidden;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
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

/* Match theme for map button - outline style for better visibility */
.map-actions .map-btn {
  background: transparent !important;
  color: var(--primary) !important;
  border: 2px solid var(--primary) !important;
  font-weight: 600 !important;
  text-decoration: none !important;
  transition: all var(--transition-base) !important;
}

.map-actions .map-btn:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-md) !important;
}

/* Contact Form Styles */
.contact-form-section {
  width: 100%;
  margin: 0;
}

.form-container {
  background: var(--bg-primary);
  padding: 2.5rem;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.form-container:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}

.form-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--primary);
}

.form-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--heidelberg-red) 100%);
  color: white !important;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-base);
}

.form-container:hover .form-icon {
  transform: scale(1.1);
  box-shadow: var(--shadow-md);
}

.form-header h3 {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin: 0;
}

.form-content {
  display: block;
}

.email-info h4 {
  color: var(--text-primary);
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border-color);
}

.contact-options {
  background: var(--bg-secondary);
  padding: 1.5rem;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
}

.contact-buttons {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.contact-divider {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.form-label {
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-style: italic;
}



/* Enhanced dark mode for contact page */
[data-theme="dark"] .location-container,
body.dark-mode .location-container {
  background: linear-gradient(135deg, #111827 0%, #1f2937 100%) !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
  border: 1px solid #374151 !important;
}

[data-theme="dark"] .contact-card,
body.dark-mode .contact-card {
  background: linear-gradient(135deg, #111827 0%, #1f2937 100%) !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
  transition: all 0.3s ease !important;
}

[data-theme="dark"] .contact-card:hover,
body.dark-mode .contact-card:hover {
  transform: translateY(-4px) !important;
  box-shadow: 0 8px 24px rgba(248, 113, 113, 0.2) !important;
  border-color: #ff6b6b !important;
}

[data-theme="dark"] .form-container,
body.dark-mode .form-container {
  background: linear-gradient(135deg, #111827 0%, #1f2937 100%) !important;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
}

/* Ensure the map button keeps strong contrast in dark mode */
[data-theme="dark"] .map-actions .map-btn,
body.dark-mode .map-actions .map-btn {
  background: transparent !important;
  color: var(--link-color) !important;
  border-color: var(--link-color) !important;
}

[data-theme="dark"] .map-actions .map-btn:hover,
body.dark-mode .map-actions .map-btn:hover {
  background: var(--primary) !important;
  color: var(--primary-text) !important;
  border-color: var(--primary) !important;
}

[data-theme="dark"] .form-container:hover,
body.dark-mode .form-container:hover {
  box-shadow: 0 12px 40px rgba(248, 113, 113, 0.15) !important;
}



/* Responsive adjustments */
@media (max-width: 768px) {
  .contact-sections {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }

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
  
  .location-container {
    padding: 1.5rem;
  }
  
  .location-header h3 {
    font-size: 1.5rem;
  }
  
  .location-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .form-container {
    padding: 1.5rem;
  }
  
  .form-header h3 {
    font-size: 1.5rem;
  }
  
  .form-content {
    display: block;
  }
}

@media (max-width: 480px) {
  .contact-sections {
    padding-left: 0.25rem;
    padding-right: 0.25rem;
  }

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

  .location-container {
    padding: 1rem;
  }

  .form-container {
    padding: 1rem;
  }

  .form-header h3 {
    font-size: 1.3rem;
  }
}
</style> 