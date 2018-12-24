$(document).ready(function () {
    if (window.location.href.indexOf('#error') != -1) {
        $('#error').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#success') != -1) {
        $('#success').modal('show');
    }
});

$(document).ready(function () {
    if (window.location.href.indexOf('#accsuccess') != -1) {
        $('#accsuccess').modal('show');
    }
});

$('#error').on('hidden.bs.modal', function () {
    window.location.hash = ''
})

$('#success').on('hidden.bs.modal', function () {
    window.location.hash = ''
})

$('#accsuccess').on('hidden.bs.modal', function () {
    window.location.hash = ''
})