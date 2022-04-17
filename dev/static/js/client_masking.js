$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $('#id_born').mask('99.99.9999', {placeholder: 'дд.мм.гггг'})
        $('#id_date').mask('99.99.9999', {placeholder: 'дд.мм.гггг'})
    });
});