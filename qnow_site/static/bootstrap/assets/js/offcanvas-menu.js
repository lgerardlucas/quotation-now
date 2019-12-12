(function($) {
	$(document).ready(function() {
		var childMenu = $("div.offcanvas-menu .menu .nav-child"),
			toggleIcon = $("<span class='toggle-icon uk-icon-angle-down'></span>"),
			hasChild = $("div.offcanvas-menu .menu .parent");

		
		$(childMenu).hide();
		$(hasChild).append(toggleIcon);
		$(".toggle-icon").on("click", function() {
			$(this).closest("li").find('> .nav-child').slideToggle();
		});
	});
})(jQuery);