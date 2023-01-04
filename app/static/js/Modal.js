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
let is_avail = false;

const querySectionAvailability = async () => {
	try {
		const response = await axios.post(
			'/api/section/check_section',
			{ query: `${current_courseName} ${current_year}${current_section}` },
			{
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded',
				},
			}
		);
		return response.data.avail;
	} catch (err) {
		console.log(err);
	}
};
let result;
function getResult() {
	querySectionAvailability().then((res) => {
		result = res;
	});
}

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

courseName.addEventListener('change', (e) => {
	current_courseName = e.target.value;
});
year.addEventListener('change', (e) => {
	current_year = e.target.value;
});
section.addEventListener('change', (e) => {
	current_section = e.target.value;
});

// FIXME: NEEDS TO BE FIX FOR ERROR HANDLING!!
submit.addEventListener('click', (e) => {
	e.preventDefault();
	getResult();
	console.log(result);
});
