// DVT Test Report Generator - File Upload JavaScript

// Handle modification details conditional display
function setupModificationDetails() {
    const modifiedYes = document.getElementById('modified_yes');
    const modifiedNo = document.getElementById('modified_no');
    const modificationDetails = document.getElementById('modification_details');
    const modificationTextarea = document.getElementById('modification_description');
    
    if (modifiedYes && modifiedYes.checked) {
        modificationDetails.style.display = 'block';
        modificationTextarea.required = true;
    } else if (modifiedNo && modifiedNo.checked) {
        modificationDetails.style.display = 'none';
        modificationTextarea.required = false;
        modificationTextarea.value = ''; // Clear the textarea
    }
}

// Handle upload area clicks intelligently
function handleUploadAreaClick(event, inputId) {
    // Check if the click target is a button or inside a button
    const target = event.target;
    const isButton = target.tagName === 'BUTTON' || target.closest('button');
    
    // If not clicking on a button, trigger file selection
    if (!isButton) {
        document.getElementById(inputId).click();
    }
}

// File upload enhancements
function setupFileUpload(uploadArea, inputId) {
    const input = document.getElementById(inputId);
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            input.files = files;
            updateUploadDisplay(uploadArea, files);
            uploadArea.classList.add('file-selected');
        }
    });
    
    input.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            updateUploadDisplay(uploadArea, e.target.files);
            uploadArea.classList.add('file-selected');
        }
    });
}

function updateUploadDisplay(area, files) {
    const input = area.querySelector('input[type="file"]');
    const isMultiple = input.hasAttribute('multiple');
    
    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Generate file list HTML
    let fileListHTML = '';
    if (isMultiple && files.length > 1) {
        fileListHTML = `
            <div class="mb-2">
                <strong><i class="fas fa-check-circle text-success me-2"></i>${files.length} files selected:</strong>
            </div>
            <div class="file-list">
        `;
        Array.from(files).forEach(file => {
            fileListHTML += `
                <div class="file-item d-flex justify-content-between align-items-center mb-1">
                    <span class="text-truncate me-2">
                        <i class="fas fa-file-excel text-success me-1"></i>
                        ${file.name}
                    </span>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
            `;
        });
        fileListHTML += '</div>';
    } else {
        const file = files[0];
        const icon = file.name.endsWith('.docx') ? 'fa-file-word text-primary' : 'fa-file-excel text-success';
        fileListHTML = `
            <div class="file-selected">
                <i class="fas fa-check-circle fa-2x text-success mb-3"></i>
                <div class="mb-2">
                    <strong>File Selected:</strong>
                </div>
                <div class="file-info d-flex justify-content-between align-items-center p-2 bg-light rounded">
                    <span class="text-truncate me-2">
                        <i class="fas ${icon} me-2"></i>
                        ${file.name}
                    </span>
                    <small class="text-muted">${formatFileSize(file.size)}</small>
                </div>
            </div>
        `;
    }
    
    // Update display with file information
    area.innerHTML = `
        ${fileListHTML}
        <div class="mt-3">
            <button type="button" class="btn btn-outline-primary btn-sm me-2" onclick="changeFiles(event, '${input.id}')">
                <i class="fas fa-exchange-alt me-1"></i>Change Files
            </button>
            <button type="button" class="btn btn-outline-secondary btn-sm" onclick="clearFiles(event, '${input.id}')">
                <i class="fas fa-times me-1"></i>Remove
            </button>
        </div>
    `;
    
    // Re-append the input element (hidden)
    input.style.display = 'none';
    area.appendChild(input);
}

function changeFiles(event, inputId) {
    // Prevent event bubbling to parent elements
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    // Trigger file selection dialog
    document.getElementById(inputId).click();
}

function clearFiles(event, inputId) {
    // Prevent event bubbling to parent elements
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    
    const input = document.getElementById(inputId);
    const area = input.closest('.upload-area');
    
    // Reset input
    input.value = '';
    
    // Remove file-selected class
    area.classList.remove('file-selected');
    
    // Reset display
    if (inputId === 'protocol_file') {
        area.innerHTML = `
            <i class="fas fa-file-word fa-3x text-muted mb-3"></i>
            <p class="mb-2">Click to upload protocol document</p>
            <small class="text-muted">Accepted: DOCX files</small>
        `;
    } else {
        area.innerHTML = `
            <i class="fas fa-file-excel fa-3x text-muted mb-3"></i>
            <p class="mb-2">Click to upload test data</p>
            <small class="text-muted">Accepted: XLSX files (multiple allowed)</small>
        `;
    }
    
    // Re-add input element
    area.appendChild(input);
    
    // Re-setup event listeners
    setupFileUpload(area, inputId);
}

// Initialize upload areas when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing upload areas...');
    
    const protocolArea = document.querySelector('.upload-area');
    const dataArea = document.querySelectorAll('.upload-area')[1];
    
    setupFileUpload(protocolArea, 'protocol_file');
    setupFileUpload(dataArea, 'data_files');
    
    // Form submission handling
    document.getElementById('reportForm').addEventListener('submit', function(e) {
        console.log('=== FORM SUBMISSION STARTED ===');
        
        // Update chronology data before validation
        console.log('Calling updateChronologyData() before validation...');
        updateChronologyData();
        
        // Update form with selected images
        console.log('Updating form with selected images...');
        updateFormSubmissionForImages();
        
        // Check the hidden input value after update
        const hiddenInput = document.getElementById('test_execution_chronology');
        console.log('Hidden input value after update:', hiddenInput ? hiddenInput.value : 'NOT FOUND');
        console.log('Selected images count:', selectedImageFiles.length);
        
        // Automatically add RPT- prefix to report number if not already present
        const reportNumberInput = document.getElementById('report_number');
        if (reportNumberInput.value && !reportNumberInput.value.startsWith('RPT-')) {
            // Create a hidden input with the full report number
            const hiddenInput = document.createElement('input');
            hiddenInput.type = 'hidden';
            hiddenInput.name = 'report_number';
            hiddenInput.value = 'RPT-' + reportNumberInput.value;
            this.appendChild(hiddenInput);
            
            // Disable the original input to prevent duplicate submission
            reportNumberInput.disabled = true;
        }
        
        // Validate required fields
        console.log('Starting validation...');
        const requiredFields = [
            { id: 'title', name: 'Report Title' },
            { id: 'report_number', name: 'Report Number' },
            { id: 'revision', name: 'Revision' },
            { id: 'project_name', name: 'Project Name' },
            { id: 'document_owner', name: 'Document Owner' },
            { id: 'protocol_file', name: 'Protocol Document' }
        ];
        
        const missingFields = [];
        
        // Check text inputs
        requiredFields.slice(0, 5).forEach(field => {
            const input = document.getElementById(field.id);
            if (!input.value.trim()) {
                missingFields.push(field.name);
            }
        });
        
        // Check protocol file
        const protocolFile = document.getElementById('protocol_file');
        if (!protocolFile.files || protocolFile.files.length === 0) {
            missingFields.push('Protocol Document');
        }
        
        // Check test data files (Excel files)
        const dataFiles = document.getElementById('data_files');
        if (!dataFiles.files || dataFiles.files.length === 0) {
            missingFields.push('Test Data Files');
        }
        
        // Check device configuration fields
        const sterilizedRadios = document.querySelectorAll('input[name="units_sterilized"]');
        const sterilizedChecked = Array.from(sterilizedRadios).some(radio => radio.checked);
        if (!sterilizedChecked) {
            missingFields.push('Sterilization Status');
        }
        
        const modifiedRadios = document.querySelectorAll('input[name="units_modified"]');
        const modifiedChecked = Array.from(modifiedRadios).some(radio => radio.checked);
        if (!modifiedChecked) {
            missingFields.push('Modification Status');
        }
        
        // Check calibration verification fields
        const calibrationRadios = document.querySelectorAll('input[name="calibration_verified"]');
        const calibrationChecked = Array.from(calibrationRadios).some(radio => radio.checked);
        if (!calibrationChecked) {
            missingFields.push('Equipment Calibration Verification');
        }
        
        // Check modification description if modification is Yes
        const modifiedYes = document.getElementById('modified_yes');
        const modificationDescription = document.getElementById('modification_description');
        if (modifiedYes && modifiedYes.checked && !modificationDescription.value.trim()) {
            missingFields.push('Modification Details');
        }
        
        // If there are missing fields, show error and prevent submission
        console.log('Missing fields found:', missingFields);
        if (missingFields.length > 0) {
            e.preventDefault();
            
            // Remove any existing error messages
            const existingAlert = document.querySelector('.alert-danger');
            if (existingAlert) {
                existingAlert.remove();
            }
            
            // Create error message
            const errorDiv = document.createElement('div');
            errorDiv.className = 'alert alert-danger mt-3';
            errorDiv.innerHTML = `
                <h6 class="mb-2"><i class="fas fa-exclamation-triangle me-2"></i>Missing Required Fields</h6>
                <p class="mb-2">Please fill in the following required fields marked with <span class="text-danger">*</span>:</p>
                <ul class="mb-0">
                    ${missingFields.map(field => `<li>${field}</li>`).join('')}
                </ul>
            `;
            
            // Insert error message before submit button
            const submitButtonContainer = document.querySelector('.d-grid');
            submitButtonContainer.parentNode.insertBefore(errorDiv, submitButtonContainer);
            
            // Scroll to error message
            errorDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
            
            // Highlight missing fields
            missingFields.forEach(fieldName => {
                const fieldMap = {
                    'Report Title': 'title',
                    'Report Number': 'report_number',
                    'Revision': 'revision',
                    'Project Name': 'project_name',
                    'Document Owner': 'document_owner',
                    'Protocol Document': 'protocol_file',
                    'Test Data Files': 'data_files'
                };
                
                const fieldId = fieldMap[fieldName];
                if (fieldId === 'protocol_file' || fieldId === 'data_files') {
                    // Highlight upload area
                    let uploadArea;
                    if (fieldId === 'protocol_file') {
                        uploadArea = document.querySelector('.upload-area');
                    } else {
                        uploadArea = document.querySelectorAll('.upload-area')[1];
                    }
                    uploadArea.style.borderColor = '#dc3545';
                    uploadArea.style.backgroundColor = '#f8d7da';
                    
                    // Remove highlight after 3 seconds
                    setTimeout(() => {
                        uploadArea.style.borderColor = '';
                        uploadArea.style.backgroundColor = '';
                    }, 3000);
                } else {
                    // Highlight input field
                    const input = document.getElementById(fieldId);
                    input.style.borderColor = '#dc3545';
                    input.style.boxShadow = '0 0 0 0.2rem rgba(220, 53, 69, 0.25)';
                    
                    // Remove highlight after 3 seconds
                    setTimeout(() => {
                        input.style.borderColor = '';
                        input.style.boxShadow = '';
                    }, 3000);
                }
            });
            
            return false;
        }
        
        // If validation passes, proceed with submission
        const submitBtn = document.querySelector('button[type="submit"]');
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating Report...';
        submitBtn.disabled = true;
        
        // Remove any existing error messages
        const existingAlert = document.querySelector('.alert-danger');
        if (existingAlert) {
            existingAlert.remove();
        }
        
        // Show progress message
        const progressDiv = document.createElement('div');
        progressDiv.className = 'alert alert-info mt-3';
        progressDiv.innerHTML = `
            <i class="fas fa-info-circle me-2"></i>
            Processing your files and generating the DVT report. This may take a few moments...
        `;
        this.appendChild(progressDiv);
    });
});

// Test Execution Chronology Functions
function addChronologyRow() {
    console.log('Adding new chronology row...');
    const tbody = document.getElementById('chronologyBody');
    const newRow = document.createElement('tr');
    newRow.className = 'chronology-row';
    newRow.innerHTML = `
        <td><input type="text" class="form-control form-control-sm chronology-step" placeholder="e.g., Distribution Simulation"></td>
        <td><input type="date" class="form-control form-control-sm chronology-start-date"></td>
        <td><input type="date" class="form-control form-control-sm chronology-end-date"></td>
        <td><input type="text" class="form-control form-control-sm chronology-location" placeholder="e.g., Lab A"></td>
        <td><button type="button" class="btn btn-sm btn-outline-danger" onclick="removeChronologyRow(this)"><i class="fas fa-trash"></i></button></td>
    `;
    tbody.appendChild(newRow);
    
    // Re-setup listeners for all inputs including the new row
    setupChronologyListeners();
    updateChronologyData();
    console.log('New chronology row added and listeners updated');
}

function removeChronologyRow(button) {
    console.log('Removing chronology row...');
    const row = button.closest('tr');
    const tbody = document.getElementById('chronologyBody');
    
    // Don't remove the last row - just clear it
    if (tbody.children.length === 1) {
        row.querySelectorAll('input').forEach(input => input.value = '');
        console.log('Cleared last remaining row');
    } else {
        row.remove();
        console.log('Removed chronology row');
    }
    
    // Re-setup listeners after row removal
    setupChronologyListeners();
    updateChronologyData();
}

function updateChronologyData() {
    console.log('📊 CHRONOLOGY DEBUG: updateChronologyData() called - Oct 9 2025 v2.1');
    const rows = document.querySelectorAll('.chronology-row');
    const chronologyData = [];
    
    console.log(`📊 CHRONOLOGY DEBUG: Found ${rows.length} chronology rows`);
    
    rows.forEach((row, index) => {
        const stepInput = row.querySelector('.chronology-step');
        const startDateInput = row.querySelector('.chronology-start-date');
        const endDateInput = row.querySelector('.chronology-end-date');
        const locationInput = row.querySelector('.chronology-location');
        
        console.log(`Row ${index + 1} inputs found:`, {
            stepInput: !!stepInput,
            startDateInput: !!startDateInput,
            endDateInput: !!endDateInput,
            locationInput: !!locationInput
        });
        
        if (!stepInput || !startDateInput || !endDateInput || !locationInput) {
            console.error(`Row ${index + 1} missing input elements!`);
            return;
        }
        
        const step = stepInput.value.trim();
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        const location = locationInput.value.trim();
        
        console.log(`Row ${index + 1} values: step="${step}", startDate="${startDate}", endDate="${endDate}", location="${location}"`);
        
        // Only add non-empty entries
        if (step || startDate || endDate || location) {
            const entry = {
                step: step,
                start_date: startDate,
                end_date: endDate,
                location: location
            };
            chronologyData.push(entry);
            console.log(`Added entry:`, entry);
        } else {
            console.log(`Row ${index + 1} skipped - all fields empty`);
        }
    });
    
    // Update hidden input with JSON data
    const hiddenInput = document.getElementById('test_execution_chronology');
    if (!hiddenInput) {
        console.error('Hidden input test_execution_chronology not found!');
        return;
    }
    
    const jsonData = JSON.stringify(chronologyData);
    hiddenInput.value = jsonData;
    
    console.log(`Final chronology data: ${jsonData}`);
    console.log(`Hidden input value set to: ${hiddenInput.value}`);
    console.log('=== updateChronologyData() completed ===');
}

// Setup chronology event listeners
function setupChronologyListeners() {
    console.log('🔧 CHRONOLOGY DEBUG: Setting up chronology listeners...');
    const chronologyInputs = document.querySelectorAll('.chronology-step, .chronology-start-date, .chronology-end-date, .chronology-location');
    console.log(`🔧 CHRONOLOGY DEBUG: Found ${chronologyInputs.length} chronology inputs`);
    
    if (chronologyInputs.length === 0) {
        console.error('🚨 CHRONOLOGY ERROR: No chronology inputs found! Check HTML structure.');
        return;
    }
    
    chronologyInputs.forEach((input, index) => {
        console.log(`🔧 CHRONOLOGY DEBUG: Setting up listener for input ${index + 1}: ${input.className}`);
        // Remove existing listeners to avoid duplicates
        input.removeEventListener('input', updateChronologyData);
        input.removeEventListener('change', updateChronologyData);
        // Add new listeners
        input.addEventListener('input', updateChronologyData);
        input.addEventListener('change', updateChronologyData);
    });
    
    console.log('🔧 CHRONOLOGY DEBUG: All listeners setup complete');
}

// Initialize chronology functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 CHRONOLOGY DEBUG: DOM loaded - initializing chronology functionality...');
    console.log('🚀 CHRONOLOGY DEBUG: JavaScript version loaded - Oct 10 2025 v3.0');
    
    // Check if hidden input exists
    const hiddenInput = document.getElementById('test_execution_chronology');
    console.log('🚀 CHRONOLOGY DEBUG: Hidden input exists:', !!hiddenInput);
    if (hiddenInput) {
        console.log('🚀 CHRONOLOGY DEBUG: Hidden input initial value:', hiddenInput.value);
    }
    
    // Check if chronology table exists
    const chronologyTable = document.getElementById('chronologyTable');
    console.log('🚀 CHRONOLOGY DEBUG: Chronology table exists:', !!chronologyTable);
    
    // Check initial rows
    const rows = document.querySelectorAll('.chronology-row');
    console.log('🚀 CHRONOLOGY DEBUG: Initial chronology rows found:', rows.length);
    
    // Setup initial listeners
    setupChronologyListeners();
    
    // Initial update to set the hidden input value
    updateChronologyData();
    
    // Initialize image upload functionality
    initializeImageUpload();
    
    console.log('🚀 CHRONOLOGY DEBUG: Chronology initialization completed');
});

// ===== IMAGE UPLOAD FUNCTIONALITY =====

let selectedImageFiles = [];

function initializeImageUpload() {
    console.log('🖼️ IMAGE DEBUG: Initializing image upload functionality...');
    
    // Check if upload area exists
    const uploadArea = document.getElementById('uploadArea');
    console.log('🖼️ IMAGE DEBUG: Upload area exists:', !!uploadArea);
    
    // Style for drag and drop and hover effects
    if (uploadArea) {
        uploadArea.style.borderColor = '#dee2e6';
        uploadArea.style.transition = 'all 0.3s ease';
        
        // Add hover effect
        uploadArea.addEventListener('mouseenter', function() {
            this.style.borderColor = '#007bff';
            this.style.backgroundColor = '#f8f9fa';
            this.style.transform = 'scale(1.02)';
        });
        
        uploadArea.addEventListener('mouseleave', function() {
            if (!this.classList.contains('drag-over')) {
                this.style.borderColor = '#dee2e6';
                this.style.backgroundColor = 'transparent';
                this.style.transform = 'scale(1)';
            }
        });
        
        // Add click effect
        uploadArea.addEventListener('mousedown', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        uploadArea.addEventListener('mouseup', function() {
            this.style.transform = 'scale(1.02)';
        });
    }
    
    console.log('🖼️ IMAGE DEBUG: Image upload initialization completed');
}

function handleImageSelection(input) {
    console.log('🖼️ IMAGE DEBUG: Image selection triggered, files:', input.files.length);
    
    const files = Array.from(input.files);
    processSelectedImages(files);
}

function handleImageDrop(event) {
    event.preventDefault();
    console.log('🖼️ IMAGE DEBUG: Image drop triggered');
    
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.remove('drag-over');
    uploadArea.style.borderColor = '#dee2e6';
    uploadArea.style.backgroundColor = 'transparent';
    uploadArea.style.transform = 'scale(1)';
    
    const files = Array.from(event.dataTransfer.files);
    processSelectedImages(files);
}

function handleDragOver(event) {
    event.preventDefault();
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.add('drag-over');
    uploadArea.style.borderColor = '#007bff';
    uploadArea.style.backgroundColor = '#e3f2fd';
    uploadArea.style.transform = 'scale(1.02)';
}

function handleDragLeave(event) {
    event.preventDefault();
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.classList.remove('drag-over');
    uploadArea.style.borderColor = '#dee2e6';
    uploadArea.style.backgroundColor = 'transparent';
    uploadArea.style.transform = 'scale(1)';
}

function processSelectedImages(files) {
    console.log('🖼️ IMAGE DEBUG: Processing', files.length, 'selected images');
    
    const validFiles = [];
    const errors = [];
    
    files.forEach((file, index) => {
        console.log(`🖼️ IMAGE DEBUG: Processing file ${index + 1}: ${file.name}, size: ${file.size}, type: ${file.type}`);
        
        // Check file type
        if (!file.type.match(/^image\/(jpeg|jpg|png)$/)) {
            errors.push(`${file.name}: Invalid file type. Only JPG and PNG are supported.`);
            return;
        }
        
        // Check file size (10MB = 10 * 1024 * 1024 bytes)
        if (file.size > 10 * 1024 * 1024) {
            errors.push(`${file.name}: File too large. Maximum size is 10MB.`);
            return;
        }
        
        validFiles.push(file);
    });
    
    if (errors.length > 0) {
        alert('Some files were rejected:\n\n' + errors.join('\n'));
    }
    
    if (validFiles.length > 0) {
        // Add to selected files (avoiding duplicates)
        validFiles.forEach(file => {
            const exists = selectedImageFiles.some(existing => 
                existing.name === file.name && existing.size === file.size
            );
            if (!exists) {
                selectedImageFiles.push(file);
            }
        });
        
        updateImageDisplay();
        console.log('🖼️ IMAGE DEBUG: Total selected images:', selectedImageFiles.length);
    }
}

function updateImageDisplay() {
    const selectedImagesDiv = document.getElementById('selectedImages');
    const imageListDiv = document.getElementById('imageList');
    
    if (selectedImageFiles.length === 0) {
        selectedImagesDiv.style.display = 'none';
        return;
    }
    
    selectedImagesDiv.style.display = 'block';
    imageListDiv.innerHTML = '';
    
    selectedImageFiles.forEach((file, index) => {
        const imageItem = document.createElement('div');
        imageItem.className = 'col-md-4 col-sm-6 mb-3';
        
        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            imageItem.innerHTML = `
                <div class="card">
                    <img src="${e.target.result}" class="card-img-top" style="height: 150px; object-fit: cover;">
                    <div class="card-body p-2">
                        <p class="card-text small mb-1">
                            <strong>${file.name}</strong><br>
                            <span class="text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</span>
                        </p>
                        <button type="button" class="btn btn-sm btn-outline-danger w-100" 
                                onclick="removeImage(${index})">
                            <i class="fas fa-trash me-1"></i>Remove
                        </button>
                    </div>
                </div>
            `;
        };
        reader.readAsDataURL(file);
        
        imageListDiv.appendChild(imageItem);
    });
}

function removeImage(index) {
    console.log('🖼️ IMAGE DEBUG: Removing image at index:', index);
    selectedImageFiles.splice(index, 1);
    updateImageDisplay();
}

// Update form submission to include images
function updateFormSubmissionForImages() {
    const form = document.getElementById('reportForm');
    const fileInput = document.getElementById('analysisImages');
    
    // Clear the file input
    fileInput.value = '';
    
    // Create a new DataTransfer object to set files
    const dt = new DataTransfer();
    selectedImageFiles.forEach(file => {
        dt.items.add(file);
    });
    
    // Set the files to the input
    fileInput.files = dt.files;
    
    console.log('🖼️ IMAGE DEBUG: Updated form with', selectedImageFiles.length, 'images');
}
