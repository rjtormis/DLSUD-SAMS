const all_input_group = document.querySelectorAll('.input-group-text');
const input_group_email = all_input_group[0];
const input_group_password = all_input_group[1];
const input_group_show = all_input_group[2];

const email = document.querySelector('#email_input');
const emailLabel = document.querySelector('label[for="email_input"]');

const password = document.querySelector('#password_input');
const passwordLabel = document.querySelector('label[for="password_input"]');
const show = document.querySelector('#show_password');
const icon = document.querySelector('.material-icons-outlined');

const submit = document.querySelector('.loginBtn');

// Email
email.addEventListener('input', (e) => {
	const email_input = email.value;
	if (email_input === '') {
		emailLabel.textContent = 'Email Address';
		emailLabel.classList.add('border-start-0');
		emailLabel.style.color = '#212529';
		emailLabel.style.fontWeight = '400';

		email.classList.remove('is-invalid');
		email.classList.remove('is-valid');

		input_group_email.style.borderColor = '#ced4da';
	}
});
email.addEventListener('click', (e) => {
	emailLabel.textContent = 'Email Address';
	emailLabel.classList.add('border-start-0');
	emailLabel.style.color = '#212529';
	emailLabel.style.fontWeight = '400';

	email.classList.remove('is-invalid');
	email.classList.remove('is-valid');

	input_group_email.style.borderColor = '#ced4da';
});

password.addEventListener('click', (e) => {
	passwordLabel.textContent = 'Password';
	passwordLabel.classList.add('border-start-0');
	passwordLabel.style.color = '#212529';
	passwordLabel.style.fontWeight = '400';

	password.style.borderColor = '#ced4da';
	show.style.color = '#212529';
	icon.style.color = '#212529';
	icon.classList.add('material-icons-outlined');

	input_group_password.style.borderColor = '#ced4da';
	input_group_show.style.borderColor = '#ced4da';
});
password.addEventListener('input', (e) => {
	passwordLabel.textContent = 'Password';
	passwordLabel.classList.add('border-start-0');
	passwordLabel.style.color = '#212529';
	passwordLabel.style.fontWeight = '400';

	password.style.borderColor = '#ced4da';
	show.style.color = '#212529';
	icon.style.color = '#212529';
	icon.classList.add('material-icons-outlined');

	input_group_password.style.borderColor = '#ced4da';
	input_group_show.style.borderColor = '#ced4da';
});

let is_active = false;

// Showing Password
show.addEventListener('click', (e) => {
	e.preventDefault();
	console.log(show.innerHTML);

	if (is_active === false) {
		password.type = 'text';
		show.innerHTML = '<span class="material-icons-outlined"> visibility_off </span>';
		is_active = true;
	} else {
		password.type = 'password';
		show.innerHTML = '<span class="material-icons-outlined"> visibility </span>';
		is_active = false;
	}
});
