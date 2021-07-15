function set_return_url(cookie_val,patient_session_id,patient_id) {
        var return_url = '/scales/select_scales?patient_session_id='+patient_session_id+'&patient_id='+patient_id;
        if (cookie_val == 'detail')
                return_url = "/patients/get_patient_detail?patient_id="+patient_id;
        var aObj = document.getElementById("return_url");
        aObj.href = return_url;
}
function getCookie(name){
    var strCookie=document.cookie;
    var arrCookie=strCookie.split("; ");
    for(var i=0;i<arrCookie.length;i++){
        var arr=arrCookie[i].split("=");
        if(arr[0]==name)
            return arr[1];
    }
    return "";

}