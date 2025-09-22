# Image History Sidebar Implementation Plan

## Overview
Implement a left-side panel displaying previously generated images with visual thumbnails, allowing users to navigate through their generation history. The sidebar will initially be hidden and appear after the first image generation, with automatic scrolling for more than 4 images.

## Current State Analysis

### Key Discoveries:
- Application uses vanilla JavaScript (no React/Vue) - `frontend/static/js/app.js`
- Main UI structure in `frontend/templates/index.html`
- No existing state management for history - all state is DOM-based
- CSS uses CSS Grid and Flexbox patterns - `frontend/static/css/styles.css`
- Generated images stored in `results/` directory with UUID filenames

### Existing Patterns to Follow:
- Container visibility using `style="display: none;"` pattern
- Event handling centralized in app.js initialization
- CSS variables for consistent theming (already defined in `:root`)
- Responsive design using CSS Grid

## Desired End State

Users will see a clean left sidebar showing thumbnail previews of all generated images during their session. The sidebar:
- Appears automatically after first image generation
- Shows up to 4 images without scrolling
- Provides smooth scroll for 5+ images
- Allows clicking thumbnails to view full images
- Maintains visual consistency with existing design

### Verification:
- Sidebar hidden on page load
- Appears after first generation
- Shows image thumbnails, not text links
- Scrollbar appears at 5+ images
- Clicking thumbnails loads that image

## What We're NOT Doing

- Server-side persistence (only browser localStorage)
- Image deletion functionality
- Image metadata display (timestamps, prompts)
- Drag and drop reordering
- Export/import of history
- Cross-browser session sync

## Implementation Approach

Use vanilla JavaScript with localStorage for persistence, following existing DOM manipulation patterns. Leverage CSS Grid for responsive layout matching the reference design.

## Phase 1: HTML Structure & CSS Layout

### Overview
Create the sidebar structure and styling to match the reference design exactly.

### Changes Required:

#### 1. HTML Structure
**File**: `frontend/templates/index.html`
**Changes**: Add sidebar HTML after opening body tag (line 9)

```html
<!-- Image History Sidebar -->
<aside class="image-history-sidebar" id="imageHistorySidebar" style="display: none;">
    <div class="sidebar-header">
        <h3>Recent AI Generated Images</h3>
    </div>
    <div class="sidebar-content" id="sidebarContent">
        <div class="history-grid" id="historyGrid">
            <!-- Dynamic images will be inserted here -->
        </div>
    </div>
</aside>

<!-- Add wrapper for main content -->
<div class="main-content-wrapper" id="mainContentWrapper">
    <!-- Existing main content starting from line 10 -->
```

Close the wrapper div before closing body tag.

#### 2. CSS Styling
**File**: `frontend/static/css/styles.css`
**Changes**: Add sidebar styles at end of file

```css
/* Image History Sidebar */
.image-history-sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: 180px;
    height: 100vh;
    background-color: var(--secondary-color);
    border-right: 1px solid var(--border-color);
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
    z-index: 100;
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
}

.image-history-sidebar.hidden {
    transform: translateX(-100%);
}

.sidebar-header {
    padding: 1.5rem 1rem;
    border-bottom: 1px solid var(--border-color);
}

.sidebar-header h3 {
    font-size: 0.875rem;
    color: var(--text-color);
    margin: 0;
    text-align: center;
}

.sidebar-content {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
}

.history-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.history-item {
    position: relative;
    cursor: pointer;
    border-radius: var(--radius);
    overflow: hidden;
    background-color: white;
    border: 2px solid transparent;
    transition: all 0.2s ease;
    aspect-ratio: 1;
}

.history-item:hover {
    border-color: var(--primary-color);
    box-shadow: var(--shadow);
}

.history-item.active {
    border-color: var(--primary-color);
}

.history-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Main content adjustment when sidebar is visible */
.main-content-wrapper {
    transition: margin-left 0.3s ease;
}

.main-content-wrapper.with-sidebar {
    margin-left: 180px;
}

/* Custom scrollbar for sidebar */
.sidebar-content::-webkit-scrollbar {
    width: 6px;
}

.sidebar-content::-webkit-scrollbar-track {
    background: var(--secondary-color);
}

.sidebar-content::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}

.sidebar-content::-webkit-scrollbar-thumb:hover {
    background: var(--light-text);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .image-history-sidebar {
        width: 120px;
    }

    .main-content-wrapper.with-sidebar {
        margin-left: 120px;
    }
}
```

### Success Criteria:

#### Automated Verification:
- [x] HTML validates without errors: Open in browser, check console
- [x] CSS loads correctly: Check browser DevTools Network tab
- [x] No JavaScript errors: Check browser console

#### Manual Verification:
- [x] Sidebar structure renders (hidden by default)
- [x] CSS styling matches reference design
- [x] Scrollbar styling appears correctly
- [x] Main content wrapper adjusts properly

---

## Phase 2: JavaScript State Management

### Overview
Implement localStorage-based history management with dynamic sidebar updates.

### Changes Required:

#### 1. History Management Module
**File**: `frontend/static/js/app.js`
**Changes**: Add history management functions after line 10 (constants section)

```javascript
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
        document.getElementById('resultContainer').style.display = 'block';

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
```

#### 2. Integration with Generation Flow
**File**: `frontend/static/js/app.js`
**Changes**: Modify generateImage function (around line 209) to add to history

```javascript
// After line 209 where resultImage.src is set
resultImage.src = imageUrl;
addToHistory(imageUrl); // Add this line
```

#### 3. Initialization
**File**: `frontend/static/js/app.js`
**Changes**: Add to window load event (around line 471)

```javascript
window.addEventListener('load', () => {
    initElements();
    setupEventListeners();
    initializeHistory(); // Add this line

    // Enable generate button when prompt has content
    if (promptInput) {
        promptInput.addEventListener('input', checkGenerateButton);
        checkGenerateButton();
    }
});
```

### Success Criteria:

#### Automated Verification:
- [x] No JavaScript errors in console
- [x] localStorage operations work correctly
- [x] History persists across page refreshes

#### Manual Verification:
- [x] History items added on generation
- [x] Sidebar appears after first image
- [x] History limited to 20 items
- [x] Active item highlighted correctly

---

## Phase 3: Integration & User Interactions

### Overview
Complete integration with modify flow and enhance user interactions.

### Changes Required:

#### 1. Modify Flow Integration
**File**: `frontend/static/js/app.js`
**Changes**: Update applyChangesToImage function (around line 444) to add to history

```javascript
// After line 444 where resultImage.src is set
resultImage.src = imageUrl;
addToHistory(imageUrl); // Add this line
```

#### 2. Clear History Option
**File**: `frontend/templates/index.html`
**Changes**: Add clear button to sidebar header

```html
<div class="sidebar-header">
    <h3>Recent AI Generated Images</h3>
    <button id="clearHistoryBtn" class="btn-text" style="font-size: 0.75rem; margin-top: 0.5rem;">Clear All</button>
</div>
```

**File**: `frontend/static/js/app.js`
**Changes**: Add clear history function and event listener

```javascript
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

// Add to setupEventListeners function
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener('click', clearHistory);
}
```

### Success Criteria:

#### Automated Verification:
- [x] Modified images added to history
- [x] Clear function removes localStorage data
- [x] Event listeners attached correctly

#### Manual Verification:
- [x] Click on history items loads them
- [x] Modify flow adds to history
- [x] Clear button works with confirmation
- [x] Smooth animations on all transitions

---

## Phase 4: Testing & Polish

### Overview
Comprehensive testing and final polish.

### Testing Strategy

#### Edge Cases:
- 0 images (sidebar hidden)
- 1-4 images (no scroll)
- 5+ images (scroll appears)
- 20+ images (limit enforced)
- Invalid localStorage data
- Missing image files

#### Browser Testing:
- Chrome/Edge (primary)
- Firefox
- Safari
- Mobile responsive

### Performance Optimizations:
- Lazy loading for thumbnails
- Debounced scroll events
- Optimized re-renders

### Success Criteria:

#### Automated Verification:
- [x] All existing tests still pass
- [x] No memory leaks in DevTools
- [x] Page load time < 2s

#### Manual Verification:
- [x] Sidebar matches reference design exactly
- [x] Smooth scrolling with 10+ images
- [x] Responsive on mobile devices
- [x] No layout shifts on sidebar toggle
- [x] Images load quickly in sidebar
- [x] History persists correctly

---

## Migration Notes

No data migration needed as this is a new feature. Users will start with empty history.

## Performance Considerations

- Thumbnail generation could be added server-side for faster sidebar loading
- Consider virtual scrolling if history grows beyond 50 items
- Implement image caching strategy for frequently accessed images

## References

- Original ticket: `tickets/back_button.md`
- Reference design: `tickets/backbtnimg.png`
- Similar sidebar pattern: `frontend/templates/index.html:95-112` (loading container structure)