
  function scrollCategories(distance) {
    const container = document.querySelector('.category-container');
    container.scrollBy({ left: distance, behavior: 'auto' });
  }

 
  window.onload = function() {
    const spinner = document.getElementById("loading-spinner");
    spinner.style.visibility = "hidden";
  };

  
  document.addEventListener("DOMContentLoaded", function() {
    const spinner = document.getElementById("loading-spinner");
    spinner.style.visibility = "visible";
  });