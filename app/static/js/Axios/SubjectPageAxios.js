import { debounce } from '../utils.js';

// CREATE
const createForm = document.getElementById('createForm');
const createSubjectBtn = document.getElementById('add');
const createBody = document.getElementById('createBody');
const createName = document.getElementById('createsubjectName');
const createDay = document.getElementById('createDay');
const createStart = document.getElementById('createStart');
const createEnd = document.getElementById('createEnd');
const createButton = document.getElementById('createSubmit');

const sectionid = createSubjectBtn.dataset.sectionid;

const error = document.createElement('div');

// EDIT
const editSectionForm = document.getElementById('editSectionModal');
const editSectionName = document.getElementById('section_name');
const editSectionAdviser = document.getElementById('section_adviser');
const editSectionCollegiate = document.getElementById('section_collegiate');

let isAvailName;
let isAvailableAdviser;

let flag_name = editSectionName.value;
let flag_adviser = editSectionAdviser.value;

const editBodyModal = document.querySelector('#editBody');

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================
let isAvailSubject;

const db_subject = debounce(async (name, day, start = '', end = '') => {
	try {
		const response_subject = await axios.get(`/api/subject/${sectionid}/${name}`, {
			params: { day: day, start: start, end: end },
		});
		return (isAvailSubject = response_subject.data.Available);
	} catch (e) {
		console.log(e);
	}
}, 350);

// CREATE SUBJECT EVENT LISTENERS
createSubjectBtn.addEventListener('click', (e) => {
	if (createBody.contains(error)) {
		createBody.removeChild(error);
	}
	createName.value = '';
	createStart.value = '';
	createEnd.value = '';
});

createForm.addEventListener('input', (e) => {
	const name = createName.value;
	const day = createDay.value;
	const start = createStart.value;
	const end = createEnd.value;
	if (end !== '') {
		createButton.disabled = false;
		db_subject(name, day, start, end);
	}
});

createForm.addEventListener('submit', (e) => {
	if (isAvailSubject === 'False') {
		e.preventDefault();
		error.innerHTML = `<div class="alert alert-danger" role="alert">Subject already exists or there is time conflict!</div>`;
		createBody.insertBefore(error, createBody.childNodes.item(1));
	}
});

// EDIT SECTION LISTENER

//TODO: Handle File change
const debounce_section = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/section/${name}`);
			console.log(response.data);
			return (isAvailName = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 750);

const debounce_adviser = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/user/${name}`);
			return (isAvailableAdviser = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 750);

debounce_section(flag_adviser);
debounce_adviser(flag_adviser);

editSectionForm.addEventListener('input', (e) => {
	const section_name = editSectionName.value;
	const section_adviser = editSectionAdviser.value;
	const section_collegiate = editSectionCollegiate.value;

	debounce_section(section_name);
	debounce_adviser(section_adviser);
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
