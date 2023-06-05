$(function () {
	var $tabButtonItem = $('#tab-button li'),
		$tabSelect = $('#tab-select'),
		$tabContents = $('.tab-contents'),
		activeClass = 'is-active';

	$tabButtonItem.first().addClass(activeClass);
	$tabContents.not(':first').hide();

	$tabButtonItem.find('a').on('click', function (e) {
		var target = $(this).attr('href');

		$tabButtonItem.removeClass(activeClass);
		$(this).parent().addClass(activeClass);
		$tabSelect.val(target);
		$tabContents.hide();
		$(target).show();
		e.preventDefault();
	});

	$tabSelect.on('change', function () {
		var target = $(this).val(),
			targetSelectNum = $(this).prop('selectedIndex');

		$tabButtonItem.removeClass(activeClass);
		$tabButtonItem.eq(targetSelectNum).addClass(activeClass);
		$tabContents.hide();
		$(target).show();
	});
});

/* left nav bar js */
function htmlbodyHeightUpdate() {
	var height3 = $(window).height()
	var height1 = $('.nav').height() + 50
	height2 = $('.main').height()
	if (height2 > height3) {
		$('html').height(Math.max(height1, height3, height2) + 10);
		$('body').height(Math.max(height1, height3, height2) + 10);
	}
	else {
		$('html').height(Math.max(height1, height3, height2));
		$('body').height(Math.max(height1, height3, height2));
	}

}
$(document).ready(function () {
	htmlbodyHeightUpdate()
	$(window).resize(function () {
		htmlbodyHeightUpdate()
	});
	$(window).scroll(function () {
		height2 = $('.main').height()
		htmlbodyHeightUpdate()
	});
});

/* ************************end *****************/

function update_votes(upvote_ele, downvote_ele, data ){
	upvote_ele.find('span').html(data['vote_difference'])
	// downvote_ele.find('span').html(data['downvotes'])

	if (data['user_has_upvoted']){
		if (upvote_ele.hasClass("btn-outline-info")){
			upvote_ele.removeClass("btn-outline-info");
			upvote_ele.addClass("btn-info");
		}
	} else {
		if (upvote_ele.hasClass("btn-info")){
			upvote_ele.removeClass("btn-info");
			upvote_ele.addClass("btn-outline-info");
		}
	}

	if (data['user_has_downvoted']){
		if (downvote_ele.hasClass("btn-outline-info")){
			downvote_ele.removeClass("btn-outline-info");
			downvote_ele.addClass("btn-info");
		}
	} else {
		if (downvote_ele.hasClass("btn-info")){
			downvote_ele.removeClass("btn-info");
			downvote_ele.addClass("btn-outline-info");
		}
	}
}


$(document).on('click', '.upvote', function () {
	// var vote_defferece_ele = $(this).siblings('span')
	console.log($(this).data('object_type'))
	var upvote_ele = $(this);
	var downvote_ele = $(this).parent().find(".downvote")
	if(upvote_ele.hasClass("btn-outline-info")){
		var vote_choice = 'UP'
	}else{
		var vote_choice = 'NONE'
	}
	$.ajax({
		type: "POST",
		url: "/forum/vote-object",
		data: {
			'object_type': upvote_ele.data('object_type'),
			'object_id': upvote_ele.data('object_id'),
			'vote_choice': vote_choice
		},
		success: function (data) {
			console.log(data)
			update_votes(upvote_ele, downvote_ele, data)
		},
		error: function (data) {
			alert(data['responseJSON']["message"]);
		}
	});
	return false;
});

$(document).on('click', '.downvote', function () {
	var downvote_ele = $(this);
	var upvote_ele = $(this).parent().find(".upvote")
	if(downvote_ele.hasClass("btn-outline-info")){
		var vote_choice = 'DOWN'
	}else{
		var vote_choice = 'NONE'
	}
	$.ajax({
		type: "POST",
		url: "/forum/vote-object",
		data: {
			'object_type': upvote_ele.data('object_type'),
			'object_id': upvote_ele.data('object_id'),
			'vote_choice': vote_choice
		},
		success: function (data) { 
			// console.log(data)
			update_votes(upvote_ele, downvote_ele, data)
		},
		error: function (data) {
			alert(data['responseJSON']["message"]);
		}
	});
	return false;
});

$(document).on('click', '.delete-post', function () {
	var post = $(this).parent().parent().parent().parent();
	var delete_form = post.find('.confirm-delete-form');
	delete_form.toggle();
});

$(document).on('click', '.edit-comment', function () {
	var comment = $(this).parent().parent().parent();
	var edit_form = comment.find('.edit-comment-form');
	var delete_form = comment.find('.confirm-delete-form');
	edit_form.toggle();
	delete_form.hide();
});

$(document).on('click', '.delete-comment', function () {
	var comment = $(this).parent().parent().parent();
	var edit_form = comment.find('.edit-comment-form');
	var delete_form = comment.find('.confirm-delete-form');
	delete_form.toggle();
	edit_form.hide();
});

$(document).ready(function () {
	$("#tearsheetformid").submit(function () {
		$('#loadinggif').css('display', 'block');
	});
});


/* ====================utility funcions=========== */

function checkForm(event) {
	var $form = $(this.element);
	var id = event.target.id;
	var elements = document.querySelectorAll("#" + id + " input[type=text]")
	for (var i = 0; i < elements.length; i++) {
		element = elements[i++];
		if ($.trim(element.value) === "") {
			window.scrollTo(0, 0)
			document.getElementById('error_msg').innerHTML = 'Please fill in all the form fields'
			return false;
		}
	}
	document.getElementById('error_msg').innerHTML = ''
	return true
}

$('button[data-toggle=modal]').click(function () {
	$(".modal").modal();
});


function checkDate(event) {
	var now = new Date()
	var selected_date = event.target.value
	maxDate = now.toISOString().substring(0, 10);
	if (selected_date > maxDate) {
		event.target.value = maxDate
		document.getElementById("error_msg").innerHTML = 'Cannot select future dates.'
		window.scrollTo(0, 0)
		return false
	}
	else {
		document.getElementById("error_msg").innerHTML = ''
		return false
	}
}

function isNumber(evt) {
	var charCode = (evt.which) ? evt.which : evt.keyCode;
	if (charCode != 46 && charCode > 31
		&& (charCode < 48 || charCode > 57))
		return false;

	return true;
}

function removeElement(array, elem) {
	var index = array.indexOf(elem);
	if (index > -1) {
		array.splice(index, 1);
	}
}


function signUpTabClick() {
	window.location.href = '/accounts/sign-up';
}

function loginTabClick() {
	window.location.href = '/accounts/log-in';
}
