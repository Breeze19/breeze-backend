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
