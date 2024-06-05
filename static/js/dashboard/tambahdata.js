
$(document).ready(function(){

    $('#input-file').change(function (e) {
        file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function (event) {
                $("#imgPreview").attr("src", event.target.result);
                $("#imgPreview").removeAttr('hidden');
            };
            reader.readAsDataURL(file);
        }
    });

})

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