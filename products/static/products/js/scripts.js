document.addEventListener("DOMContentLoaded", function() {
        const mainImage = document.getElementById("main-product-image");
        const thumbnails = document.querySelectorAll(".img-fluid");

        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener("click", function() {
                mainImage.src = this.src;
            });
        });
    });