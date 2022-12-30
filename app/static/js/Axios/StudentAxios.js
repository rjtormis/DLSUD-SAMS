import { debounce } from './utils.js';

const id = document.querySelector('#id_input');

// Add's delay
const debounce_id = debounce((id_input) => {
	axios
		.post(
			'/check_id',
			{ query: id_input },
			{
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}
		)
		.then((res) => {
			console.log(res.data.avail);
		})
		.catch((err) => {
			console.log(err);
		});
}, 500);

id.addEventListener('input', (e) => {
	const id_input = id.value;
	debounce_id(id_input);
});
