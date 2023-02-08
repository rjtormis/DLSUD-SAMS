import { debounce } from '../utils.js';
const createForm = document.getElementById('createClassroom');
const customBG = document.getElementById('customBG');
const file = document.querySelector('.disabled');
const submit = document.querySelector('#create');

const courseName = document.querySelector('#courseName');
const year = document.querySelector('#year');
const section = document.querySelector('#section');

let current_courseName = courseName.value;
let current_year = year.value;
let current_section = section.value;

const error = document.createElement('div');

const modal_body = document.querySelector('.modal-body');
// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================

let isAvail;
// STRUCTURED
const debounce_section = debounce(async (course, year, section) => {
	try {
		const response = await axios.get(`/api/sections/${course} ${year}${section}`);
		return (isAvail = response.data.Available);
	} catch (e) {
		console.log(e);
	}
}, 350);
// Query the default value.
debounce_section(current_courseName, current_year, current_section);

file.required = false;

customBG.addEventListener('click', (e) => {
	if (customBG.checked) {
		file.classList.remove('disabled');
		file.required = true;
	} else {
		file.classList.toggle('disabled');
		file.required = false;
	}
});

createForm.addEventListener('change', (e) => {
	submit.disabled = true;
	setTimeout(() => {
		submit.disabled = false;
	}, 750);
});

createForm.addEventListener('input', async (e) => {
	const course = courseName.value;
	const cyear = year.value;
	const csection = section.value;
	debounce_section(course, cyear, csection);
});

createForm.addEventListener('submit', (e) => {
	if (isAvail === false) {
		e.preventDefault();
		error.innerHTML = `<div class="alert alert-danger" role="alert"><b>${current_courseName} ${current_year}${current_section}</b> already exists! </div>`;
		modal_body.insertBefore(error, modal_body.childNodes.item(3));
	}
});
