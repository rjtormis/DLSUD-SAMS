import { debounce } from './utils.js';

const createSubject = document.getElementById('add');
const createName = document.getElementById('createsubjectName');
const createNameLabel = document.querySelector('label[for="createsubjectName"]');
const createSubmit = document.getElementById('createSubmit');

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================
//TODO: FIX THIS FOR TOMORROW.
let result;
const debounce_subjectName = debounce(async (id, subject_input) => {
	try {
		const response = await axios.get(`/api/subject/${id}/${subject_input}`);
		result = response.data.avail;
	} catch (e) {
		console.log(e);
	}
}, 350);

createName.addEventListener('input', (e) => {
	const val = createName.value;
	if (val.trim().length > 0) {
		createName.classList.remove('is-invalid');
		createNameLabel.style.color = 'black';
		createNameLabel.textContent = 'Subject Name';
		debounce_subjectName(createSubject.dataset.sectionid, createName.value);
	} else {
		createName.classList.add('is-invalid');
		createNameLabel.style.color = 'red';
		createNameLabel.textContent = 'Invalid input';
	}
});

createSubmit.addEventListener('click', (e) => {
	e.preventDefault();
	console.log(result);
});
