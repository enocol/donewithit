
  function scrollCategories(distance) {
    const container = document.querySelector('.category-container');
    container.scrollBy({ left: distance, behavior: 'auto' });
  }

