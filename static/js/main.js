// Global variables
let currentDepartmentId = null;

// Function to load faculty for selected department
function loadFaculty(departmentId, departmentName) {
    console.log(`Loading faculty for ${departmentName} (${departmentId})`);
    currentDepartmentId = departmentId;
    
    // Update UI
    $('#departmentTitle').html(`<i class="bi bi-people-fill me-2"></i>${departmentName}`);
    $('#facultyList').html('<tr><td colspan="7" class="text-center py-4"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></td></tr>');
    
    // Load faculty data
    $.ajax({
        url: `/api/faculty/${encodeURIComponent(departmentId)}`,
        method: 'GET',
        dataType: 'json',
        success: function(data) {
            console.log('Faculty data loaded:', data);
            if (!data || data.length === 0) {
                $('#facultyList').html('<tr><td colspan="7" class="text-center text-muted py-4"><i class="bi bi-people me-2"></i>No faculty members found in this department</td></tr>');
                return;
            }
            
            let html = '';
            data.forEach((faculty, index) => {
                const isActive = faculty.isActive !== false; // Default to true if not set
                html += `
                    <tr class="${!isActive ? 'table-secondary' : ''}" data-faculty-id="${faculty.Initials || ''}">
                        <td class="fw-medium">${faculty.Name || 'N/A'}</td>
                        <td><span class="badge bg-light text-dark">${faculty.Initials || 'N/A'}</span></td>
                        <td>${faculty.Designation || 'N/A'}</td>
                        <td>${faculty.Phone || 'N/A'}</td>
                        <td class="text-nowrap">
                            ${faculty.Email ? `<a href="mailto:${faculty.Email}" class="text-decoration-none">${faculty.Email}</a>` : 'N/A'}
                        </td>
                        <td>
                            <span class="badge rounded-pill ${isActive ? 'bg-success' : 'bg-secondary'}">
                                <i class="bi ${isActive ? 'bi-check-circle' : 'bi-lock'} me-1"></i>
                                ${isActive ? 'Active' : 'Locked'}
                            </span>
                        </td>
                        <td>
                            <div class="btn-group btn-group-sm" role="group">
                                <button class="btn ${isActive ? 'btn-outline-warning' : 'btn-outline-success'} toggle-status" 
                                        data-index="${index}"
                                        title="${isActive ? 'Lock Faculty' : 'Unlock Faculty'}">
                                    <i class="bi ${isActive ? 'bi-lock' : 'bi-unlock'}"></i>
                                </button>
                            </div>
                        </td>
                    </tr>
                `;
            });
            
            $('#facultyList').html(html);
        },
        error: function(xhr, status, error) {
            console.error('Error loading faculty:', error);
            $('#facultyList').html(`
                <tr>
                    <td colspan="7" class="text-center text-danger py-4">
                        <i class="bi bi-exclamation-triangle me-2"></i>Error loading faculty data
                        <div class="small text-muted mt-1">${xhr.status} ${xhr.statusText}</div>
                    </td>
                </tr>
            `);
        }
    });
}

// Function to toggle add faculty form
function toggleAddFacultyForm(show = null) {
    const formContainer = $('#addFacultyFormContainer');
    const toggleBtn = $('#toggleAddFaculty');
    
    if (show === null) {
        show = formContainer.is(':hidden');
    }
    
    if (show) {
        formContainer.slideDown('fast');
        toggleBtn.html('<i class="bi bi-dash-lg me-1"></i> Hide Form');
        toggleBtn.removeClass('btn-primary').addClass('btn-outline-secondary');
        
        // Scroll to form
        $('html, body').animate({
            scrollTop: formContainer.offset().top - 20
        }, 300);
        
        // Focus on first input
        $('#facultyName').focus();
    } else {
        formContainer.slideUp('fast');
        toggleBtn.html('<i class="bi bi-plus-lg me-1"></i> Add Faculty');
        toggleBtn.removeClass('btn-outline-secondary').addClass('btn-primary');
    }
}

// Helper function to validate email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Helper function to show alerts
function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    // Remove any existing alerts
    $('.alert-dismissible').alert('close');
    
    // Add new alert at the top of the container
    $('.container').prepend(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        $('.alert-dismissible').alert('close');
    }, 5000);
}

// Document ready handler
$(document).ready(function() {
    console.log('Document ready');
    
    // Toggle add faculty form
    $('#toggleAddFaculty, #toggleAddFacultyNav').on('click', function(e) {
        e.preventDefault();
        toggleAddFacultyForm();
    });
    
    // Close form when clicking the X button
    $('#closeAddFacultyForm, #cancelAddFaculty').on('click', function() {
        toggleAddFacultyForm(false);
    });
    
    // Auto-format initials to uppercase
    $('#facultyInitials').on('input', function() {
        this.value = this.value.toUpperCase();
    });
    
    // Handle department selection
    $(document).on('click', '.department-item', function(e) {
        e.preventDefault();
        
        // Update active state with visual feedback
        $('.department-item').removeClass('active');
        const $this = $(this);
        $this.addClass('active');
        
        const departmentId = $this.data('dept-id');
        const departmentName = $this.find('.department-name').text().trim() || $this.text().trim();
        
        // Load faculty for selected department
        loadFaculty(departmentId, departmentName);
    });
    
    // Add form submission
    $('#addFacultyForm').on('submit', function(e) {
        e.preventDefault();
        
        if (!currentDepartmentId) {
            showAlert('Please select a department first', 'warning');
            return;
        }
        
        const facultyData = {
            name: $('#facultyName').val().trim(),
            initials: $('#facultyInitials').val().trim(),
            designation: $('#facultyDesignation').val().trim(),
            phone: $('#facultyPhone').val().trim(),
            email: $('#facultyEmail').val().trim()
        };
        
        // Validation
        if (!facultyData.name) {
            showAlert('Full name is required', 'warning');
            $('#facultyName').focus();
            return;
        }
        
        if (!facultyData.initials) {
            showAlert('Initials are required', 'warning');
            $('#facultyInitials').focus();
            return;
        }
        
        if (!facultyData.designation) {
            showAlert('Please select a designation', 'warning');
            $('#facultyDesignation').focus();
            return;
        }
        
        if (!facultyData.phone) {
            showAlert('Phone number is required', 'warning');
            $('#facultyPhone').focus();
            return;
        }
        
        if (!facultyData.email) {
            showAlert('Email is required', 'warning');
            $('#facultyEmail').focus();
            return;
        }
        
        if (!isValidEmail(facultyData.email)) {
            showAlert('Please enter a valid email address', 'warning');
            $('#facultyEmail').focus();
            return;
        }
        
        // Disable submit button and show loading state
        const $submitBtn = $(this).find('button[type="submit"]');
        const originalBtnText = $submitBtn.html();
        $submitBtn.prop('disabled', true).html('<span class="spinner-border spinner-border-sm me-1"></span> Adding...');
        
        // Send data to server
        $.ajax({
            url: `/api/faculty/${encodeURIComponent(currentDepartmentId)}/add`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(facultyData),
            success: function(response) {
                console.log('Faculty added:', response);
                // Reload faculty list
                $(`.department-item[data-dept-id="${currentDepartmentId}"]`).click();
                
                // Reset form
                $('#addFacultyForm')[0].reset();
                toggleAddFacultyForm(false);
                
                // Show success message
                showAlert('Faculty member added successfully!', 'success');
            },
            error: function(xhr, status, error) {
                console.error('Error adding faculty:', error);
                const errorMsg = xhr.responseJSON && xhr.responseJSON.message 
                    ? xhr.responseJSON.message 
                    : 'Error adding faculty member';
                showAlert(errorMsg, 'danger');
            },
            complete: function() {
                // Re-enable submit button
                $submitBtn.prop('disabled', false).html(originalBtnText);
            }
        });
    });
    
    // Toggle faculty status (lock/unlock)
    $(document).on('click', '.toggle-status', function() {
        if (!currentDepartmentId) return;
        
        const $btn = $(this);
        const index = $btn.data('index');
        const $row = $btn.closest('tr');
        const isActive = $row.find('.badge').hasClass('bg-success');
        
        // Show loading state
        const originalHtml = $btn.html();
        $btn.html('<span class="spinner-border spinner-border-sm"></span>');
        
        // Send request to toggle status
        $.ajax({
            url: `/api/faculty/${encodeURIComponent(currentDepartmentId)}/toggle_status`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ index: index }),
            success: function(response) {
                console.log('Status toggled:', response);
                // Reload faculty list
                $(`.department-item[data-dept-id="${currentDepartmentId}"]`).click();
                
                // Show success message
                showAlert(`Faculty member ${response.isActive ? 'unlocked' : 'locked'} successfully!`, 'success');
            },
            error: function(xhr, status, error) {
                console.error('Error toggling status:', error);
                showAlert('Error updating faculty status', 'danger');
                $btn.html(originalHtml);
            }
        });
    });
    
    // Log jQuery version for debugging
    console.log('jQuery version:', $.fn.jquery);
});
