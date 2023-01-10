import { debounce } from './utils.js';

const createSubject = document.getElementById('add');
const createBody = document.getElementById('createBody');
const createName = document.getElementById('createsubjectName');
const createNameLabel = document.querySelector('label[for="createsubjectName"]');
const createSubmit = document.getElementById('createSubmit');
const createDay = document.getElementById('createDay');
const createStart = document.getElementById('createStart');
const createEnd = document.getElementById('createEnd');

const sectionid = createSubject.dataset.sectionid;

const error = document.createElement('div');

// ============================================================================
// 							FETCH API FOR BACKEND QUERY
// ============================================================================

let avail;

const debounce_subjectName = debounce(async (id, subject_input, day, start, end) => {
	try {
		const response = await axios.get(`/api/subject/${id}`, {
			params: { subject: subject_input, day: day, start: start, end: end },
		});

		avail = response.data.avail;
	} catch (e) {
		console.log(e);
	}
}, 350);

createEnd.addEventListener('input', (e) => {
	const name = createName.value;
	const day = createDay.value;
	const start = createStart.value;
	const end = createEnd.value;
	debounce_subjectName(sectionid, name, day, start, end);
});
// FIXME: TO FIX
createSubmit.addEventListener('click', (e) => {
	const val = createName.value;

	console.log(val);
});
