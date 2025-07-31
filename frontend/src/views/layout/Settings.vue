<template>
  <div>
    <!-- Main floating button -->
    <div
      ref="floatingButton"
      class="settings-button ml-6 -mt-4"
      :style="{
        top: `${position.top}px`,
        left: `${position.left}px`
      }"
      @mousedown="handleMouseDown"
      @touchstart="handleTouchStart"
    >
      <!-- Button content -->
      <button
        class="button-content"
        @click="handleManualClick"
      >
        <BookOpen class="icon" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen } from 'lucide-vue-next';

// Vue Router
const router = useRouter();

// Default position constants
const DEFAULT_X = 30;
const DEFAULT_Y = 30;
const BUTTON_SIZE = 56;
const POSITION_THRESHOLD = 20; // Threshold for considering button "back in position"

// State
const position = ref({
  top: 0,
  left: 0
});
const defaultPosition = ref({
  top: 0,
  left: 0
});
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });
const floatingButton = ref(null);
const window = globalThis.window;
const clickStartTime = ref(0);
const clickStartPosition = ref({ x: 0, y: 0 });

// Calculate default position (bottom-right corner)
const calculateDefaultPosition = () => {
  return {
    top: window.innerHeight - BUTTON_SIZE - DEFAULT_Y,
    left: window.innerWidth - BUTTON_SIZE - DEFAULT_X
  };
};

// Check if position is close to default
const isNearDefaultPosition = (pos) => {
  return Math.abs(pos.top - defaultPosition.value.top) < POSITION_THRESHOLD && 
         Math.abs(pos.left - defaultPosition.value.left) < POSITION_THRESHOLD;
};

// Handle manual click - navigate to manual guide
const handleManualClick = (e) => {
  // Only navigate if not dragging
  if (!isDragging.value) {
    e.stopPropagation();
    console.log('Navigating to manual guide page...');
    
    // Navigate to manual guide route
    try {
      router.push('/manual-guide');
    } catch (error) {
      console.error('Navigation error:', error);
      // Fallback navigation method
      window.location.href = '/manual-guide';
    }
  }
};

// Reset position to default (bottom-right corner)
const resetPosition = () => {
  position.value = { ...defaultPosition.value };
};

// Mouse down handler - separate from touch
const handleMouseDown = (event) => {
  // Record start time and position for drag detection
  clickStartTime.value = Date.now();
  clickStartPosition.value = { x: event.clientX, y: event.clientY };
  
  // Setup drag handling
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
};

// Touch start handler
const handleTouchStart = (event) => {
  // Prevent default to avoid scrolling
  event.preventDefault();
  
  // Record start time and position for drag detection
  clickStartTime.value = Date.now();
  clickStartPosition.value = { 
    x: event.touches[0].clientX, 
    y: event.touches[0].clientY 
  };
  
  // Setup drag handling
  document.addEventListener('touchmove', handleTouchMove, { passive: false });
  document.addEventListener('touchend', handleTouchEnd);
};

// Mouse move handler
const handleMouseMove = (event) => {
  // Start dragging if mouse has moved enough
  const deltaX = Math.abs(event.clientX - clickStartPosition.value.x);
  const deltaY = Math.abs(event.clientY - clickStartPosition.value.y);
  
  if (deltaX > 5 || deltaY > 5) {
    startDrag(event);
    document.removeEventListener('mousemove', handleMouseMove);
  }
};

// Touch move handler
const handleTouchMove = (event) => {
  // Prevent scrolling
  event.preventDefault();
  
  // Start dragging if touch has moved enough
  const deltaX = Math.abs(event.touches[0].clientX - clickStartPosition.value.x);
  const deltaY = Math.abs(event.touches[0].clientY - clickStartPosition.value.y);
  
  if (deltaX > 5 || deltaY > 5) {
    startDrag(event);
    document.removeEventListener('touchmove', handleTouchMove);
  }
};

// Mouse up handler
const handleMouseUp = (event) => {
  // Clean up listeners
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
  
  // If it was a quick tap without much movement, it's a click
  const deltaTime = Date.now() - clickStartTime.value;
  const deltaX = Math.abs(event.clientX - clickStartPosition.value.x);
  const deltaY = Math.abs(event.clientY - clickStartPosition.value.y);
  
  if (deltaTime < 200 && deltaX < 5 && deltaY < 5) {
    // It's a click, not a drag
    handleManualClick(event);
  }
};

// Touch end handler
const handleTouchEnd = (event) => {
  // Clean up listeners
  document.removeEventListener('touchmove', handleTouchMove);
  document.removeEventListener('touchend', handleTouchEnd);
  
  // If it was a quick tap without much movement, it's a click
  const deltaTime = Date.now() - clickStartTime.value;
  
  if (deltaTime < 200 && !isDragging.value) {
    // It's a tap, not a drag
    handleManualClick(event);
  }
};

// Start dragging
const startDrag = (event) => {
  isDragging.value = true;
  
  // Get the current button position
  const rect = floatingButton.value.getBoundingClientRect();
  
  // Get the mouse/touch position
  const clientX = event.clientX || (event.touches && event.touches[0].clientX);
  const clientY = event.clientY || (event.touches && event.touches[0].clientY);
  
  // Calculate the offset between mouse position and button position
  dragOffset.value = {
    x: clientX - rect.left,
    y: clientY - rect.top
  };
  
  // Add event listeners for drag and end drag events
  if (event.type === 'mousemove') {
    document.addEventListener('mousemove', onDrag);
    document.addEventListener('mouseup', stopDrag);
  } else if (event.type === 'touchmove') {
    document.addEventListener('touchmove', onDrag, { passive: false });
    document.addEventListener('touchend', stopDrag);
  }
};

// Handle drag
const onDrag = (event) => {
  if (!isDragging.value) return;
  
  // Prevent default to avoid scrolling while dragging
  event.preventDefault();
  
  // Get the current mouse/touch position
  const clientX = event.clientX || (event.touches && event.touches[0].clientX);
  const clientY = event.clientY || (event.touches && event.touches[0].clientY);
  
  // Calculate new position
  const newLeft = clientX - dragOffset.value.x;
  const newTop = clientY - dragOffset.value.y;
  
  // Update position with bounds checking
  position.value = {
    top: Math.max(0, Math.min(newTop, window.innerHeight - BUTTON_SIZE)),
    left: Math.max(0, Math.min(newLeft, window.innerWidth - BUTTON_SIZE))
  };
};

// Stop dragging
const stopDrag = () => {
  if (isDragging.value) {
    isDragging.value = false;
    
    // Check if button is near default position and snap it back if it is
    if (isNearDefaultPosition(position.value)) {
      position.value = { ...defaultPosition.value };
    }
    
    // Remove event listeners
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);
    document.removeEventListener('touchmove', onDrag);
    document.removeEventListener('touchend', stopDrag);
  }
};

// Handle window resize
const handleResize = () => {
  // Update default position
  defaultPosition.value = calculateDefaultPosition();
  
  // Ensure button stays within viewport
  const maxTop = window.innerHeight - BUTTON_SIZE;
  const maxLeft = window.innerWidth - BUTTON_SIZE;
  
  position.value = {
    top: Math.min(position.value.top, maxTop),
    left: Math.min(position.value.left, maxLeft)
  };
};

// Initialize component
onMounted(() => {
  // Set default position
  defaultPosition.value = calculateDefaultPosition();
  
  // Always set to default position on page load
  resetPosition();
  
  // Handle window resize
  window.addEventListener('resize', handleResize);
  
  // Add double-click to reset
  floatingButton.value.addEventListener('dblclick', resetPosition);
});

onBeforeUnmount(() => {
  // Clean up event listeners
  document.removeEventListener('mousemove', handleMouseMove);
  document.removeEventListener('mouseup', handleMouseUp);
  document.removeEventListener('touchmove', handleTouchMove);
  document.removeEventListener('touchend', handleTouchEnd);
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
  document.removeEventListener('touchmove', onDrag);
  document.removeEventListener('touchend', stopDrag);
  window.removeEventListener('resize', handleResize);
  
  if (floatingButton.value) {
    floatingButton.value.removeEventListener('dblclick', resetPosition);
  }
});
</script>

<style scoped>
/* Settings button */
.settings-button {
  position: fixed;
  z-index: 50;
  width: 56px;
  height: 56px;
  border-radius: 9999px;
  background-color: #10b981; /* emerald-500 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2), 0 0 0 2px rgba(16, 185, 129, 0.3);
  transition: all 0.2s ease;
  touch-action: none; /* Prevent scrolling when touching the button on mobile */
  user-select: none; /* Prevent text selection during drag */
}

.settings-button:hover {
  background-color: #059669; /* emerald-600 */
  transform: scale(1.05);
}

.settings-button:active {
  transform: scale(0.95);
}

/* Button content */
.button-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  z-index: 2;
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer; /* Show pointer cursor for the button */
  transition: all 0.2s ease;
}

.button-content:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

/* Icon */
.icon {
  width: 24px;
  height: 24px;
  color: white;
  pointer-events: none;
  transition: all 0.2s ease;
}

/* Media queries for responsive design */
/* @media (max-width: 640px) {
  .settings-button {
    width: 48px;
    height: 48px;
  }
  
  .icon {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 480px) {
  .settings-button {
    width: 44px;
    height: 44px;
  }
  
  .icon {
    width: 18px;
    height: 18px;
  }
} */

/* High DPI displays */
@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
  .settings-button {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(16, 185, 129, 0.2);
  }
}

/* Reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .settings-button,
  .button-content,
  .icon {
    transition: none;
  }
}

/* Focus styles for accessibility */
.button-content:focus-visible {
  outline: 2px solid #ffffff;
  outline-offset: 2px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .settings-button {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4), 0 0 0 2px rgba(16, 185, 129, 0.4);
  }
}
</style>