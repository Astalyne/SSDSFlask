var cartDetails;

$(document).ready(function(){
	$('.checkout-box').hide();
});
// FUNCTION.............................................................................
function addToCart(btn){
	$('.checkout-box').hide();
	$('.list-group-item').remove();
	//getting price and item name
	var itemName = btn.parentElement.parentElement.getElementsByClassName('card-title')[0].innerHTML;
	console.log(itemName)
	var price = btn.parentElement.parentElement.getElementsByClassName('priceitem')[0].innerHTML;
	console.log(price)

	//constructing cart row
	var deleteButton = $("<td></td>").append('<button class="btn btn-primary delete-btn" onclick="deleteBtn(this)" type="button" style="background-color: rgb(166,22,13);font-size: 21px;">Delete</button>');
    var tableRow = $("<tr class='itemRow'></tr>").append(
    	$("<td class='itemName'></td>").text(itemName),
    	$("<td class='itemPrice'></td>").text(price),
    	$("<td></td>").append("<select onchange='itemPrice(this)' ><option value='1' selected>1</option><option value='2'>2</option><option value='3'>3</option> <option value='4'>4</option><option value='5'>5</option> </select>"),
    	$("<td class='totalItemprice'></td>").text(price),
    	deleteButton);

 	$(".cartItemsBody").append(tableRow);

 	totalPrice();
}

// FUNCTION.............................................................................
function itemPrice(quantity){
	itemQuantity = quantity.value;
	itemprice = quantity.parentElement.parentElement.getElementsByClassName('itemPrice')[0].innerHTML;
	totalprice = itemprice*itemQuantity;
	quantity.parentElement.parentElement.getElementsByClassName('totalItemprice')[0].innerHTML = totalprice;

	totalPrice();
	$('.checkout-box').hide();
	$('.list-group-item').remove();

}
// FUNCTION.............................................................................
function deleteBtn(dbtn){
	dbtn.parentElement.parentElement.remove();
	totalPrice()
	$('.checkout-box').hide();
	$('.list-group-item').remove();
}
// FUNCTION..............................................................................
function totalPrice(){
	totalprice = document.getElementsByClassName('totalItemprice');
	var cookieprice=0
	for(var i = 0; i<totalprice.length; i++){
		cookieprice += parseFloat(totalprice[i].innerHTML)
	}
	console.log(cookieprice)
	document.getElementById('totalprice').innerHTML = cookieprice +' SAR'
}
// FUNCTION..............................................................................CHECKOUT
function checkout(){

	$('.checkout-box').show('slow/400/fast', function() {

	});

//.........Checks if the checkout button was already clicked and the summary was already generated or not
//......... if yes, remove order summary
		if(!$(".item-checkout").empty()){
			$(".item-checkout").html().remove();
		}

    var orderSummary =$("<li class='list-group-item' id='order-summary'></li>").append(
										$('<h2 style="font-family: Roboto, sans-serif;color: rgb(255,255,255);"></h2>').text('Order Summary')
		);
	$(".item-checkout").append(orderSummary);

	var itemName = document.getElementsByClassName('itemName');
	var price = document.getElementsByClassName('totalItemprice')
	var totalitemprice=0;

	for(var i =0; i<itemName.length && i<price.length; i++){
		var listitem =	$("<li class='list-group-item summary_item'></li>").append(
						$("<div class='row'></div>").append(
															$("<div class='col'></div>").append(
																								$("<h3 name='fooditemName' class='fooditemName'></h3>").text(itemName[i].innerHTML)
																								),
															$("<div class='col'></div>").append(
																								$("<p name='fooditemPrice' class='fooditemPrice'></p>").text(price[i].innerHTML)
																								)
															)
				    );
		totalitemprice += parseFloat(price[i].innerHTML);
		$(".item-checkout").append(listitem);
	}
	var total = $("<li class='list-group-item'></li>").append(
						$("<div class='row'></div>").append(
															$("<div class='col'></div>").append(
																								$("<h3></h3>").text('TOTAL')
																								),
															$("<div class='col'></div>").append(
																								$("<p name='TotalPrice' id='TotalPrice'></p>").text(totalitemprice)
																								)
															)
				    );
	$(".item-checkout").append(total);


	var placeOrderBtn =$("<li class='list-group-item' id='place-order' style='padding: 0px;height: 45px;'></li>").append(
										$('<button class="btn btn-danger" id="placeOrderBtn" onclick="placeOrder()" style="width: 100%;height: 100%;font-size: 20px;"></button>').text('PLACE ORDER')
		);
	$(".item-checkout").append(placeOrderBtn);
}
