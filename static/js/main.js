/**
 * GearGuard Main JavaScript
 * 
 * 🔍 EXPLANATION FOR BEGINNERS:
 * This JavaScript file handles interactive features like:
 * - Sidebar toggle (mobile menu)
 * - Smooth animations
 * - Dynamic UI updates
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // ============================================
    // Sidebar Toggle (Mobile)
    // ============================================
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleBtn = document.getElementById('sidebarToggleBtn');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    
    /**
     * 🔍 EXPLANATION: Toggle Sidebar
     * Shows/hides the sidebar on mobile devices.
     * Also shows/hides the overlay (dark background).
     */
    function toggleSidebar() {
        sidebar.classList.toggle('show');
        sidebarOverlay.classList.toggle('show');
    }
    
    // Toggle sidebar when button is clicked
    if (sidebarToggleBtn) {
        sidebarToggleBtn.addEventListener('click', toggleSidebar);
    }
    
    // Close sidebar when close button is clicked
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    // Close sidebar when overlay is clicked
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }
    
    // ============================================
    // Auto-dismiss Alerts
    // ============================================
    /**
     * 🔍 EXPLANATION: Auto-dismiss Alerts
     * Automatically hides success messages after 5 seconds.
     * Error messages stay until user dismisses them.
     */
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        if (alert.classList.contains('alert-success')) {
            setTimeout(function() {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000); // 5 seconds
        }
    });
    
    // ============================================
    // HTMX Configuration
    // ============================================
    /**
     * 🔍 EXPLANATION: HTMX Configuration
     * HTMX allows us to update parts of the page without full reload.
     * This configures HTMX to show loading indicators.
     */
    if (typeof htmx !== 'undefined') {
        // Show loading indicator on HTMX requests
        document.body.addEventListener('htmx:beforeRequest', function(event) {
            const target = event.detail.target;
            if (target) {
                target.classList.add('htmx-loading');
            }
        });
        
        // Hide loading indicator after request completes
        document.body.addEventListener('htmx:afterRequest', function(event) {
            const target = event.detail.target;
            if (target) {
                target.classList.remove('htmx-loading');
            }
        });
    }
    
    // ============================================
    // Form Validation Feedback
    // ============================================
    /**
     * 🔍 EXPLANATION: Form Validation
     * Adds visual feedback to form fields with errors.
     */
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // ============================================
    // Tooltip Initialization
    // ============================================
    /**
     * 🔍 EXPLANATION: Tooltips
     * Initializes Bootstrap tooltips (small popup hints).
     */
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ============================================
    // Popover Initialization
    // ============================================
    /**
     * 🔍 EXPLANATION: Popovers
     * Initializes Bootstrap popovers (larger popup content).
     */
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // ============================================
    // Confirm Delete Dialogs
    // ============================================
    /**
     * 🔍 EXPLANATION: Confirm Delete
     * Shows confirmation dialog before deleting items.
     */
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            const message = button.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                event.preventDefault();
            }
        });
    });
    
    // ============================================
    // Smooth Scroll
    // ============================================
    /**
     * 🔍 EXPLANATION: Smooth Scroll
     * Makes page scrolling smooth when clicking anchor links.
     */
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(event) {
            const href = anchor.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                const target = document.querySelector(href);
                if (target) {
                    event.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // ============================================
    // Loading State for Buttons
    // ============================================
    /**
     * 🔍 EXPLANATION: Button Loading State
     * Shows loading spinner in buttons when form is submitted.
     * This runs AFTER the form starts submitting (doesn't block submission).
     */
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                // Store original state
                const originalHTML = submitButton.innerHTML;
                
                // Show loading state (form is already submitting, this is just visual feedback)
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...';
            }
        });
    });
    
});

/**
 * 🔍 EXPLANATION: Utility Functions
 * Helper functions that can be used throughout the application.
 */

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format datetime for display
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show toast notification (if Bootstrap toast is available)
function showToast(message, type = 'info') {
    // This will be implemented when we add toast notifications
    console.log(`Toast [${type}]: ${message}`);
}

