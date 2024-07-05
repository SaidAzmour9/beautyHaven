/* global bootstrap: false */
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelectorAll('.nav-link').forEach(navLink => navLink.classList.remove('active'));
    link.classList.add('active');
  });
});

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
      const alerts = document.querySelectorAll('.alert');
      alerts.forEach(alert => {
          alert.style.opacity = '0';
          setTimeout(() => {
              alert.classList.add('hidden');
          }, 600); // Match the transition duration
      });
  }, 3000); // 3 seconds
});