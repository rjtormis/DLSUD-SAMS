const side_bar = document.querySelector('.side-bar');
const arrow = document.querySelector('.arrow');
const nav_item = document.querySelectorAll('.nav-item a');
let checker = false;

function show(check) {
	const item_name = document.querySelectorAll('.item-name');
	const item_icon = document.querySelectorAll('.item-icon');

	if (check === false) {
		item_name.forEach(function (item) {
			item.style.display = 'inline';
		});
		item_icon.forEach(function (item) {
			item.style.marginRight = '10px';
		});
		nav_item.forEach(function (item) {
			item.style.justifyContent = 'start';
			item.classList.add('active');
			item.classList.remove('anim');
		});

		checker = true;
	} else {
		item_name.forEach(function (item) {
			item.style.display = 'none';
		});
		item_icon.forEach(function (item) {
			item.style.marginRight = '0';
		});
		nav_item.forEach(function (item) {
			item.style.justifyContent = 'center';
			item.classList.add('anim');
			item.classList.remove('active');
		});
		checker = false;
	}
}

nav_item.forEach(function (item) {
	item.classList.add('anim');
	item.classList.remove('active');
});

arrow.addEventListener('click', (e) => {
	if (checker === true) {
		show(true);
	} else {
		show(false);
	}
});
