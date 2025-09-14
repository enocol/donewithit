
  function scrollCategories(distance) {
    const container = document.querySelector('.category-container');
    container.scrollBy({ left: distance, behavior: 'auto' });
  }

 // Hide spinner when page fully loads
  window.onload = function() {
    const spinner = document.getElementById("loading-spinner");
    spinner.style.visibility = "hidden";
  };

  // Show spinner immediately when page starts loading
  document.addEventListener("DOMContentLoaded", function() {
    const spinner = document.getElementById("loading-spinner");
    spinner.style.visibility = "visible";
  });