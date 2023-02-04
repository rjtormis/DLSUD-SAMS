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
import { input_group_id, input_group_email } from './register_utils.js';
// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================

// TODO: CONVERT TO ASYNC , AWAIT
// Fetch the data and sends back to the back-end
const debounce_id = debounce((id_input) => {
	axios
		.post(
			'/api/user/check_id',
			{ query: id_input },
			{
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}
		)
		.then((res) => {
			if (res.data.avail === true) {
				idLabel.textContent = 'ID Number is available';
				idLabel.style.fontWeight = '400';
				idLabel.style.color = 'green';
				id.classList.add('is-valid');
				id.classList.remove('is-invalid');

				input_group_id.style.borderColor = 'green';
			} else if (res.data.avail === false) {
				idLabel.textContent = 'ID Number is already taken';
				idLabel.style.color = 'red';
				idLabel.style.fontWeight = '400';

				id.classList.add('is-invalid');
				id.classList.remove('is-valid');

				input_group_id.style.borderColor = 'red';
			} else if (res.data.avail === 'invalid') {
				idLabel.textContent = 'Invalid Input';
				idLabel.style.color = 'red';
				idLabel.style.fontWeight = '400';

				id.classList.add('is-invalid');
				id.classList.remove('is-valid');

				input_group_id.style.borderColor = 'red';
			} else if (res.data.avail === 'short') {
				idLabel.textContent = 'Input is too short';
				idLabel.style.color = 'red';
				idLabel.style.fontWeight = '400';

				id.classList.remove('is-valid');
				id.classList.add('is-invalid');

				input_group_id.style.borderColor = 'red';
			}
		})
		.catch((err) => {
			console.log(err);
		});
}, 350);

id.addEventListener('input', (e) => {
	const id_input = id.value;
	if (id_input === '') {
		idLabel.textContent = 'ID Number';
		idLabel.style.color = '#212529';
		idLabel.classList.add('border-start-0');
		idLabel.style.fontWeight = '400';

		id.classList.remove('is-valid');
		id.classList.remove('is-invalid');

		input_group_id.style.borderColor = '#ced4da';
	} else {
		debounce_id(id_input);
	}
});

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
					emailLabel.textContent = 'Must be DLSUD email';
					emailLabel.style.fontWeight = '400';
					emailLabel.style.color = 'red';

					email.classList.add('is-invalid');
					email.classList.remove('is-valid');

					input_group_email.style.borderColor = 'red';
				}
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
