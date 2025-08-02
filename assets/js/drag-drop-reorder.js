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

    // Wait for Pages CMS to load
    const checkInterval = setInterval(() => {
      const cmsContainer = document.querySelector('[data-pagescms]') || 
                          document.querySelector('.pagescms-container') ||
                          document.querySelector('.cms-content');
      
      if (cmsContainer) {
        clearInterval(checkInterval);
        setupDragAndDrop();
      }
    }, 1000);

    // Also listen for Pages CMS content updates
    document.addEventListener('pagescms-content-updated', setupDragAndDrop);
  }

  // Setup drag and drop for all collections
  function setupDragAndDrop() {
    DRAG_DROP_CONFIG.collections.forEach(collection => {
      setupCollectionDragAndDrop(collection);
    });
  }

  // Setup drag and drop for a specific collection
  function setupCollectionDragAndDrop(collectionName) {
    const collectionContainer = document.querySelector(`[data-collection="${collectionName}"]`) ||
                               document.querySelector(`.${collectionName}-list`) ||
                               document.querySelector(`.collection-${collectionName}`);

    if (!collectionContainer) {
      console.log(`Collection container not found for: ${collectionName}`);
      return;
    }

    const rows = collectionContainer.querySelectorAll('tr[data-id], .collection-item, .cms-item');
    
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
    `;

    // Add hover effects
    dragHandle.addEventListener('mouseenter', () => {
      dragHandle.style.color = '#007bff';
      dragHandle.style.background = '#f8f9fa';
    });

    dragHandle.addEventListener('mouseleave', () => {
      dragHandle.style.color = '#666';
      dragHandle.style.background = 'transparent';
    });

    // Insert drag handle at the beginning of the row
    const firstCell = row.querySelector('td, .cell, .field');
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
    });

    row.addEventListener('dragend', (e) => {
      row.classList.remove(DRAG_DROP_CONFIG.draggingClass);
      row.style.opacity = '';
      row.style.transform = '';
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
    });

    row.addEventListener('dragleave', (e) => {
      row.classList.remove(DRAG_DROP_CONFIG.dropZoneClass);
      row.style.borderTop = '';
    });

    row.addEventListener('drop', (e) => {
      e.preventDefault();
      row.classList.remove(DRAG_DROP_CONFIG.dropZoneClass);
      row.style.borderTop = '';

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
    const rows = Array.from(container.querySelectorAll('tr[data-id], .collection-item, .cms-item'));
    
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
    const rows = Array.from(container.querySelectorAll('tr[data-id], .collection-item, .cms-item'));
    
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
    });
  }

  // Save order changes to Pages CMS
  function saveOrderChanges(collectionName) {
    console.log(`Saving order changes for collection: ${collectionName}`);
    
    // Trigger save in Pages CMS
    const saveButton = document.querySelector('.save-button, .btn-save, [data-action="save"]');
    if (saveButton) {
      saveButton.click();
    }
    
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
      }
      
      .${DRAG_DROP_CONFIG.dropZoneClass} {
        background-color: #f8f9fa;
      }
      
      .${DRAG_DROP_CONFIG.dragHandleClass}:hover {
        background-color: #e9ecef;
      }
      
      .${DRAG_DROP_CONFIG.dragHandleClass}:active {
        cursor: grabbing;
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