$(document).ready(function (){
    $('.increment-btn').click(function(e){
        e.preventDefault();
        var inc_value=$(this).closest('.product-data').find('.quantity-input').val();
        var value=parseInt(inc_value,10);
        value=isNaN(value)?0:value;
        if(value<10){
            value++;
            $(this).closest('.product-data').find('.quantity-input').val(value);
        }
    });



    $('.decrement-btn').click(function(e){
        e.preventDefault();
        var dec_value=$(this).closest('.product-data').find('.quantity-input').val();
        var value=parseInt(dec_value,10);
        value=isNaN(value)?0:value;
        if(value>1){
            value--;
            $(this).closest('.product-data').find('.quantity-input').val(value);
        }
    });
    
    $('.addCartBtn').click(function(e){
        e.preventDefault();
        var product_id=$(this).closest('.product-data').find('.product_id').val();
        var product_quantity=$(this).closest('.product-data').find('.quantity-input').val();
        token=$('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method:"POST",
            url:"/cart/add_to_cart/",
            data:{
                'product_id':product_id,
                'product_quantity':product_quantity,
                csrfmiddlewaretoken:token
            },
            dataType:"dataType",
            success:function(response){
                console.log(response)
            }
        })
    })

    $('.changeQuantity').click(function(e){
        e.preventDefault();
        var product_id=$(this).closest('.product-data').find('.product_id').val();
        var product_quantity=$(this).closest('.product-data').find('.quantity-input').val();
        token=$('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method:"POST",
            url:"/cart/update_cart/",
            data:{
                'product_id':product_id,
                'product_quantity':product_quantity,
                csrfmiddlewaretoken:token
            },
            dataType:"dataType",
            success:function(response){
                console.log(response)
            }
        })
    })

    


    


});