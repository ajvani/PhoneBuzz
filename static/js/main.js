$(document).ready(function() {
    $('.opt').click(function() {
        var next_active = $(this);
        $.when($('.opt').removeClass('active-btn')).done(function() {
            $(next_active).addClass('active-btn'); 
        });

        var inner_id = '#' + $(this).html().toLowerCase().split(" ").join("_");
        $.when($('.page').fadeOut(250)).done(function() {
            $(inner_id).fadeIn(250);
        });
    }); 
});    
