function addData(){
    var mobil = $('#mobil').val()
    var harga = $('#harga').val()

    $.ajax({
        url : 'add-data',
        type: 'post',
        data:{
            mobil : mobil,
            harga: harga
        },
        success : function(response){
            alert(`berhasil : ${response['result']}`)
            window.location.replace('/dashboard')
        }
    })
}