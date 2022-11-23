function decereseQuantity(qty,id,sub_total){
    var qty=$('#'+qty)
    var sub_total=$('#'+sub_total)
    console.log('heehheee')
    

    $.ajax({
        type:"GET",
        url:"/cart/decrease_quantity/",
        data:{
            'id':id
        },
        success : function(r){
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total)
            $('#total_price').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)
        },
        error:function(r){
            alert('Error Occured')
        }
    });
}


function increaseQuantity(qty,id,sub_total){
    var qty=$('#'+qty)
    var sub_total=$('#'+sub_total)
    console.log('heehheee ++')
    

    $.ajax({
        type:"GET",
        url:"/cart/increase_quantity/",
        data:{
            'id':id
        },
        success : function(r){
            $(qty).val(r.quantity)
            $(sub_total).text("₹"+r.sub_total)
            $('#total').text("₹"+r.total)
            $('#total_price').text("₹"+r.total_price)
            $('#saved').text("-"+r.saved)
            
        },
        error:function(r){
            alert('Error Occured')
        }
    });
}