

function addData(){

    $.ajax({
        url : 'add-data',
        type: 'post',
        data:{
            merek : $('#merek').val(),
            seat: $('#seat').val(),
            transmisi : $('#transmisi').val(),
            harga: $('#harga').val()
        },
        success : function(response){
            alert(`berhasil : ${response['result']}`)
            window.location.replace('/dashboard/data_mobil')
        }
    })
}