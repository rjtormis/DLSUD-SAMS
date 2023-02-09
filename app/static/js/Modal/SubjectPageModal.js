// CUSTOM BACKGROUND TRIGGER
const customBG = document.getElementById('customBG');
const editBG = document.getElementById('editBG');
const file1 = document.querySelector('#create_subject');
const file2 = document.querySelector('#edit_subject');
const file3 = document.querySelector('#editSectionFile');
const submit = document.querySelector('#create');

// DELETE SUBJECT MODAL
const deleteModal = document.getElementById('deleteSubjectModal');
const deleteBody = document.querySelector('#subjectname');
const deleteform = document.querySelector('#deleteForm');

// EDIT SUBJECT MODAL
const editModal = document.getElementById('editSubjectModal');
const editName = document.getElementById('editSubjectName');
const editTeacher = document.getElementById('editSubjectTeacher');
const editForm = document.getElementById('editForm');
const editDay = document.getElementById('editDay');
const editStart = document.getElementById('editStart');
const editEnd = document.getElementById('editEnd');

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
		file3.classList.remove('disabled');

		file2.required = true;
		file3.required = true;
	} else {
		file2.classList.toggle('disabled');
		file3.classList.toggle('disabled');

		file2.required = true;
		file3.required = false;
	}
});

// Pass the subject ID to be deleted
deleteModal.addEventListener('show.bs.modal', (e) => {
	const button = e.relatedTarget;
	const subjectName = button.dataset.subjectname;
	const sectionID = button.dataset.section;
	deleteform.action = `/api/subjects/${sectionID}/${subjectName}`;
});

editModal.addEventListener('show.bs.modal', (e) => {
	const button = e.relatedTarget;
	const subjectName = button.dataset.subjectname;
	const subjectTeacher = button.dataset.subjectteacher;
	const subjectID = button.dataset.subjectid;
	const subjectDay = button.dataset.subjectday;
	const subjectStart = button.dataset.subjectstart.split(' ');
	const subjectEnd = button.dataset.subjectend.split(' ');

	editName.value = subjectName;
	editTeacher.value = subjectTeacher;
	editForm.action = `/api/subject/update/${subjectID}`;
	editDay.value = subjectDay;
	editStart.value = subjectStart[1];
	editEnd.value = subjectEnd[1];
});
