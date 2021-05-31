import ar from './ar.json';
import de from './de.json';
import en from './en.json';
import es from './es.json';
import fr from './fr.json';
import it from './it.json';
import ptBR from './pt-BR.json';
import tr from './tr.json';

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
} else if (language === 'es') {
	setlang = es;
} else if (language === 'it') {
	setlang = it;
} else if (language === 'pt-BR') {
	setlang = ptBR;
} else if (language === 'tr') {
	setlang = tr;
} else {
	setlang = en;
}

if (!setlang.network_fetch_fail) {
	setlang.network_fetch_fail = en.network_fetch_fail;
}
if (!setlang.network_absent) {
	setlang.network_absent = en.network_absent;
}
if (!setlang.network_connect_fail) {
	setlang.network_connect_fail = en.network_connect_fail;
}
if (!setlang.network_connect_fail) {
	setlang.network_connect_fail = en.network_connect_fail;
}
if (!setlang.wifi) {
	setlang.wifi = en.wifi;
}
if (!setlang.user) {
	setlang.user = en.user;
}
if (!setlang.password) {
	setlang.password = en.password;
}
if (!setlang.select_ssid) {
	setlang.select_ssid = en.select_ssid;
}
if (!setlang.connect) {
	setlang.connect = en.connect;
}
if (!setlang.applying_changes) {
	setlang.applying_changes = en.applying_changes;
}
if (!setlang.connection_reset_request) {
	setlang.connection_reset_request = en.connection_reset_request;
}
if (!setlang.no_networks) {
	setlang.no_networks = en.no_networks;
}

export default setlang;
