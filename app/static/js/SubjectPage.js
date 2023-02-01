const form = document.querySelectorAll('.catButtons');
const searchParams = new URLSearchParams(window.location.search);
const res = searchParams.has('handled');

if (res) {
	form[0].classList.remove('isActive');
	form[1].classList.add('isActive');
} else {
	form[1].classList.remove('isActive');
	form[0].classList.add('isActive');
}
