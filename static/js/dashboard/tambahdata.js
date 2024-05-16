

function addData(){

    $.ajax({
        url : 'add-data',
        type: 'post',
        data:{
            merek : $('#merek').val(),
            model: $('#model').val(),
            tahun : $('#tahunM').val(),
            warna : $('#warna').val(),
            harga: $('#harga').val()
        },
        success : function(response){
            alert(`berhasil : ${response['result']}`)
            window.location.replace('/dashboard/product')
        }
    })
}