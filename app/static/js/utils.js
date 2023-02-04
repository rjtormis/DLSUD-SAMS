export const emailRegex = (email) => {
	const pattern = /@dlsud.edu.ph$/;
	if (pattern.test(email)) {
		return true;
	}
};

// DEBOUNCING
export function debounce(cb, delay = 1000) {
	let timeout;
	return (...args) => {
		clearTimeout(timeout);
		timeout = setTimeout(() => {
			cb(...args);
		}, delay);
	};
}
