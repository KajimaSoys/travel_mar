$(document).ready(function(jQuery) {
    jQuery(function ($) {
        $.mask.definitions['9'] = "[1-5]";
        $('#id_type').mask('9', {placeholder: 'дд.мм.гггг'})
    });
});