$(document).ready(function(){
    $('.pure-input-2-3').attr('disabled', 'disabled');
    $('#option-one').click(function(){
        $('#id_query').removeAttr('disabled');
        $('#id_query').attr('required', 'required');
        $('#id_count1').removeAttr('disabled');
        $('#id_count1').attr('required', 'required');
        $('#id_result_type').removeAttr('disabled');
        $('#id_date').removeAttr('disabled');
        $('#id_usernames').attr('disabled', 'disable');
        $('#id_usernames').removeAttr('required');
        $('#id_count').attr('disabled', 'disable');
        $('#id_count').removeAttr('required');
        $(':button').removeClass('pure-button pure-button-disabled');
        $(':button').addClass('pure-button pure-button-primary');
    });
    $('#option-two').click(function(){
        $('#id_usernames').removeAttr('disabled');
        $('#id_usernames').attr('required', 'required');
        $('#id_count').removeAttr('disabled');
        $('#id_query').attr('disabled', 'disable');
        $('#id_query').removeAttr('required');
        $('#id_count1').attr('disabled', 'disable');
        $('#id_count1').removeAttr('required');
        $('#id_result_type').attr('disabled', 'disable');
        $('#id_date').attr('disabled', 'disable');
        $(':button').removeClass('pure-button pure-button-disabled');
        $(':button').addClass('pure-button pure-button-primary');
    });
    $(':button').click(function(){
        $('#p').removeAttr('hidden');
    });
});
