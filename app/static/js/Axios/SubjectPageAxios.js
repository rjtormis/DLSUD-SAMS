import { debounce, emailRegex } from '../utils.js';

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
const editSection = document.getElementById('currentSection').textContent.split(' ');
const editSectionYearAndSection = editSection[1].split('');
const editSectionForm = document.getElementById('editSectionModalForm');
const editSectionName = document.getElementById('editCourseName');
const editSectionYear = document.getElementById('editCourseYear');
const editSectionSection = document.getElementById('editCourseSection');
const editSectionAdviser = document.getElementById('section_adviser');
const editSectionCollegiate = document.getElementById('section_collegiate');
const editSectionBtn = document.getElementById('editSection');
const editSectionFile = document.getElementById('editSectionFile');

editSectionForm.action = `/api/sections/${sectionid}/edit`;

editSectionBtn.disabled = true;

editSectionName.value = editSection[0];
editSectionYear.value = editSectionYearAndSection[0];
editSectionSection.value = editSectionYearAndSection[1];

let isAvailName;
let isAvailableAdviser;

let flag_name = `${editSection.join(' ')}`;
let flag_adviser = editSectionAdviser.value;
const editBodyModal = document.querySelector('#editBody');

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================
let isAvailSubject;

const db_subject = debounce(async (name, day, start = '', end = '') => {
	try {
		const response_subject = await axios.get(`/api/subjects/${sectionid}/${name}`, {
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
			const response = await axios.get(`/api/sections/${name}`);
			return (isAvailName = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
});

const debounce_adviser = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/users/faculty/${name}`);
			return (isAvailableAdviser = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 350);

const debounce_request = debounce(async (link, data) => {
	try {
		const request = await axios.patch(link, data);
		console.log(request.data);
	} catch (e) {
		console.log(e);
	}
});
debounce_section(flag_name);
debounce_adviser(flag_adviser);

editSectionForm.addEventListener('input', (e) => {
	const section_name = `${editSectionName.value} ${editSectionYear.value}${editSectionSection.value}`;
	const section_adviser = editSectionAdviser.value;
	const section_collegiate = editSectionCollegiate.value;

	debounce_section(section_name);
	if (emailRegex(section_adviser) && section_name !== flag_name) {
		debounce_adviser(section_adviser);
		editSectionBtn.disabled = false;
	}
});

editSectionForm.addEventListener('submit', (e) => {
	if (isAvailName === 'False' || isAvailableAdviser === 'True') {
		e.preventDefault();
		if (isAvailName === 'False') {
			error.innerHTML = `<div class="alert alert-danger" role="alert"><b>${editSectionName.value} ${editSectionYear.value}${editSectionSection.value}</b> already exists! </div>`;
		} else if (isAvailableAdviser === 'True') {
			error.innerHTML = `<div class="alert alert-danger" role="alert"> User does not exists! </div>`;
		}
		editBodyModal.insertBefore(error, editBodyModal.childNodes.item(3));
	} else {
		e.preventDefault();
		const data = new FormData(editSectionForm);
		for (const [key, val] of data.entries()) {
			console.log(`${key}:${val}`);
		}
		debounce_request(editSectionForm.action, data);
	}
});
