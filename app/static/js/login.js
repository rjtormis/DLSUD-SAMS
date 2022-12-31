const show = document.querySelector('#show_password');
const password = document.querySelector('#password_input');
let is_active = false;
show.addEventListener('click', (e) => {
	e.preventDefault();
	if (is_active === false) {
		password.type = 'text';
		is_active = true;
	} else {
		password.type = 'password';
		is_active = false;
	}
});
