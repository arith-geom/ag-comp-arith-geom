// Drag and Drop Reordering for Pages CMS
// This script provides drag-and-drop functionality for reordering content in Pages CMS

(function() {
  'use strict';

  // Configuration
  const DRAG_DROP_CONFIG = {
    enabled: true,
    collections: ['members', 'research', 'links', 'teaching'],
    dragHandleClass: 'drag-handle',
    draggingClass: 'dragging',
    dropZoneClass: 'drop-zone',
    orderField: 'order'
  };

  // Initialize drag and drop functionality
  function initDragAndDrop() {
    if (!DRAG_DROP_CONFIG.enabled) return;

    console.log('Initializing drag and drop reordering...');

    // Try to setup immediately
    setupDragAndDrop();

    // Also try periodically in case Pages CMS loads later
    const checkInterval = setInterval(() => {
      setupDragAndDrop();
    }, 2000);

    // Stop checking after 30 seconds
    setTimeout(() => {
      clearInterval(checkInterval);
    }, 30000);

    // Listen for Pages CMS content updates
    document.addEventListener('pagescms-content-updated', setupDragAndDrop);
    
    // Listen for DOM changes
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList') {
          setupDragAndDrop();
        }
      });
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }

  // Setup drag and drop for all collections
  function setupDragAndDrop() {
    DRAG_DROP_CONFIG.collections.forEach(collection => {
      setupCollectionDragAndDrop(collection);
    });
  }

  // Setup drag and drop for a specific collection
  function setupCollectionDragAndDrop(collectionName) {
    // Try multiple selectors to find the collection container
    const selectors = [
      `[data-collection="${collectionName}"]`,
      `.${collectionName}-list`,
      `.collection-${collectionName}`,
      `[data-testid="${collectionName}-list"]`,
      `.pagescms-collection[data-name="${collectionName}"]`,
      `table[data-collection="${collectionName}"]`,
      `.collection-table[data-collection="${collectionName}"]`
    ];

    let collectionContainer = null;
    for (const selector of selectors) {
      collectionContainer = document.querySelector(selector);
      if (collectionContainer) break;
    }

    // If no specific container found, try to find any table or list that might contain the collection
    if (!collectionContainer) {
      const tables = document.querySelectorAll('table, .collection-list, .list-container');
      for (const table of tables) {
        if (table.textContent.toLowerCase().includes(collectionName)) {
          collectionContainer = table;
          break;
        }
      }
    }

    if (!collectionContainer) {
      console.log(`Collection container not found for: ${collectionName}`);
      return;
    }

    // Find rows - try multiple selectors
    const rowSelectors = [
      'tr[data-id]',
      'tr[data-item-id]',
      '.collection-item',
      '.cms-item',
      '.list-item',
      'tr:not(:first-child)', // All table rows except header
      '.item-row'
    ];

    let rows = [];
    for (const selector of rowSelectors) {
      rows = collectionContainer.querySelectorAll(selector);
      if (rows.length > 0) break;
    }

    if (rows.length === 0) {
      console.log(`No rows found for collection: ${collectionName}`);
      return;
    }

    console.log(`Found ${rows.length} rows for collection: ${collectionName}`);
    
    rows.forEach((row, index) => {
      // Add drag handle
      addDragHandle(row, index);
      
      // Make row draggable
      makeDraggable(row, collectionName);
      
      // Make row a drop zone
      makeDropZone(row, collectionName);
    });

    console.log(`Drag and drop setup for collection: ${collectionName}`);
  }

  // Add drag handle to a row
  function addDragHandle(row, index) {
    // Check if drag handle already exists
    if (row.querySelector(`.${DRAG_DROP_CONFIG.dragHandleClass}`)) {
      return;
    }

    const dragHandle = document.createElement('div');
    dragHandle.className = DRAG_DROP_CONFIG.dragHandleClass;
    dragHandle.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
        <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/>
      </svg>
    `;
    dragHandle.style.cssText = `
      cursor: grab;
      padding: 4px;
      color: #666;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      transition: all 0.2s ease;
      margin-right: 8px;
      opacity: 0.7;
    `;

    // Add hover effects
    dragHandle.addEventListener('mouseenter', () => {
      dragHandle.style.color = '#007bff';
      dragHandle.style.background = '#f8f9fa';
      dragHandle.style.opacity = '1';
      dragHandle.style.transform = 'scale(1.1)';
    });

    dragHandle.addEventListener('mouseleave', () => {
      dragHandle.style.color = '#666';
      dragHandle.style.background = 'transparent';
      dragHandle.style.opacity = '0.7';
      dragHandle.style.transform = 'scale(1)';
    });

    // Insert drag handle at the beginning of the row
    const firstCell = row.querySelector('td, .cell, .field, th');
    if (firstCell) {
      firstCell.insertBefore(dragHandle, firstCell.firstChild);
    } else {
      row.insertBefore(dragHandle, row.firstChild);
    }
  }

  // Make a row draggable
  function makeDraggable(row, collectionName) {
    row.draggable = true;
    row.setAttribute('data-collection', collectionName);

    row.addEventListener('dragstart', (e) => {
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/html', row.outerHTML);
      row.classList.add(DRAG_DROP_CONFIG.draggingClass);
      
      // Add visual feedback
      row.style.opacity = '0.5';
      row.style.transform = 'rotate(2deg)';
      row.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
      row.style.zIndex = '1000';
      row.style.position = 'relative';
    });

    row.addEventListener('dragend', (e) => {
      row.classList.remove(DRAG_DROP_CONFIG.draggingClass);
      row.style.opacity = '';
      row.style.transform = '';
      row.style.boxShadow = '';
      row.style.zIndex = '';
      row.style.position = '';
    });
  }

  // Make a row a drop zone
  function makeDropZone(row, collectionName) {
    row.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      
      // Add visual feedback for drop zone
      row.classList.add(DRAG_DROP_CONFIG.dropZoneClass);
      row.style.borderTop = '2px solid #007bff';
      row.style.backgroundColor = '#f8f9fa';
    });

    row.addEventListener('dragleave', (e) => {
      row.classList.remove(DRAG_DROP_CONFIG.dropZoneClass);
      row.style.borderTop = '';
      row.style.backgroundColor = '';
    });

    row.addEventListener('drop', (e) => {
      e.preventDefault();
      row.classList.remove(DRAG_DROP_CONFIG.dropZoneClass);
      row.style.borderTop = '';
      row.style.backgroundColor = '';

      const draggedRow = document.querySelector(`.${DRAG_DROP_CONFIG.draggingClass}`);
      if (draggedRow && draggedRow !== row) {
        // Reorder the rows
        reorderRows(draggedRow, row, collectionName);
      }
    });
  }

  // Reorder rows and update order values
  function reorderRows(draggedRow, targetRow, collectionName) {
    const container = draggedRow.parentNode;
    const rows = Array.from(container.querySelectorAll('tr, .collection-item, .cms-item, .list-item'));
    
    // Find positions
    const draggedIndex = rows.indexOf(draggedRow);
    const targetIndex = rows.indexOf(targetRow);
    
    if (draggedIndex === -1 || targetIndex === -1) return;

    // Move the row
    if (draggedIndex < targetIndex) {
      container.insertBefore(draggedRow, targetRow.nextSibling);
    } else {
      container.insertBefore(draggedRow, targetRow);
    }

    // Update order values
    updateOrderValues(container, collectionName);
    
    // Save changes
    saveOrderChanges(collectionName);
  }

  // Update order values for all rows
  function updateOrderValues(container, collectionName) {
    const rows = Array.from(container.querySelectorAll('tr, .collection-item, .cms-item, .list-item'));
    
    rows.forEach((row, index) => {
      // Update the order field in the row
      const orderField = row.querySelector(`[data-field="${DRAG_DROP_CONFIG.orderField}"] input`);
      if (orderField) {
        orderField.value = index + 1;
        orderField.dispatchEvent(new Event('change', { bubbles: true }));
      }
      
      // Also update any hidden order field
      const hiddenOrderField = row.querySelector('input[type="hidden"][name*="order"]');
      if (hiddenOrderField) {
        hiddenOrderField.value = index + 1;
      }

      // Try to find order field by name
      const orderInputs = row.querySelectorAll('input[name*="order"], input[data-field*="order"]');
      orderInputs.forEach(input => {
        input.value = index + 1;
        input.dispatchEvent(new Event('change', { bubbles: true }));
      });
    });
  }

  // Save order changes to Pages CMS
  function saveOrderChanges(collectionName) {
    console.log(`Saving order changes for collection: ${collectionName}`);
    
    // Try to trigger save in Pages CMS
    const saveButtons = document.querySelectorAll('.save-button, .btn-save, [data-action="save"], button[type="submit"]');
    saveButtons.forEach(button => {
      if (button.textContent.toLowerCase().includes('save') || 
          button.getAttribute('data-action') === 'save') {
        button.click();
      }
    });
    
    // Show success message
    showReorderMessage('Order updated successfully!', 'success');
  }

  // Show reorder message
  function showReorderMessage(message, type = 'info') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `reorder-message reorder-message-${type}`;
    messageDiv.textContent = message;
    messageDiv.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 12px 16px;
      border-radius: 4px;
      color: white;
      font-weight: 500;
      z-index: 10000;
      animation: slideIn 0.3s ease;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    `;

    // Set background color based on type
    switch (type) {
      case 'success':
        messageDiv.style.background = '#28a745';
        break;
      case 'error':
        messageDiv.style.background = '#dc3545';
        break;
      default:
        messageDiv.style.background = '#007bff';
    }

    document.body.appendChild(messageDiv);

    // Remove message after 3 seconds
    setTimeout(() => {
      messageDiv.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
        if (messageDiv.parentNode) {
          messageDiv.parentNode.removeChild(messageDiv);
        }
      }, 300);
    }, 3000);
  }

  // Add CSS animations
  function addReorderStyles() {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
      
      .${DRAG_DROP_CONFIG.draggingClass} {
        opacity: 0.5;
        transform: rotate(2deg);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1000;
        position: relative;
      }
      
      .${DRAG_DROP_CONFIG.dropZoneClass} {
        background-color: #f8f9fa;
        border-top: 2px solid #007bff;
        transition: all 0.2s ease;
      }
      
      .${DRAG_DROP_CONFIG.dragHandleClass}:hover {
        background-color: #e9ecef;
        transform: scale(1.1);
      }
      
      .${DRAG_DROP_CONFIG.dragHandleClass}:active {
        cursor: grabbing;
        transform: scale(0.95);
      }
    `;
    document.head.appendChild(style);
  }

  // Public API
  window.PagesCMSReorder = {
    init: initDragAndDrop,
    setupCollection: setupCollectionDragAndDrop,
    updateOrder: updateOrderValues,
    saveChanges: saveOrderChanges
  };

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      addReorderStyles();
      initDragAndDrop();
    });
  } else {
    addReorderStyles();
    initDragAndDrop();
  }

})(); 