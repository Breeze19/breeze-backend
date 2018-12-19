function hideDiv(){

    if ($(window).width() < 765) {

            $("#image").fadeOut("slow");

    }else{

        $("#image").fadeIn("slow");

    }

}

$(document).ready(function () {

    
    hideDiv();

    
    $(window).resize(function(){
        hideDiv();
    });

});

$(document).ready(function () {
    if (window.location.href.indexOf('#passworderror') != -1) {
        $('#passworderror').modal('show');
    }
});
