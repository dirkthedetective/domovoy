const imageContainers = document.querySelectorAll('.image-container');
let currentImageIndex = 0;

function showImage(index) {
	imageContainers.forEach((container, i) => {
		container.style.transform = `translateX(-${index * 100}%)`;  // Adjust translateX value
	});
	currentImageIndex = index;
}

document.querySelectorAll('.prev-button').forEach(button => {
	button.addEventListener('click', () => {
		if (currentImageIndex > 0) {
			showImage(currentImageIndex - 1);
		}
	});
});

document.querySelectorAll('.next-button').forEach(button => {
    button.addEventListener('click', () => {
      // Check if there are more images to show
      if (currentImageIndex < imageContainers[0].children.length - 1) {
        showImage(currentImageIndex + 1);
      }
    });
});