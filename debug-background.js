// Debug script for background image and transparency issues
// Run this in the browser console to troubleshoot

console.log('=== Background Image & Transparency Debug Tool ===');

// Check if background image element exists
const backgroundImage = document.querySelector('.background-image');
if (backgroundImage) {
  console.log('✅ Background image element found');
  const bgImage = window.getComputedStyle(backgroundImage).backgroundImage;
  console.log('Background image URL:', bgImage);

  // Check if image is actually loading
  const img = new Image();
  img.onload = () => console.log('✅ Background image loaded successfully');
  img.onerror = () => console.log('❌ Background image failed to load');
  img.src = bgImage.replace(/url\(["']?([^"']*)["']?\)/, '$1');
} else {
  console.log('❌ Background image element not found');
}

// Check glassmorphism content sections
const contentSections = document.querySelectorAll('.content-section');
console.log(`Found ${contentSections.length} content sections`);

contentSections.forEach((section, index) => {
  const styles = window.getComputedStyle(section);
  console.log(`Section ${index + 1}:`, {
    background: styles.background,
    backdropFilter: styles.backdropFilter,
    opacity: styles.opacity,
    display: styles.display,
    visibility: styles.visibility
  });
});

// Check if backdrop-filter is supported
const testElement = document.createElement('div');
testElement.style.backdropFilter = 'blur(10px)';
const isSupported = testElement.style.backdropFilter === 'blur(10px)';
console.log('Backdrop-filter support:', isSupported ? '✅ Supported' : '❌ Not supported');

// Check browser info
console.log('Browser info:', {
  userAgent: navigator.userAgent,
  platform: navigator.platform,
  vendor: navigator.vendor
});

// Check if any CSS is overriding our styles
const allElements = document.querySelectorAll('*');
let problematicElements = [];

allElements.forEach(el => {
  const styles = window.getComputedStyle(el);
  if (styles.backgroundImage && styles.backgroundImage !== 'none' && el !== backgroundImage) {
    problematicElements.push({
      element: el.tagName + (el.className ? '.' + el.className : ''),
      backgroundImage: styles.backgroundImage
    });
  }
});

if (problematicElements.length > 0) {
  console.log('⚠️ Other elements with background images found:', problematicElements);
} else {
  console.log('✅ No conflicting background images found');
}

console.log('=== Debug Complete - Check console for results ===');
