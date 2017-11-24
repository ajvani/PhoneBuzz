$(document).ready(function() {
    $('.opt').click(function() {
        if ($(this).hasClass('active-btn')) {
            return; 
        }

        var next_active = $(this);
        $.when($('.opt').removeClass('active-btn')).done(function() {
            $(next_active).addClass('active-btn'); 
        });

        var inner_id = '#' + $(this).html().toLowerCase().split(" ").join("_");
        $.when($('.page').fadeOut(250)).done(function() {
            $(inner_id).fadeIn(250);
        });
    }); 

    $('#phone_number').on('input', function() {
        var re = /^[0-9]{10}|\([0-9]{3}\) ?[0-9]{3}-[0-9]{4}|[0-9]{3}-[0-9]{3}-[0-9]{4}$/;

        if ($(this).val().match(re) == $(this).val()) {
            $(this).css('border-color', '#0db71c');
        } else {
            $(this).css('border-color', '#b70e0e'); 
        }
    });

    $('#delay').on('input', function() {
        var re = /^[0-9]+$/;

        if ($(this).val() == '' || $(this).val().match(re)) {
            $(this).css('border-color', '#0db71c');
        } else {
            $(this).css('border-color', '#b70e0e'); 
        }
    })
});    

