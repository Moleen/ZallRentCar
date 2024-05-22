$('#date').datepicker({
    orientation: "bottom",
    autoclose:true,
    startDate:'0d',
    format:'yyyy-mm-dd',
    todayHighlight:true
})

function createTransaction(id_mobil){
    var user = 'foo'
    var hari = $('#hari').val();
    $.ajax({
        url : '/api/create_transaction',
        type : 'post',
        data : {
            user : user,
            hari : hari,
            id_mobil : id_mobil
        },
        success : function (response){
            window.location.replace(`/transaksi/${response.id}`)
        }
    })
}