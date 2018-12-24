/*
 * Change Navbar color while scrolling
*/
$(document).ready(function(){

$(window).scroll(function(){
    $(".slideanim").each(function(){
      var pos = $(this).offset().top;

      var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
          $(this).addClass("slide");
        }
    });
	handleTopNavAnimation();
});

});

$(document).ready(function () {
    if (window.location.href.indexOf('#invalidlogin') != -1) {
        $('#invalidlogin').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#authrequired') != -1) {
        $('#authrequired').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#authreq2') != -1) {
        $('#authreq2').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#invalidsignup') != -1) {
        $('#invalidsignup').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#userexists') != -1) {
        $('#userexists').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#success') != -1) {
        $('#success').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#passwordresetsuccess') != -1) {
        $('#passwordresetsuccess').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#passwordreseterror') != -1) {
        $('#passwordreseterror').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#404') != -1) {
        $('#404').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#mailsent') != -1) {
        $('#mailsent').modal('show');
    }
});

function handleTopNavAnimation() {
	var top=$(window).scrollTop();

	if(top>10){
		$('#site-nav').addClass('navbar-solid'); 
	}
	else{
		$('#site-nav').removeClass('navbar-solid'); 
	}
}

/*
 * Registration Form
*/

$('.navbar-nav>li>a').not("#aboutlink").on('click', function(){
    $('.navbar-collapse').collapse('hide');
});
/*
 * SmoothScroll
*/

smoothScroll.init();

function validateAndSignUp() {
    var email = document.getElementById("signupemail").value;
    var phone = document.getElementById("signupcontact").value;
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email) && phone.match(/^\d{10}$/)) {
        $(userRegisterFrm).submit();
    }
    else {
        $('#modal').modal('hide');
        $('#invalidemail').modal('show');
    }
}

function validateAndLogin() {
    var email = document.getElementById("loginemail").value;
    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
        $(userLgnFrm).submit();
    } else {
        $('#modal').modal('hide');
        $('#invalidemail').modal('show');
    }
}

$('#invalidemail').on('hidden.bs.modal', function () {
    $('#modal').modal('show');
})

$('#invalidlogin').on('hidden.bs.modal', function () {
    window.location.hash = '';
    $('#modal').modal('show');
})

$('#success').on('hidden.bs.modal', function () {
    window.location.hash = '';
})

$('#passwordresetsuccess').on('hidden.bs.modal', function () {
    window.location.hash = '';
})

$('#passwordreseterror').on('hidden.bs.modal', function () {
    window.location.hash = '';
})

$('#mailsent').on('hidden.bs.modal', function () {
    window.location.hash = '';
})

$('#404').on('hidden.bs.modal', function () {
    window.location.hash = '';
})

$('#invalidsignup').on('hidden.bs.modal', function () {
    window.location.hash = '';
    $('#modal').modal('show');
})

$('#userexists').on('hidden.bs.modal', function () {
    window.location.hash = '';
    $('#modal').modal('show');
})

$('#authrequired').on('hidden.bs.modal', function () {
    window.location.hash = '';
    $('#modal').modal('show');
})

$('#authreq2').on('hidden.bs.modal', function () {
    window.location.hash = '';
    $('#modal').modal('show');
})