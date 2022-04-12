$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,  
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})


//this plus-cart is the class we took from html page  and click is the button that when pressed the other function runs
//this plus-cart class is made icon in this
$('.plus-cart').click(function(){  
    var id = $(this).attr("pid").toString();   //we need to send thid id to server and for that we used AJAX
    //the current of the object with class pid pid="{{cart.product.id}} from html page we'll get in the form of string
   // console.log(id)  // this console is in f12 button on google
  
   //for quantity
   //<!--now we want to change quantity also and for that we have to use ajax ,  for changing quatity 
   //we'll go to class class="plus-cart btn" parent class node class="my-3" and its 2nd child node to change the quantity and
   // that too we have to call it in ajax and change the inner text--> this is based on template add to cart
    
    var eml = this.parentNode.children[2]  // cart.quantity is the 2nd children
 //eml is the short for element
//we could have also have done this quantity update jsut like the above approach of id

    //this below code is fo quantity which we need to change
    $.ajax({
        type:"GET",
        url:"/pluscart", //we need to send data below to this url and we have to create that url
        data:{        
            prod_id:id  
        },
        //now we'll get function success   
                         //this is data we get in the form of object from views.py JsonResponse
        success:function (data) {
           // console.log(data)  //before the quantity we were getting quantity, amount, total amount in the console

           //below is the code for inner text not inner html for quantiy
           eml.innerText = data.quantity  // and now quantity will get store

           //now we have to show amount and total amount after we add more products
           //so for this in the add to cart.html we'll create span and put and id so that our task become easy and same is with total_amount where we'll put id in the <strong>
           document.getElementById("amount").innerText = data.amount
           document.getElementById("total_amount").innerText = data.total_amount

        }
    })
})


////////////////////now here we'll be doing it for minus cart 

//this minus-cart is the class we took from html page  and click is the button that when pressed the other function runs
//this minus-cart class is made icon in this
$('.minus-cart').click(function(){  
    var id = $(this).attr("pid").toString();   //we need to send thid id to server and for that we used AJAX
    //the current of the object with class pid pid="{{cart.product.id}} from html page we'll get in the form of string
   // console.log(id)  // this console is in f12 button on google
  
   //for quantity
   //<!--now we want to change quantity also and for that we have to use ajax ,  for changing quatity 
   //we'll go to class class="minus-cart btn" parent class node class="my-3" and its 2nd child node to change the quantity and
   // that too we have to call it in ajax and change the inner text--> this is based on template add to cart
    
    var eml = this.parentNode.children[2]  // cart.quantity is the 2nd children
 //eml is the short for element
//we could have also have done this quantity update jsut like the above approach of id

    //this below code is fo quantity which we need to change
    $.ajax({
        type:"GET",
        url:"/minuscart", //we need to send data below to this url and we have to create that url
        data:{        
            prod_id:id  
        },
        //now we'll get function success   
                         //this is data we get in the form of object from views.py JsonResponse
        success:function (data) {
           // console.log(data)  //before the quantity we were getting quantity, amount, total amount in the console

           //below is the code for inner text not inner html for quantiy
           eml.innerText = data.quantity  // and now quantity will get store

           //now we have to show amount and total amount after we add more products
           //so for this in the add to cart.html we'll create span and put and id so that our task become easy and same is with total_amount where we'll put id in the <strong>
           document.getElementById("amount").innerText = data.amount
           document.getElementById("total_amount").innerText = data.total_amount

        }
    })
})




////////////////////now here we'll be doing it for remove cart 

//this remove-cart is the class we took from html page  and click is the button that when pressed the other function runs
//this remove-cart class is made icon in this

//here we don't need to pass quantity 
$('.remove-cart').click(function(){  
    var id = $(this).attr("pid").toString();   //we need to send thid id to server and for that we used AJAX
    //the current of the object with class pid pid="{{cart.product.id}} from html page we'll get in the form of string
   // console.log(id)  // this console is in f12 button on google
  
   //for quantity
   //<!--now we want to change quantity also and for that we have to use ajax ,  for changing quatity 
   //we'll go to class class="-cart btn" parent class node class="my-3" and its 2nd child node to change the quantity and
   // that too we have to call it in ajax and change the inner text--> this is based on template add to cart
    
    var eml = this  // this is basically the current object
 //eml is the short for element
//we could have also have done this quantity update jsut like the above approach of id

    //this below code is fo quantity which we need to change
    $.ajax({
        type:"GET",
        url:"/removecart", //we need to send data below to this url and we have to create that url
        data:{        
            prod_id:id  
        },
        //now we'll get function success   
                         //this is data we get in the form of object from views.py JsonResponse
        success:function (data) {
           // console.log(data)  //before the quantity we were getting quantity, amount, total amount in the console

           //below is the code for inner text not inner html for quantiy
         

           //now we have to show amount and total amount after we add more products
           //so for this in the add to cart.html we'll create span and put and id so that our task become easy and same is with total_amount where we'll put id in the <strong>
           document.getElementById("amount").innerText = data.amount
           document.getElementById("total_amount").innerText = data.total_amount

           //now we'll remove the object by holding the eml above in which we put the object 
           //and then we go to parent node and it's parent node and so on which represents div
           eml.parentNode.parentNode.parentNode.parentNode.remove()  //by this our whole item will be removed in template page 
        }
    })
})