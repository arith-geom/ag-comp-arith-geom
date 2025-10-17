document.addEventListener('DOMContentLoaded', function () {
  const debugBtn = document.getElementById('debug-btn');
  const debugModal = document.getElementById('debug-modal');
  const interactiveElementsList = document.getElementById('interactive-elements-list');
  const outlineToggleSwitch = document.getElementById('outline-toggle-switch');

  if (debugBtn && debugModal) {
    // Show the debug modal when the button is clicked
    debugBtn.addEventListener('click', () => {
      populateInteractiveElements();
      $(debugModal).modal('show');
    });
  }

  function populateInteractiveElements() {
    if (!interactiveElementsList) return;

    // Clear existing list
    interactiveElementsList.innerHTML = '';

    // Find all interactive elements, excluding those within the debug modal
    const interactiveElements = document.querySelectorAll(
      'body *:not(#debug-modal *) > a[href], body *:not(#debug-modal *) > button, body *:not(#debug-modal *) > input[type="button"], body *:not(#debug-modal *) > input[type="submit"], body *:not(#debug-modal *) > [onclick]'
    );

    // Create a list item for each element
    interactiveElements.forEach((element, index) => {
      const listItem = document.createElement('a');
      listItem.href = '#';
      listItem.className = 'list-group-item list-group-item-action';
      listItem.textContent = `${index}: ${element.tagName} - ${element.id || element.className || 'No ID/Class'} - "${element.textContent.trim().substring(0,20)}"`;

      listItem.addEventListener('mouseenter', () => {
        element.style.border = '2px solid red';
      });

      listItem.addEventListener('mouseleave', () => {
        element.style.border = '';
      });

      interactiveElementsList.appendChild(listItem);
    });
  }

  if (outlineToggleSwitch) {
    outlineToggleSwitch.addEventListener('change', () => {
      if (outlineToggleSwitch.checked) {
        document.body.classList.add('debug-outline');
      } else {
        document.body.classList.remove('debug-outline');
      }
    });
  }
});