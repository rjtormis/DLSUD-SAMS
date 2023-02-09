import { debounce } from '../utils.js';
import { firstName, firstNameLabel, middleName, middleNameLabel, lastName, lastNameLabel } from './register_utils.js';
import {
	id,
	idLabel,
	email,
	emailLabel,
	password1,
	password1Label,
	password2,
	password2Label,
} from './register_utils.js';
import { all_input_group, input_group_email } from './register_utils.js';
// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================

// Collegiate
const collegiate = document.querySelector('#collegiate_input');
const collegiateLabel = document.querySelector('label[for="collegiate_input"]');
// Birthdate
const birthDate = document.querySelector('#date_input');
const birthDateLabel = document.querySelector('label[for="date_input"]');

const input_group_collegiate = all_input_group[0];
const input_group_birthdate = all_input_group[1];

if (collegiate.value) {
	collegiate.style.borderColor = 'green';
	collegiateLabel.style.color = 'green';
	collegiateLabel.style.fontWeight = '400';
	input_group_collegiate.style.borderColor = 'green';
}

birthDate.addEventListener('input', (e) => {
	const date = birthDate.value;
	if (date === '') {
		birthDate.style.borderColor = '#ced4da';

		birthDateLabel.style.color = '#212529';
		birthDateLabel.style.fontWeight = '400';

		input_group_birthdate.style.borderColor = '#ced4da';
	} else {
		birthDate.style.borderColor = 'green';

		birthDateLabel.style.color = 'green';
		birthDateLabel.style.fontWeight = '400';

		input_group_birthdate.style.borderColor = 'green';
	}
});

// TODO: CONVERT TO ASYNC AWAIT
const debounce_email = debounce((email_input) => {
	axios
		.post(
			'/api/user/check_email',
			{ query: email_input },
			{
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}
		)
		.then((res) => {
			if (res.data.avail === true) {
				emailLabel.textContent = 'Email Address is available';
				emailLabel.style.fontWeight = '400';
				emailLabel.style.color = 'green';

				email.classList.add('is-valid');
				email.classList.remove('is-invalid');

				input_group_email.style.borderColor = 'green';
			} else if (res.data.avail === false) {
				emailLabel.textContent = 'Email Address is already taken';
				emailLabel.style.fontWeight = '400';
				emailLabel.style.color = 'red';

				email.classList.add('is-invalid');
				email.classList.remove('is-valid');

				input_group_email.style.borderColor = 'red';
			} else if (res.data.avail === 'invalid') {
				emailLabel.textContent = 'Must be DLSUD email';
				emailLabel.style.fontWeight = '400';
				emailLabel.style.color = 'red';

				email.classList.add('is-invalid');
				email.classList.remove('is-valid');

				input_group_email.style.borderColor = 'red';
			}
		})
		.catch((err) => {
			console.log(err);
		});
}, 350);

email.addEventListener('input', (e) => {
	const email_input = email.value;
	if (email_input == '') {
		emailLabel.textContent = 'Email Address';
		emailLabel.classList.add('border-start-0');
		emailLabel.style.color = '#212529';
		emailLabel.style.fontWeight = '400';

		email.classList.remove('is-invalid');
		email.classList.remove('is-valid');

		input_group_email.style.borderColor = '#ced4da';
	} else {
		debounce_email(email_input);
	}
});
