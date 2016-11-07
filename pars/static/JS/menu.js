$(document).ready(function(){
	var link = window.location.pathname;
	$('.pure-menu-item a[href="'+link+'"]').parent().addClass('pure-menu-item pure-menu-selected');
});
