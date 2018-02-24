function is_sendmail(){
    if($("input[name='send_mail']").is(':checked')){
        $("input[name='send']").val('true');
    }
    else{
        $("input[name='send']").val('false');
    }
}

$(function (){
    $("#id_report_email,#id_session_id,#id_subject_id,#id_project_id,#id_apply_email,#id_report_type").chosen();

    $("#id_report_email option").each(function(i){
        if($(this).is(':selected')){
            $("#id_report_email_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_report_email_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_report_email_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_report_email_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });

    $("#id_session_id option").each(function(i){
        if($(this).is(':selected')){
            $("#id_session_id_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_session_id_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_session_id_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_session_id_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });

    $("#id_subject_id option").each(function(i){
        if($(this).is(':selected')){
            $("#id_subject_id_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_subject_id_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_subject_id_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_subject_id_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });

    $("#id_project_id option").each(function(i){
        if($(this).is(":selected")){
            $("#id_project_id_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_project_id_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_project_id_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_project_id_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });


    $("#id_apply_email option").each(function(i){
        if($(this).is(':selected')){
            $("#id_apply_email_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_apply_email_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_apply_email_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_apply_email_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });

    $("#id_report_type option").each(function(i){
        if($(this).is(':selected')){
            $("#id_report_type_chzn .chzn-single").attr("data-content",$(this).attr("data-content"));
            $("#id_report_type_chzn .chzn-single").attr("data-title",$(this).attr("data-title"));
        }
        $("#id_report_type_chzn_o_"+i).attr("data-content",$(this).attr("data-content"));
        $("#id_report_type_chzn_o_"+i).attr("data-title",$(this).attr("data-title"));
    });
    $(".active-result,.chzn-single").on('mouseover',function(){
         $(this).popover({
             trigger: 'manual',
             placement: 'right',
             html:true,
         }).popover('toggle');
    
    });
    $(".active-result,.chzn-single").on('mouseleave',function(){
        $(this).popover('destroy');
    });
    $("#id_subject_id").chosen().change(function(){
            $("#id_subject_id_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_subject_id_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });
    $("#id_project_id").chosen().change(function(){
            $("#id_project_id_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_project_id_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });

    $("#id_apply_email").chosen().change(function(){
            $("#id_apply_email_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_apply_email_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });

    $("#id_report_type").chosen().change(function(){
            $("#id_report_type_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_report_type_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });

    $("#id_session_id").chosen().change(function(){
            $("#id_session_id_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_session_id_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });
    $("#id_report_email").chosen().change(function(){
            $("#id_report_email_chzn .chzn-single").attr("data-content",$(this).find("option:selected").attr("data-content"));
            $("#id_report_email_chzn .chzn-single").attr("data-title",$(this).find("option:selected").attr("data-title"));
    });
});

