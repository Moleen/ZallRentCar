import { addStatusLabel, changeCurrency  } from './function.js';

$(document).ready(function () {
  addStatusLabel();
  changeCurrency()
});

$('#filter_transaksi').on('change', function(){
  $('#tanggal_input').remove()
  var filter = $(this).val()
  

  if( filter == '1'){
    
    $('#tanggal').attr('hidden' ,false)
    $('#tanggal').append('<input type="text" name="" id="tanggal_input">')
    $("#tanggal_input").datepicker({
      dateFormat: "dd-mm-yy",
      changeMonth: true,
      changeYear: true,
      yearRange: "1900:2100"
  });

  $('#tanggal_input').on('change',function(){
    $(this).attr('disabled', true)
    $.ajax({
      type: 'POST',
      url : '/api/filter_transaksi',
      data :{
        mtd :'fTanggal',
        date : $(this).val()
      },
      success : function(response){
        
      }
    })
  })



    
  }else if(filter == '2'){
    console.log('ini sudah bayar');

  }else if(filter == '3'){
    console.log('ini belum bayar');
  }
})
