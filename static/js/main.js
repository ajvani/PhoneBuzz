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
            $(this).removeClass('invalid-button');
            $(this).addClass('valid-button');
        } else {
            $(this).removeClass('valid-button');
            $(this).addClass('invalid-button');
        }

        update_button();
    });

    $('#delay').on('input', function() {
        var re = /^[0-9]+$/;

        if ($(this).val() == '' || $(this).val().match(re)) {
            $(this).removeClass('invalid-button');
            $(this).addClass('valid-button');
        } else {
            $(this).removeClass('valid-button');
            $(this).addClass('invalid-button');
        }

        update_button();
    });

    $('#receive_button').on('click', function() {
        var delay = $('#delay').val();
        
        if (delay == '') {
            delay = '0';
        }

        $('#success_message').show();
    });

    $('#receive_form').submit(function() {
        var delay = $('#delay').val();
        
        if (delay == '') {
            delay = '0';
        }

        $.ajax({
            type: 'POST',
            url: '/handle_outgoing',
            data: {
                phone_number: $('#phone_number').val(),
                delay: delay
            }
        });

        return false;
    });
});    

function update_button() {
    if ($('#phone_number').hasClass('invalid-button') || $('#delay').hasClass('invalid-button')) {
        $('#receive_button').addClass('disabled-button');
    } else {
        $('#receive_button').removeClass('disabled-button');
    }
}

