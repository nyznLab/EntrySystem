$('input.scale_form[type=radio]').change(function () {
    if ($(this).prop('checked')===true) {
                    $(this).siblings().css({'background-color': '#2a3f54', 'color': '#efefef'})
                    $(this).parent().siblings('div').children('label').css({'background-color':'#efefef','color':'#73879C'})
    }
});
