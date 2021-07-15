$('#modal_container_subjectBaseInfo_build').on('show.bs.modal', function(){
    var $this = $(this);
    var $modal_dialog = $this.find('.modal-dialog');
    $this.css('display', 'block');
    $modal_dialog.css({'margin-top': 200 });

});

function Subject_information_submit(){
    var scale = document.subjectEstablishForm.scale;
    var a = document.subjectEstablishForm.scale_selected;
    if(scale[0].checked){
            alert(scale[0].value);
            document.subjectEstablishForm.action="/patients/subjectEstablish";
        }
    else if(scale[1].checked){
           alert(scale[1].value);
           document.subjectEstablishForm.action='/patients/subjectSelfTest';
    }
    else if(scale[2].checked){
        alert(scale[2].value)
           document.subjectEstablishForm.action='/patients/subjectCognitionTest';
    }
}

<!--独生子女-->
$(".only_child_1").on('ifChecked', function(event){
      $("#brother_num_1").hide();
      $("#brother_num_2").hide();
      $(".brother_num_2_val").val("");
});
$(".only_child_2").on('ifChecked', function(event){
      $("#brother_num_1").show();
      $("#brother_num_2").show();
});
<!--收养-->
$("#patient_adopt_2").on('ifChecked', function(event){
      $("#adopt_age_1").hide();
      $("#adopt_age_2").hide();
      $("#adopt_age_2").val("");
});
$("#patient_adopt_1").on('ifChecked', function(event){
      $("#adopt_age_1").show();
      $("#adopt_age_2").show();
});
<!--学生干部-->
$("#patient_leader_2").on('ifChecked', function(event){
      $("#patient_leader_occupation").attr("disabled", true);
      $("#patient_leader_occupation").val("");
});
$("#patient_leader_1").on('ifChecked', function(event){
      $("#patient_leader_occupation").removeAttr("disabled");
});
<!--住校-->
$("#patient_live_school_2").on('ifChecked', function(event){
      $("#patient_home_frequency").attr("disabled", true);
      $("#patient_home_frequency").val("");
});
$("#patient_live_school_1").on('ifChecked', function(event){
      $("#patient_home_frequency").removeAttr("disabled");
});
<!--躯体疾病-->
$("#patient_somatic_diseases_1").on('ifChecked', function(event){
      $("#patient_somatic_diseases_name").removeAttr("disabled");
      $("#patient_somatic_diseases_year").removeAttr("disabled");
});
$("#patient_somatic_diseases_2").on('ifChecked', function(event){
      $("#patient_somatic_diseases_name").attr("disabled", true);
      $("#patient_somatic_diseases_year").attr("disabled", true);
      $("#patient_somatic_diseases_name").val("");
      $("#patient_somatic_diseases_year").val("");
});
<!--精神疾病-->
$("#patient_mental_diseases_1").on('ifChecked', function(event){
      $("#patient_mental_diseases_name").removeAttr("disabled");
      $("#patient_mental_diseases_year").removeAttr("disabled");
});
$("#patient_mental_diseases_2").on('ifChecked', function(event){
      $("#patient_mental_diseases_name").attr("disabled", true);
      $("#patient_mental_diseases_year").attr("disabled", true);
      $("#patient_mental_diseases_name").val("");
      $("#patient_mental_diseases_year").val("");
});
<!--家族史-->
$("#patient_family_diseases_history_1").on('ifChecked', function(event){
      $("#patient_family_diseases_name").removeAttr("disabled");
});
$("#patient_family_diseases_history_2").on('ifChecked', function(event){
      $("#patient_family_diseases_name").attr("disabled", true);
      $("#patient_family_diseases_name").val("");
});
<!--吸烟-->
$("#patient_smoke_1").on('ifChecked', function(event){
      $("#patient_smoke_age").removeAttr("disabled");
      $("#patient_daily_smoke_num").removeAttr("disabled");
});
$("#patient_smoke_2").on('ifChecked', function(event){
      $("#patient_smoke_age").attr("disabled", true);
      $("#patient_daily_smoke_num").attr("disabled", true);
      $("#patient_smoke_age").val("");
      $("#patient_daily_smoke_num").val("");
});
<!--其他物质-->
$("#patient_other_abuse_2").on('ifChecked', function(event){
      $("#patient_other_abuse_age").attr("disabled", true);
      $("#patient_other_abuse_age").val("");
});
$("#patient_other_abuse_1").on('ifChecked', function(event){
      $("#patient_other_abuse_age").removeAttr("disabled");
});
<!--重大生活事件-->
$("#patient_big_event_2").on('ifChecked', function(event){
      $("#patient_big_event_describtion").attr("disabled", true);
      $("#patient_big_event_describtion").val("");
});
$("#patient_big_event_1").on('ifChecked', function(event){
      $("#patient_big_event_describtion").removeAttr("disabled");
});
<!--父母婚姻状态-->
$("#parent_marry").change(function(){
       var val = $("#parent_marry").val();
<!--       离异-->
       if (val == "2"){
              $(".StepParents").show();
              $(".patient_parent_death_age").hide();
              $(".patient_parent_death").hide();
              $(".patient_parent_death_age").val("");
<!--有一方过世-->
       }else if(val == "4"){
              $(".patient_parent_death_age").show();
              $(".patient_parent_death").show();
              $(".StepParents").hide();
       }else{
              $(".patient_parent_death_age").hide();
              $(".StepParents").hide();
              $(".patient_parent_death").hide();
              $(".patient_parent_death_age").val("");
       }
});
<!--饮酒-->
$("#patient_alcohol").change(function(){
       var val = $("#patient_alcohol").val();
       if (val == "1"){
             $("#patient_alcohol_age").attr("disabled", true);
       }else{
             $("#patient_alcohol_age").removeAttr("disabled");
       }
});
<!--少数民族-->
$("#nation").change(function(){
       var val = $("#nation").val();
       if (val == "0"){
           $(".minority").hide();
           $(".minority").val("");
       }else if(val == "1"){
           $(".minority").show();
       }
});
<!--居住方式 其他居住方式-->
$("#patient_live_type").change(function(){
       var val = $("#patient_live_type").val();
       if (val == "6"){
           $(".patient_live_type_other").show();

       }else{
           $(".patient_live_type_other").hide();
           $(".patient_live_type_other").val("");
       }
});