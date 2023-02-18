import { debounce, emailRegex } from '../utils.js';

// CREATE SUBJECT
const createForm = document.getElementById('createForm');
const createSubjectBtn = document.getElementById('add');
const createBody = document.getElementById('createBody');
const createName = document.getElementById('createsubjectName');
const createDay = document.getElementById('createDay');
const createStart = document.getElementById('createStart');
const createEnd = document.getElementById('createEnd');
const createButton = document.getElementById('createSubmit');

export const sectionid = createSubjectBtn.dataset.sectionid;

const error = document.createElement('div');

// EDIT SUBJECT
const editSubjectForm = document.getElementById('editForm');
const editSubjectBody = document.getElementById('editSubjectBody');
const editSubjectName = document.getElementById('editSubjectName');
const editSubjectTeacher = document.getElementById('editSubjectTeacher');
const editSubjectDay = document.getElementById('editDay');
const editSubjectStart = document.getElementById('editStart');
const editSubjectEnd = document.getElementById('editEnd');
const editSubjectBtn = document.getElementById('edit');

// EDIT SECTION
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

// ============================================================================
// 									SUBJECT
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

const db_subject_edit = debounce(async (id, day, start = '', end = '', name) => {
	try {
		const response_subject = await axios.get(`/api/subjects/${sectionid}/${id}/edit`, {
			params: { day: day, start: start, end: end, name: name },
		});
		console.log(response_subject.data);
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
	if (isAvailSubject === false) {
		e.preventDefault();
		error.innerHTML = `<div class="alert alert-danger" role="alert">Subject already exists or there is time conflict!</div>`;
		createBody.insertBefore(error, createBody.childNodes.item(1));
	}
});

editSubjectForm.addEventListener('input', (e) => {
	const subID = `${editSubjectForm.action.slice(-2)}`;
	const name = editSubjectName.value;
	const day = editSubjectDay.value;
	const start = editSubjectStart.value;
	const end = editSubjectEnd.value;
	editSubjectBtn.disabled = false;
	db_subject_edit(subID, day, start, end, name);
});

editSubjectForm.addEventListener('submit', (e) => {
	if (isAvailSubject === false) {
		e.preventDefault();
		error.innerHTML = `<div class="alert alert-danger" role="alert">Subject already exists or there is time conflict!</div>`;
		editSubjectBody.insertBefore(error, editSubjectBody.childNodes.item(1));
	}
});

// ============================================================================
// 									SECTION
// ============================================================================

// EDIT SECTION LISTENER

//TODO: Handle File change
const debounce_section = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/sections/${name}`);
			if (flag_name === name) {
				return (isAvailName = true);
			} else {
				return (isAvailName = response.data.Available);
			}
		}
	} catch (e) {
		console.log(e);
	}
});

const debounce_adviser = debounce(async (name) => {
	try {
		if (name !== '') {
			const response = await axios.get(`/api/users/${name}`);
			return (isAvailableAdviser = response.data.Available);
		}
	} catch (e) {
		console.log(e);
	}
}, 350);

debounce_section(flag_name);
debounce_adviser(flag_adviser);
editSectionBtn.disabled = true;
editSectionForm.addEventListener('input', (e) => {
	const section_name = `${editSectionName.value} ${editSectionYear.value}${editSectionSection.value}`;
	const section_adviser = editSectionAdviser.value;
	const section_collegiate = editSectionCollegiate.value;

	debounce_section(section_name);

	if (emailRegex(section_adviser)) {
		debounce_adviser(section_adviser);

		setTimeout(() => {
			editSectionBtn.disabled = false;
		}, 1000);
	} else {
		editSectionBtn.disabled = true;
	}
});

editSectionForm.addEventListener('submit', (e) => {
	if (isAvailName === false || isAvailableAdviser === true) {
		e.preventDefault();
		if (isAvailName === false) {
			error.innerHTML = `<div class="alert alert-danger" role="alert"><b>${editSectionName.value} ${editSectionYear.value}${editSectionSection.value}</b> already exists! </div>`;
		} else if (isAvailableAdviser === true) {
			error.innerHTML = `<div class="alert alert-danger" role="alert"> User does not exists or! </div>`;
		}
		editBodyModal.insertBefore(error, editBodyModal.childNodes.item(3));
	}
});
