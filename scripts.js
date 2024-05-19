document.addEventListener("DOMContentLoaded", function () {
	const sliders = document.querySelectorAll('.image-slider');
	sliders.forEach(slider => {
		let index = 0;
		setInterval(() => {
			index = (index + 1) % slider.children.length;
			slider.style.transform = `translateX(-${index * 100}%)`;
		}, 3000);
	});
});
