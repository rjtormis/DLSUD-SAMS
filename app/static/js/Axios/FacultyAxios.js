import { debounce } from './utils.js';
import { firstName, firstNameLabel, middleName, middleNameLabel, lastName, lastNameLabel } from './utils.js';
import { id, idLabel, email, emailLabel, password1, password1Label, password2, password2Label } from './utils.js';

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================

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
				email.classList.add('is-valid');
				email.classList.remove('is-invalid');
			} else if (res.data.avail === false) {
				emailLabel.textContent = 'Email Address is already taken';
				email.classList.add('is-invalid');
				email.classList.remove('is-valid');
			} else if (res.data.avail === 'invalid') {
				emailLabel.textContent = 'Must be a DLSUD email';
				email.classList.add('is-invalid');
				email.classList.remove('is-valid');
			}
		})
		.catch((err) => {
			console.log(err);
		});
}, 350);

email.addEventListener('input', (e) => {
	const email_input = email.value;
	if (email_input == '') {
		email.classList.remove('is-invalid');
		email.classList.remove('is-valid');
		emailLabel.textContent = 'Email Address';
	} else {
		debounce_email(email_input);
	}
});
