const customBG = document.getElementById('customBG');
const file = document.querySelector('.disabled');

file.required = false;

customBG.addEventListener('click', (e) => {
	if (customBG.checked) {
		file.classList.remove('disabled');
		file.required = true;
		console.dir(file);
	} else {
		file.classList.toggle('disabled');
		file.required = false;
		console.dir(file);
	}
});
