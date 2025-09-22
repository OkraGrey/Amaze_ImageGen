/**
 * Image Generation Web App
 * Frontend JavaScript functionality
 */

// DOM Elements
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const removePreview = document.getElementById('removePreview');
const promptInput = document.getElementById('promptInput');
const generateBtn = document.getElementById('generateBtn');
const attachmentBtn = document.getElementById('attachmentBtn');
const modelSelect = document.getElementById('modelSelect');
const resultContainer = document.getElementById('resultContainer');
const resultImage = document.getElementById('resultImage');
const downloadBtn = document.getElementById('downloadBtn');
const loadingContainer = document.getElementById('loadingContainer');
const generationContainer = document.querySelector('.generation-container');
const generateAgainBtn = document.getElementById('generateAgainBtn');
const reviewPromptText = document.getElementById('reviewPromptText');
const reviewImage = document.getElementById('reviewImage');
const reviewImageContainer = document.getElementById('reviewImageContainer');
const modifyImageBtn = document.getElementById('modifyImageBtn');
const conversationInput = document.getElementById('conversationInput');
const followUpPrompt = document.getElementById('followUpPrompt');
const applyChangesBtn = document.getElementById('applyChangesBtn');
const cancelChangesBtn = document.getElementById('cancelChangesBtn');

// API Endpoint
const UPLOAD_API_URL = '/api/upload';
const DOWNLOAD_API_URL = '/api/download';

// Image History Management
const MAX_HISTORY_ITEMS = 20;
let imageHistory = [];

/**
 * Initialize image history from localStorage
 */
function initializeHistory() {
    const stored = localStorage.getItem('imageHistory');
    if (stored) {
        try {
            imageHistory = JSON.parse(stored);
            if (imageHistory.length > 0) {
                showSidebar();
                renderHistoryItems();
            }
        } catch (e) {
            console.error('Failed to load history:', e);
            imageHistory = [];
        }
    }
}

/**
 * Add image to history
 */
function addToHistory(imagePath) {
    const historyItem = {
        id: Date.now(),
        path: imagePath,
        timestamp: new Date().toISOString(),
        thumbnail: imagePath // In production, might want separate thumbnail
    };

    imageHistory.unshift(historyItem);

    // Limit history size
    if (imageHistory.length > MAX_HISTORY_ITEMS) {
        imageHistory = imageHistory.slice(0, MAX_HISTORY_ITEMS);
    }

    localStorage.setItem('imageHistory', JSON.stringify(imageHistory));

    // Show sidebar on first image
    if (imageHistory.length === 1) {
        showSidebar();
    }

    renderHistoryItems();
}

/**
 * Show sidebar with animation
 */
function showSidebar() {
    const sidebar = document.getElementById('imageHistorySidebar');
    const mainWrapper = document.getElementById('mainContentWrapper');

    if (sidebar && mainWrapper) {
        sidebar.style.display = 'flex';
        setTimeout(() => {
            sidebar.classList.remove('hidden');
            mainWrapper.classList.add('with-sidebar');
        }, 10);
    }
}

/**
 * Hide sidebar
 */
function hideSidebar() {
    const sidebar = document.getElementById('imageHistorySidebar');
    const mainWrapper = document.getElementById('mainContentWrapper');

    if (sidebar && mainWrapper) {
        sidebar.classList.add('hidden');
        mainWrapper.classList.remove('with-sidebar');
        setTimeout(() => {
            sidebar.style.display = 'none';
        }, 300);
    }
}

/**
 * Render history items in sidebar
 */
function renderHistoryItems() {
    const historyGrid = document.getElementById('historyGrid');
    if (!historyGrid) return;

    historyGrid.innerHTML = '';

    imageHistory.forEach(item => {
        const historyElement = document.createElement('div');
        historyElement.className = 'history-item';
        historyElement.dataset.imageId = item.id;

        const img = document.createElement('img');
        img.src = item.path;
        img.alt = 'Generated image';
        img.loading = 'lazy';

        historyElement.appendChild(img);
        historyElement.addEventListener('click', () => loadHistoryImage(item));

        historyGrid.appendChild(historyElement);
    });

    // Mark current image as active
    const currentPath = document.getElementById('resultImage')?.src;
    if (currentPath) {
        markActiveHistoryItem(currentPath);
    }
}

/**
 * Load image from history
 */
function loadHistoryImage(item) {
    const resultImage = document.getElementById('resultImage');
    if (resultImage) {
        resultImage.src = item.path;

        // Show result container
        setGenerationState(false);
        document.getElementById('resultContainer').hidden = false;

        // Mark as active
        markActiveHistoryItem(item.path);
    }
}

/**
 * Mark active history item
 */
function markActiveHistoryItem(imagePath) {
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('active');
    });

    const activeItem = Array.from(document.querySelectorAll('.history-item')).find(item => {
        const img = item.querySelector('img');
        return img && img.src === imagePath;
    });

    if (activeItem) {
        activeItem.classList.add('active');
    }
}

/**
 * Clear all history
 */
function clearHistory() {
    if (confirm('Clear all image history?')) {
        imageHistory = [];
        localStorage.removeItem('imageHistory');
        document.getElementById('historyGrid').innerHTML = '';
        hideSidebar();
    }
}
/**
 * Initialize the application
 */
function init() {
    // Ensure loading container is hidden on page load
    if (loadingContainer) {
        loadingContainer.hidden = true;
        loadingContainer.style.display = 'none';
    }
    
    // Setup event listeners
    attachmentBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    removePreview.addEventListener('click', clearPreview);
    generateBtn.addEventListener('click', generateImage);
    downloadBtn.addEventListener('click', downloadImage);
    generateAgainBtn.addEventListener('click', resetToUploadView);
    modifyImageBtn.addEventListener('click', () => showConversationInput('modify'));
    applyChangesBtn.addEventListener('click', applyChangesToImage);
    cancelChangesBtn.addEventListener('click', hideConversationInput);

    // Initialize history
    initializeHistory();

    // Add clear history button listener
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearHistory);
    }

    // Setup drag and drop on prompt area
    setupDragAndDrop();
}

/**
 * Set up drag and drop functionality
 */
function setupDragAndDrop() {
    const promptContainer = document.querySelector('.prompt-input-container');
    
    if (promptContainer) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            promptContainer.addEventListener(eventName, preventDefaults, false);
        });
        
        ['dragenter', 'dragover'].forEach(eventName => {
            promptContainer.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            promptContainer.addEventListener(eventName, unhighlight, false);
        });
        
        promptContainer.addEventListener('drop', handleDrop, false);
    }
}

/**
 * Prevent default browser behavior
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Highlight drop zone on drag enter/over
 */
function highlight() {
    const promptContainer = document.querySelector('.prompt-input-container');
    if (promptContainer) {
        promptContainer.style.borderColor = 'var(--primary-color)';
        promptContainer.style.backgroundColor = 'rgba(79, 70, 229, 0.05)';
    }
}

/**
 * Remove highlight on drag leave/drop
 */
function unhighlight() {
    const promptContainer = document.querySelector('.prompt-input-container');
    if (promptContainer) {
        promptContainer.style.borderColor = '';
        promptContainer.style.backgroundColor = '';
    }
}

/**
 * Handle file drop
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    
    if (files.length) {
        handleFiles(files);
    }
}

/**
 * Handle file selection from input
 */
function handleFileSelect(e) {
    if (e.target.files.length) {
        handleFiles(e.target.files);
    }
}

/**
 * Process selected files
 */
function handleFiles(files) {
    const file = files[0]; // Only handle the first file
    
    // Validate file type
    if (!file.type.match('image/jpeg') && !file.type.match('image/png')) {
        showError('Please select a JPG or PNG image.');
        return;
    }
    
    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File size must be less than 10MB.');
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewContainer.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

/**
 * Clear image preview
 */
function clearPreview(e) {
    e.stopPropagation();
    previewImage.src = '';
    previewContainer.style.display = 'none';
    fileInput.value = '';
}

/**
 * Generate image from API
 */
async function generateImage() {
    // Validate prompt
    const prompt = promptInput.value.trim();
    if (!prompt) {
        showError('Please enter a prompt for image generation.');
        return;
    }
    
    // Hide the upload section and show loading state
    setGenerationState(true);
    
    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('prompt', prompt);
        formData.append('model', modelSelect.value);
        
        // Add file if available
        if (fileInput.files.length) {
            formData.append('file', fileInput.files[0]);
        }
        
        // Send API request
        const response = await fetch(UPLOAD_API_URL, {
            method: 'POST',
            body: formData
        });
        
        // Process response
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to generate image');
        }
        
        const data = await response.json();
        
        // Display result
        resultImage.src = data.result_path;
        addToHistory(data.result_path); // Add to history
        resultContainer.hidden = false;
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showError(error.message);
        // Restore the upload section if there's an error
        setGenerationState(false);
    } finally {
        // Keep the upload section hidden after successful generation
        setLoading(false);
    }
}

/**
 * Download generated image
 */
async function downloadImage() {
    console.log('[INFO]--- Starting download process ---');

    try {
        // Show loading state
        downloadBtn.disabled = true;
        downloadBtn.textContent = 'Processing...';

        // First, call the backend to process the image with background removal
        console.log('[INFO]--- Calling backend for background removal ---');
        const response = await fetch(DOWNLOAD_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ path: resultImage.src }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to process image');
        }

        const data = await response.json();
        console.log('[INFO]--- Background removal complete, path:', data.path);

        // Now fetch the processed image as a blob
        console.log('[INFO]--- Fetching processed image as blob ---');
        const imageResponse = await fetch(data.path);
        if (!imageResponse.ok) {
            throw new Error('Failed to fetch processed image');
        }

        const blob = await imageResponse.blob();
        console.log('[INFO]--- Image blob received, size:', blob.size);

        // Create a blob URL and trigger download
        const blobUrl = window.URL.createObjectURL(blob);

        // Generate filename with timestamp
        const timestamp = new Date().toISOString().slice(0, 19).replace(/[:]/g, '-');
        const filename = `image-no-bg-${timestamp}.png`;

        // Create download link and trigger it
        const link = document.createElement('a');
        link.href = blobUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        // Clean up the blob URL after a short delay
        setTimeout(() => {
            window.URL.revokeObjectURL(blobUrl);
            console.log('[INFO]--- Blob URL cleaned up ---');
        }, 1000);

        console.log('[INFO]--- Download triggered successfully ---');

    } catch (error) {
        console.error('[ERROR]--- Download failed:', error);
        showError(error.message);
    } finally {
        // Restore button state
        downloadBtn.disabled = false;
        downloadBtn.textContent = 'Download';
    }
}

/**
 * Show/hide loading state
 */
function setLoading(isLoading) {
    if (loadingContainer) {
        loadingContainer.hidden = !isLoading;
        if (isLoading) {
            loadingContainer.style.display = 'flex';
        } else {
            loadingContainer.style.display = 'none';
        }
    }
    if (generateBtn) {
        generateBtn.disabled = isLoading;
    }
}

/**
 * Handle generation state - hide generation section and show loader with review
 */
function setGenerationState(isGenerating) {
    if (generationContainer) {
        if (isGenerating) {
            generationContainer.style.display = 'none';
            // Populate review section
            populateReviewSection();
        } else {
            generationContainer.style.display = 'block';
        }
    }
    setLoading(isGenerating);
}

/**
 * Populate the review section with current prompt and image
 */
function populateReviewSection() {
    // Set the prompt text
    if (reviewPromptText && promptInput) {
        reviewPromptText.textContent = promptInput.value.trim() || 'No prompt provided';
    }
    
    // Set the uploaded image if available
    if (reviewImageContainer && reviewImage && previewImage) {
        if (previewImage.src && !previewImage.hidden) {
            reviewImage.src = previewImage.src;
            reviewImageContainer.style.display = 'block';
        } else {
            reviewImageContainer.style.display = 'none';
        }
    }
}

/**
 * Reset to generation view for generating another image
 */
function resetToUploadView() {
    // Hide result container
    resultContainer.hidden = true;
    
    // Show generation container
    if (generationContainer) {
        generationContainer.style.display = 'block';
    }
    
    // Clear the prompt for a fresh start
    promptInput.value = '';
    
    // Clear any uploaded image
    clearPreview(new Event('click'));
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Show conversation input for modifications
 */
function showConversationInput(type) {
    if (conversationInput && followUpPrompt) {
        conversationInput.style.display = 'block';
        followUpPrompt.placeholder = 'Describe the changes you want to make to this image...';
        followUpPrompt.focus();
    }
}

/**
 * Hide conversation input
 */
function hideConversationInput() {
    if (conversationInput && followUpPrompt) {
        conversationInput.style.display = 'none';
        followUpPrompt.value = '';
    }
}

/**
 * Apply changes to the current image
 */
async function applyChangesToImage() {
    const followUpText = followUpPrompt.value.trim();
    if (!followUpText) {
        showError('Please describe the changes you want to make.');
        return;
    }
    
    // Hide conversation section and show loading
    hideConversationInput();
    resultContainer.hidden = true;
    
    // Set up the review section with the modification request
    reviewPromptText.textContent = `Modify previous image: ${followUpText}`;
    
    // Show the previous generated image in review
    if (reviewImageContainer && reviewImage && resultImage.src) {
        reviewImage.src = resultImage.src;
        reviewImageContainer.style.display = 'block';
    }
    
    setLoading(true);
    
    try {
        // Convert current result image to blob and send with modification request
        const response = await fetch(resultImage.src);
        const blob = await response.blob();
        
        // Prepare form data with the modification request
        const formData = new FormData();
        formData.append('prompt', followUpText);
        formData.append('model', modelSelect.value);
        formData.append('file', blob, 'current-image.png');
        
        // Send API request
        const apiResponse = await fetch(UPLOAD_API_URL, {
            method: 'POST',
            body: formData
        });
        
        // Process response
        if (!apiResponse.ok) {
            const errorData = await apiResponse.json();
            throw new Error(errorData.detail || 'Failed to modify image');
        }
        
        const data = await apiResponse.json();
        
        // Display new result
        resultImage.src = data.result_path;
        addToHistory(data.result_path); // Add to history
        resultContainer.hidden = false;
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
        showError(error.message);
        // Show result container again if there's an error
        resultContainer.hidden = false;
    } finally {
        setLoading(false);
    }
}

/**
 * Show error message
 */
function showError(message) {
    alert(message); // Simple alert for now, can be replaced with a better UI component
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', init);
