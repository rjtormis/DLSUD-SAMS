const mastheadBtn = document.getElementById('menu-btn');
const sideBar = document.querySelector('.sidebar');

let isActive = false;
mastheadBtn.addEventListener('click', (e) => {
	if (isActive === false) {
		sideBar.classList.toggle('active');
		isActive = true;
	} else {
		sideBar.classList.remove('active');
		isActive = false;
	}
});
