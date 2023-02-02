import { debounce } from '../utils.js';

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

// TODO:FIX THIS!
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

// CREATE SUBJECT EVENT LISTENERS
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

// EDIT SECTION LISTENER
//TODO: Handle File change
const editSectionForm = document.getElementById('editSectionModal');
const editSectionName = document.getElementById('section_name');
const editSectionAdviser = document.getElementById('section_adviser');
const editSectionCollegiate = document.getElementById('section_collegiate');

let isAvailName;
let isAvailableAdviser;

let current_name = editSectionName.value;
let flag_name = editSectionName.value;
let current_adviser = editSectionAdviser.value;
let flag_adviser = editSectionAdviser.value;
let current_collegiate = editSectionCollegiate.value;

const editBodyModal = document.querySelector('#editBody');

const debounce_section = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/section/${name}`);
			return (isAvailName = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 350);

const debounce_adviser = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/user/${name}`);
			return (isAvailableAdviser = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 350);

debounce_section(current_name);
debounce_adviser(current_adviser);

editSectionForm.addEventListener('input', (e) => {
	debounce_section(current_name);
	debounce_adviser(current_adviser);
});
editSectionForm.addEventListener('submit', (e) => {
	if (isAvailName === 'False' || isAvailableAdviser === 'True') {
		e.preventDefault();
		if (isAvailName === 'False') {
			error.innerHTML = `<div class="alert alert-danger" role="alert"><b>${current_name}</b> already exists! </div>`;
		} else if (isAvailableAdviser === 'True') {
			error.innerHTML = `<div class="alert alert-danger" role="alert"><b>${current_adviser}</b> does not exists! </div>`;
		}
		editBodyModal.insertBefore(error, editBodyModal.childNodes.item(3));
	}
});

editSectionName.addEventListener('input', (e) => {
	current_name = e.target.value;
});
editSectionAdviser.addEventListener('input', (e) => {
	current_adviser = e.target.value;
});
editSectionCollegiate.addEventListener('input', (e) => {
	current_collegiate = e.target.value;
});
