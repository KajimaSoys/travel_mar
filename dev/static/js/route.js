$(document).ready(function(jQuery) {
    jQuery(function ($) {
        let count;
        let discount = id_exempt.value;
        let cost = id_cost.value;
        let amount = id_amount.value;
        let returnCost = id_returnCost.value;
        let amount_field = $('input#id_amount');
        amount_field.attr('disabled', true);
        let returnCost_field = $('input#id_returnCost');
        returnCost_field.attr('disabled', true);
        let exempt_field = $('input#id_exempt');
        exempt_field.attr('disabled', true);

        document.querySelector('select[name="clients"]').onchange=function() {
            count = $(this).find("option:selected").length;
            console.log(count);
            discount_calc();
        };

        $('#id_cost').on('change', function() {
            cost = id_cost.value;
            last_calc();
        });

        $('.add-row').on('click', function () {
            console.log('added new inline point')
            $('.vDateField').mask('99.99.2099', {placeholder: 'дд.мм.20гг'})
            $('.vTimeField').mask('99:99:00', {placeholder: 'чч.мм.00'})
        });

        function discount_calc(){
            if (count === 1){
                id_exempt.value = 0;
                discount = 0;
            } else if (count === 0){
                id_exempt.value = 0;
                discount = 0;
            } else if (count > 5){
                id_exempt.value = 10;
                discount = 10;
            } else if (count === 2){
                id_exempt.value = 3;
                discount = 3;
            } else if (count > 2){
                id_exempt.value = 5;
                discount = 5;
            }
            last_calc()
        }

        function last_calc(){
            amount = cost * (100-discount)/100;
            id_amount.value = amount;
            returnCost = amount * 0.4;
            id_returnCost.value = returnCost;
        }

        $('.vDateField').mask('99.99.2099', {placeholder: 'дд.мм.20гг'})
        $('.vTimeField').mask('99:99:00', {placeholder: 'чч.мм.00'})


        var frm = $('form');
        var chosenBtn = frm.find('[name="_save"]');
        var btns = frm.find('[name="_save"], [name="_addanother"], [name="_continue"]');
        btns.unbind('click.btnAssign').bind('click.btnAssign', function(e)
        {
            chosenBtn = $(this);
        });
        frm.unbind('submit.saveStuff').bind('submit.saveStuff', function(e)
        {

            amount_field.attr("disabled", false);
            returnCost_field.attr("disabled", false);
            exempt_field.attr('disabled', false);

            frm.append(
            [
                '<input type="hidden" name="',
                chosenBtn.attr('name'),
                '" value="',
                chosenBtn.attr('value'),
                '" />'
            ].join(''));
        });
    });
});