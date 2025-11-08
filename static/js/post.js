// Modern vanilla JavaScript - no jQuery needed!

function initImageGallery(post_id) {
    // Find the post card by post ID
    const postCard = document.querySelector(`#images_${post_id}`)?.closest('.post-card') ||
                     Array.from(document.querySelectorAll('.post-card')).find(card => {
                         const imgContainer = card.querySelector(`#images_${post_id}`);
                         const textContent = card.querySelector('.post-text-content');
                         return imgContainer || textContent;
                     });
    
    if (!postCard) {
        console.warn('Post card not found for post_id:', post_id);
        return;
    }
    
    // Find all images in this post card
    const allImages = Array.from(postCard.querySelectorAll('img.post-image'));
    if (allImages.length === 0) {
        return;
    }
    
    // Mark as initialized to prevent duplicate handlers
    if (postCard.dataset.galleryInitialized) {
        return;
    }
    postCard.dataset.galleryInitialized = 'true';
    
    // Wait for PhotoSwipe to be available
    function checkPhotoSwipe() {
        if (typeof PhotoSwipe === 'undefined') {
            console.warn('PhotoSwipe not loaded yet, retrying...');
            setTimeout(checkPhotoSwipe, 100);
            return;
        }
        
        // Initialize click handlers for all images in this post
        allImages.forEach((img, index) => {
            // Skip if already has click handler
            if (img.dataset.clickHandler) {
                return;
            }
            img.dataset.clickHandler = 'true';
            
            img.style.cursor = 'pointer';
            img.setAttribute('title', 'Click to enlarge');
            
            img.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Get all images for this gallery
                const postImages = Array.from(postCard.querySelectorAll('img.post-image'));
                const items = postImages.map((image, idx) => {
                    // Try to get actual dimensions
                    let width = image.naturalWidth || image.width || 1920;
                    let height = image.naturalHeight || image.height || 1080;
                    
                    // If image hasn't loaded, use defaults
                    if (width === 0 || height === 0) {
                        width = 1920;
                        height = 1080;
                    }
                    
                    return {
                        src: image.src,
                        w: width,
                        h: height,
                        alt: image.alt || `Image ${idx + 1}`
                    };
                });
                
                // Find the clicked image index
                const clickedIndex = postImages.indexOf(img);
                
                try {
                    // PhotoSwipe v5 API
                    const gallery = new PhotoSwipe({
                        dataSource: items,
                        index: clickedIndex >= 0 ? clickedIndex : 0,
                        showHideAnimationType: 'fade',
                        zoomAnimationDuration: 300
                    });
                    gallery.init();
                } catch (error) {
                    console.error('Error opening PhotoSwipe:', error);
                    // Fallback: open image in new tab
                    window.open(img.src, '_blank');
                }
            });
        });
    }
    
    checkPhotoSwipe();
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

async function unlike(post, reblog) {
    const btn = event.target.closest('button');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing...';
    
    try {
        const response = await fetch('/api/unlike', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: post,
                reblog_key: reblog
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showNotification('Post unliked successfully!', 'success');
        btn.innerHTML = originalText;
        btn.disabled = false;
    } catch (error) {
        showNotification('Error unliking post: ' + error.message, 'danger');
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

async function like(post, reblog) {
    const btn = event.target.closest('button');
    if (!btn) return;
    
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing...';
    
    try {
        const response = await fetch('/api/relike', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: post,
                reblog_key: reblog
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        showNotification('Post liked successfully!', 'success');
        btn.innerHTML = originalText;
        btn.disabled = false;
    } catch (error) {
        showNotification('Error liking post: ' + error.message, 'danger');
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing image galleries...');
    
    // Wait a bit for images to load
    setTimeout(function() {
        // Initialize image galleries for posts with known IDs from likes list
        if (typeof likes !== 'undefined' && Array.isArray(likes)) {
            likes.forEach(function (s) {
                if (s && s[0]) {
                    try {
                        initImageGallery(s[0]);
                    } catch (error) {
                        console.error('Error initializing image gallery for post', s[0], error);
                    }
                }
            });
        }
        
        // Also find all image containers and initialize them (fallback for any missed posts)
        document.querySelectorAll('[id^="images_"]').forEach(function(container) {
            const postId = container.id.replace('images_', '');
            const hasImages = container.querySelectorAll('img.post-image').length > 0;
            if (hasImages) {
                const postCard = container.closest('.post-card');
                if (postCard && !postCard.dataset.galleryInitialized) {
                    try {
                        initImageGallery(postId);
                    } catch (error) {
                        console.error('Error initializing gallery for container:', error);
                    }
                }
            }
        });
        
        console.log('Image galleries initialized');
    }, 100);
    
    // Initialize Bootstrap tooltips
    try {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = Array.from(tooltipTriggerList).map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    } catch (error) {
        console.error('Error initializing Bootstrap tooltips:', error);
    }
});
