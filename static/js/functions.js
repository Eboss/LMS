function time_diff(){
    var From_date=document.getElementById('From_date').value;
    var To_date=document.getElementById('To_date').value; 
    var date1 = new Date(From_date);
    var date2 = new Date(To_date);
    var timeDiff = Math.abs(date2.getTime() - date1.getTime());
    var diffDays = Math.ceil(timeDiff / (1000 * 3600 * 24)); 
    if (!isNaN(diffDays)) {
    console.log(diffDays);
    document.getElementById('WDapply').value=diffDays;

    };
};
function Save(){
    var Timeoff=document.getElementById('Timeoff').value;
    var leavetype = document.getElementById('leavetype').value;
    var remark = document.getElementById('remark').value;
    var From_date=document.getElementById('From_date').value;
    var To_date=document.getElementById('To_date').value; 
    var WDapply = document.getElementById('WDapply').value;
    alert(WDapply);
 
    var all={
      Timeoff:Timeoff,
      From_date:From_date,
      To_date:To_date,
      leavetype:leavetype,
      WDapply:WDapply,      
      remark:remark,
    };      
    $.ajax({
      type:'POST',
      url:'/leaveform/',
      data:{
           all:all,
         csrfmiddlewaretoken: '{{csrf_token}}'
      },
    success: function (response) {
        console.log(response);
        if (response="saved")
          {
            alert('ok');
          }
            }
            });
}
