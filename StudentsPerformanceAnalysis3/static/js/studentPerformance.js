
$(document).ready(function() {

    $('#present').click(function(){
    var pk;
    pk = $(this).attr("data-pk");
     $.get('/teachers/setAttendanceStatus/'+pk+'/',function(data){
            alert('hie')
           });
});

});
