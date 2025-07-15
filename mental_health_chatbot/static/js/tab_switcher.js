// Function to switch to a specific tab
function switchToTab(tabIndex) {
    // Wait for the DOM to be fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            performTabSwitch(tabIndex);
        });
    } else {
        // DOM is already ready
        performTabSwitch(tabIndex);
    }
}

// Helper function to perform the actual tab switch
function performTabSwitch(tabIndex) {
    // Add a small delay to ensure the tabs are rendered
    setTimeout(function() {
        const tabs = document.querySelectorAll('[data-baseweb="tab"]');
        if (tabs && tabs.length > tabIndex) {
            tabs[tabIndex].click();
            console.log("Tab switched to index: " + tabIndex);
        } else {
            console.log("Tab not found. Available tabs: " + tabs.length);
        }
    }, 100);
}

// Switch to the first tab (Current Chat)
function switchToCurrentChatTab() {
    switchToTab(0);
}

// Switch to the second tab (Previous Chats)
function switchToPreviousChatsTab() {
    switchToTab(1);
}
