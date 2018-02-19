window.onscroll = function() {
	const main_menu = document.getElementById("main-menu");
	monitor_nav(main_menu);	
};

const monitor_nav = function (nav) {   
	if (window.pageYOffset >= 10) {
		nav.classList.add('bg-dark');
	} else {
		nav.classList.remove('bg-dark');
	}
}
