$(function(){
    var onClick = function(e) {
        e.preventDefault();
        this.siblings().removeClass('active').end().addClass('active').parent();
        var mainSection = $('#nav .main .active').data('id');
        var subSection = $('#nav .sub .active').data('id');
        $('.module_container > div').hide();
        $('#' + mainSection + ' .' + subSection).show();
    }
    var PREFER_ID = "ksi";
    $('#nav .main a').each(function(i, a) {
        var $a = $(a);
        $a.on('click', onClick.bind($a));
        if ($a.data('id') === PREFER_ID) {
            $a.click();
        }
    });
    $('#nav .sub a').each(function(i, a) {
        var $a = $(a);
        $a.on('click', onClick.bind($a));
    });
});