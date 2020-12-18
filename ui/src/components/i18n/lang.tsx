import ar from './ar.json';
import en from './en.json';
import fr from './fr.json';
import de from './de.json';

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const language = urlParams.get('lang');

let setlang: any;

if (language === 'ar') {
	setlang = ar;
} else if (language === 'de') {
	setlang = de;
} else if (language === 'en') {
	setlang = en;
} else if (language === 'fr') {
	setlang = fr;
} else {
	setlang = en;
}

export default setlang;
