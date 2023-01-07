const customBG = document.getElementById('customBG');
const editBG = document.getElementById('editBG');
const file1 = document.querySelector('#create_subject');
const file2 = document.querySelector('#edit_section');
const submit = document.querySelector('#create');

const deleteModal = document.getElementById('deleteSubjectModal');
const deleteform = document.querySelector('#deleteForm');

customBG.addEventListener('click', (e) => {
	if (customBG.checked) {
		file1.classList.remove('disabled');
		file1.required = true;
	} else {
		file1.classList.toggle('disabled');
		file1.required = false;
	}
});

editBG.addEventListener('click', (e) => {
	if (editBG.checked) {
		file2.classList.remove('disabled');
		file2.required = true;
	} else {
		file2.classList.toggle('disabled');
		file2.required = false;
	}
});

// Pass the subject ID to be deleted
deleteModal.addEventListener('show.bs.modal', (e) => {
	const button = e.relatedTarget;
	const subjectID = button.dataset.subjectid;
	deleteform.action = `/api/subject/delete/${subjectID}`;
});
