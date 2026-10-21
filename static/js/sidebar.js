document.addEventListener("DOMContentLoaded", function() {
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");
  const toggle = document.getElementById("sidebarToggle");
  const profileTrigger = document.getElementById("profileTrigger");
  const profileDropdown = document.getElementById("profileDropdown");
  const notifTrigger = document.getElementById("notifTrigger");
  const notifPanel = document.getElementById("notificationPanel");

  // ── Sidebar Toggle ──
  if (toggle && sidebar && overlay) {
    toggle.addEventListener("click", function(e) {
      e.stopPropagation();
      sidebar.classList.toggle("open");
      overlay.classList.toggle("open");
    });

    overlay.addEventListener("click", function() {
      sidebar.classList.remove("open");
      overlay.classList.remove("open");
    });

    // Close sidebar on Escape
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape" && sidebar.classList.contains("open")) {
        sidebar.classList.remove("open");
        overlay.classList.remove("open");
      }
    });
  }

  // ── Profile Dropdown ──
  if (profileTrigger && profileDropdown) {
    profileTrigger.addEventListener("click", function(e) {
      e.stopPropagation();
      profileDropdown.classList.toggle("open");
      if (notifPanel) notifPanel.classList.remove("open");
    });

    document.addEventListener("click", function(e) {
      if (!profileTrigger.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove("open");
      }
    });
  }

  // ── Notification Panel ──
  if (notifTrigger && notifPanel) {
    notifTrigger.addEventListener("click", function(e) {
      e.stopPropagation();
      notifPanel.classList.toggle("open");
      if (profileDropdown) profileDropdown.classList.remove("open");
    });

    document.addEventListener("click", function(e) {
      if (!notifTrigger.contains(e.target) && !notifPanel.contains(e.target)) {
        notifPanel.classList.remove("open");
      }
    });
  }

  // ── Active Sidebar Item ──
  if (sidebar) {
    const currentPath = window.location.pathname;
    sidebar.querySelectorAll(".sidebar-item").forEach(function(item) {
      const href = item.getAttribute("href");
      if (href && href !== "#" && currentPath.startsWith(href)) {
        item.classList.add("active");
      }
    });
  }
});