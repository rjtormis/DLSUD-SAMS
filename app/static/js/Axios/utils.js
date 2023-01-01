// DEBOUNCING
export function debounce(cb, delay = 1000) {
	let timeout;
	return (...args) => {
		clearTimeout(timeout);
		timeout = setTimeout(() => {
			cb(...args);
		}, delay);
	};
}

// REGEX
const nameRegex = '^[A-Za-z ]+$';
const passwordRegex = /^(?=.*[!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>\/?])[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>\/?]+$/;

export const all_input_group = document.querySelectorAll('.input-group-text');

export let input_group_id = '';
export let input_group_email = '';

export let input_group_password1 = '';
export let input_group_password2 = '';

all_input_group.forEach((uri) => {
	if (uri.baseURI.includes('/create/student')) {
		input_group_id = all_input_group[0];
		input_group_email = all_input_group[1];
		input_group_password1 = all_input_group[2];
		input_group_password2 = all_input_group[3];
	} else if (uri.baseURI.includes('/create/faculty')) {
		input_group_email = all_input_group[2];
		input_group_password1 = all_input_group[3];
		input_group_password2 = all_input_group[4];
	}
});

// ID
export const id = document.querySelector('#id_input');
export const idLabel = document.querySelector('label[for = "id_input"]');

// First name
export const firstName = document.querySelector('#first_name');
export const firstNameLabel = document.querySelector('label[for="first_name"]');
const current_label_firstname = firstNameLabel.textContent;

// Middle Initial
export const middleName = document.querySelector('#initial');
export const middleNameLabel = document.querySelector('label[for="initial"]');
const current_label_middlename = middleNameLabel.textContent;

// Last name
export const lastName = document.querySelector('#last_name');
export const lastNameLabel = document.querySelector('label[for="last_name"]');
const current_label_lastname = lastNameLabel.textContent;

// Email Address
export const email = document.querySelector('#email_input');
export const emailLabel = document.querySelector('label[for="email_input"]');
// Password 1
export const password1 = document.querySelector('#password_input');
export const password1Label = document.querySelector('label[for="password_input"]');
// Password 2 (Confirm)
export const password2 = document.querySelector('#password_confirm');
export const password2Label = document.querySelector('label[for="password_confirm"]');

// Submit
export const submit = document.querySelector('.registerBtn');

// REGEX CHECKER FOR INPUT IN LAST NAME , MIDDLE I, FIRST NAME
export function validateInput(input, element_var, label_var, characters, default_content) {
	const regex = new RegExp(nameRegex);
	if (input.search(/[0-9]/) !== -1) {
		element_var.classList.add('is-invalid');
		element_var.classList.remove('is-valid');
		label_var.textContent = 'Invalid';
		label_var.style.color = 'red';
		label_var.style.fontWeight = '400';
	} else {
		if (regex.test(input) && input !== '' && input.length >= characters) {
			element_var.classList.add('is-valid');
			element_var.classList.remove('is-invalid');
			label_var.textContent = `${default_content}`;
			label_var.style.color = 'green';
			label_var.style.fontWeight = '400';
		} else if (regex.test(input) && input !== '' && input.length < characters) {
			element_var.classList.add('is-invalid');
			element_var.classList.remove('is-valid');
			label_var.textContent = `Too short`;
			label_var.style.color = 'red';
			label_var.style.fontWeight = '400';
		}
	}
}

// Validate password
export function validatePassword() {
	const password = password1.value;
	const regex = new RegExp(passwordRegex);

	const hasSpecialCharacter = regex.test(password);

	if (password === '') {
		password1Label.textContent = 'Password';
		password1Label.style.color = '#212529';
		password1Label.classList.add('border-start-0');
		password1Label.style.fontWeight = '400';

		password1.classList.remove('is-invalid');
		password1.classList.remove('is-valid');

		input_group_password1.style.borderColor = '#ced4da';
	} else {
		if (hasSpecialCharacter && password.length >= 8) {
			password1Label.textContent = 'Password';
			password1Label.style.color = 'green';
			password1Label.style.fontWeight = '400';

			password1.classList.add('is-valid');
			password1.classList.remove('is-invalid');

			input_group_password1.style.borderColor = 'green';
		} else if (hasSpecialCharacter && password.length < 8) {
			password1Label.textContent = 'Password length is too short.';
			password1Label.style.color = 'red';
			password1Label.style.fontWeight = '400';

			password1.classList.add('is-invalid');
			password1.classList.remove('is-valid');

			input_group_password1.style.borderColor = 'red';
		} else {
			password1Label.textContent = 'Must contain atleast 1 special character';
			password1Label.style.color = 'red';
			password1Label.style.fontWeight = '400';

			password1.classList.add('is-invalid');
			password1.classList.remove('is-valid');

			input_group_password1.style.borderColor = 'red';
		}
	}

	const confirmed_password = password2.value;
	if (confirmed_password == '') {
		password2Label.textContent = 'Confirm Password';
		password2Label.style.color = '#212529';
		password2Label.classList.add('border-start-0');
		password2Label.style.fontWeight = '400';

		password2.classList.remove('is-invalid');
		password2.classList.remove('is-valid');

		input_group_password2.style.borderColor = '#ced4da';
	} else if (confirmed_password !== '' && password !== confirmed_password) {
		password2Label.textContent = 'Password do not match';
		password2Label.style.color = 'red';
		password2Label.style.fontWeight = '400';

		password2.classList.add('is-invalid');
		password2.classList.remove('is-valid');

		input_group_password2.style.borderColor = 'red';
	} else if (confirmed_password !== '' && password == confirmed_password) {
		password2Label.textContent = 'Password Matched';
		password2Label.style.color = 'green';
		password2Label.style.fontWeight = '400';

		password2.classList.add('is-valid');
		password2.classList.remove('is-invalid');

		input_group_password2.style.borderColor = 'green';
	}
}

// Remove all elements
export function removeAll() {
	firstName.classList.remove('is-invalid');
	middleName.classList.remove('is-invalid');
	lastName.classList.remove('is-invalid');
	email.classList.remove('is-invalid');
	password1.classList.remove('is-invalid');
	password2.classList.remove('is-invalid');

	firstName.classList.remove('is-valid');
	middleName.classList.remove('is-valid');
	lastName.classList.remove('is-valid');
	email.classList.remove('is-valid');
	password1.classList.remove('is-valid');
	password2.classList.remove('is-valid');

	firstNameLabel.textContent = 'First name';
	middleNameLabel.textContent = 'Middle I.';
	lastNameLabel.textContent = 'Last name';
	emailLabel.textContent = 'Email Address';
	password1Label.textContent = 'Password';
	password2Label.textContent = 'Confirm Password';

	firstName.textContent = '';
	middleName.textContent = '';
	lastName.textContent = '';
	email.textContent = '';
	password1.textContent = '';
	password2.textContent = '';

	input_group_email.style.borderColor = '#ced4da';
	input_group_password1.style.borderColor = '#ced4da';
	input_group_password2.style.borderColor = '#ced4da';

	if (submit.baseURI.includes('/create/student')) {
		id.classList.remove('is-invalid');
		id.classList.remove('is-valid');
		id.textContent = '';
		input_group_id.style.borderColor = '#ced4da';
	}
}

// firstName Event Listener
firstName.addEventListener('input', (e) => {
	const first = firstName.value;
	if (first === '') {
		firstName.classList.remove('is-invalid');
		firstName.classList.remove('is-valid');
		firstNameLabel.textContent = 'First name';
		firstNameLabel.style.color = '#212529';
		firstNameLabel.style.fontWeight = '400';
	} else {
		validateInput(first, firstName, firstNameLabel, 2, current_label_firstname);
	}
});

// middleName Event Listener
middleName.addEventListener('input', (e) => {
	const middle = middleName.value;
	if (middle === '') {
		middleName.classList.remove('is-invalid');
		middleName.classList.remove('is-valid');
		middleNameLabel.textContent = 'Middle I.';
		middleNameLabel.style.color = '#212529';
		middleNameLabel.style.fontWeight = '400';
	} else {
		validateInput(middle, middleName, middleNameLabel, 1, current_label_middlename);
	}
});

// lastName Event Listener
lastName.addEventListener('input', (e) => {
	const last = lastName.value;
	if (last === '') {
		lastName.classList.remove('is-invalid');
		lastName.classList.remove('is-valid');
		lastNameLabel.textContent = 'Last name';
		lastNameLabel.style.color = '#212529';
		lastNameLabel.style.fontWeight = '400';
	} else {
		validateInput(last, lastName, lastNameLabel, 4, current_label_lastname);
	}
});

// password1 Event Listener
password1.addEventListener('input', validatePassword);
// password2 Event Listener
password2.addEventListener('input', validatePassword);
// Submit Event Listener
submit.addEventListener('click', (e) => {
	removeAll();
});
