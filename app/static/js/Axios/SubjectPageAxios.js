import { debounce } from './utils.js';

// CREATE
const createForm = document.getElementById('createForm');
const createSubjectBtn = document.getElementById('add');
const createBody = document.getElementById('createBody');
const createName = document.getElementById('createsubjectName');
const createDay = document.getElementById('createDay');
const createStart = document.getElementById('createStart');
const createEnd = document.getElementById('createEnd');

const sectionid = createSubjectBtn.dataset.sectionid;

const error = document.createElement('div');

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================
let avail;

const debounce_subject = debounce(async (id, subject_input, day, start, end) => {
	try {
		const response = await axios.get(`/api/subject/${id}`, {
			params: { subject: subject_input, day: day, start: start, end: end },
		});
		return (avail = response.data.avail);
	} catch (e) {
		console.log(e);
	}
});

let section_avail;
const debounce_section = debounce(async (name) => {
	try {
		const response = await axios.get(`/api/section/check_section`, {
			params: { query: name },
		});
		return (section_avail = response.data.avail);
	} catch (e) {
		console.log(e);
	}
});

// CREATE EVENT LISTENERS
createSubjectBtn.addEventListener('click', (e) => {
	if (createBody.contains(error)) {
		createBody.removeChild(error);
	}
	createName.value = '';
	createStart.value = '';
	createEnd.value = '';
});

createForm.addEventListener('input', async (e) => {
	const name = createName.value;
	const day = createDay.value;
	const start = createStart.value;
	const end = createEnd.value;
	if (name !== '' && start !== '' && end !== '') {
		debounce_subject(sectionid, name, day, start, end);
	}
});

createForm.addEventListener('submit', (e) => {
	if (!avail) {
		e.preventDefault();
		error.innerHTML = `<div class="alert alert-danger" role="alert">Subject already exists or there is time conflict!</div>`;
		createBody.insertBefore(error, createBody.childNodes.item(1));
	}
});

// EDIT
const editSectionForm = document.querySelector('#editSectionModal');
const editSectionName = document.querySelector('#section_name');

editSectionForm.addEventListener('input', async (e) => {
	const value = editSectionName.value;
	if (value !== '') {
	}
});
