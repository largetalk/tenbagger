$(function (){

});

function checktime(){
    var start_time = $(".start_time").val();
    var end_time = $(".end_time").val();
    
    var s=start_time.split(" ");
    var d=s[0].split("-");
    var t=s[1].split(":");

    var e=end_time.split(" ");
    var d1=e[0].split("-");
    var t1=e[1].split(":");

    var stt = new Date(d[0],(d[1]-1),d[2],t[0],t[1]);
    stt = stt.getTime();

    var edt = new Date(d1[0],(d1[1]-1),d1[2],t1[0],t1[1]);
    edt = edt.getTime();

    if(stt >= edt){
        bootbox.alert('开始时间必须小于结束时间！');
        return false;
    }
}

function CountdownRedirect(secs,url){ 
URL =url; 
for(var i=secs;i>=0;i--) 
{ 
window.setTimeout('doUpdate(' + i + ')', (secs-i) * 1000); 
} 
} 
function doUpdate(num) 
{ 
document.getElementById('ShowSpan').innerHTML = '将在'+num+'秒后自动跳转' ; 
if(num == 0) { window.location=URL; } 
} 
