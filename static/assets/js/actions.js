
(function($) {
    'use strict';
/*=============  Plus Minus Button ==============*/


    $(".cart-plus-minus").append('<div class="dec qtybutton">-</i></div><div class="inc qtybutton">+</div>');

    $(".qtybutton").on("click", function () {
        var $button = $(this);
        var oldValue = $button.parent().find("input").val();
        if ($button.text() == "+") {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            // Don't allow decrementing below zero
            if (oldValue > 1) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 1;
            }
        }
        $button.parent().find("input").val(newVal);
    });




/*=========== ScrollUp ===========*/

  $.scrollUp({
      scrollText: '<i class="fa fa-angle-up"></i>',
      easingType: 'linear',
      scrollSpeed: 900,
      animation: 'slideInRight'
  });


/*=========== Mobile Menu ===========*/

  $('nav.main__menu__nav').meanmenu({
    meanMenuClose: 'X',
    meanMenuCloseSize: '18px',
    meanScreenWidth: '991',
    meanExpandableChildren: true,
    meanMenuContainer: '.mobile-menu',
    onePage: true
  });



/*=========== ScrollReveal ===========*/

  window.sr = ScrollReveal({ duration: 700 , reset: false});
  sr.reveal('.foo');
  sr.reveal('.bar');



/*=========== Sticky Header ===========*/
function stickyHeader(){
    $(window).on('scroll', function(){
        var sticky_menu = $('.sticky__header');
        var pos = sticky_menu.position();
        if (sticky_menu.length) {
            var windowpos = sticky_menu.top;
            $(window).on('scroll', function() {
               var windowpos = $(window).scrollTop();
               if (windowpos > pos.top + 250) {
                   sticky_menu.addClass('is-sticky');
               } else {
                   sticky_menu.removeClass('is-sticky');
               }
            });
        }
    });
}
stickyHeader();


/*============= Checkout Login/Register Toggle ==============*/
    function checkoutLoginToggle(){
        var checkoutMethodList = $('.checkout-method-list li');
        checkoutMethodList.on('click', function(){
            var form = $(this).data('form');
            if( !$(this).hasClass('active') ) {
                $('.checkout-method-list li').removeClass('active');
                $(this).addClass('active');
                $('.checkout-method form').slideUp(500);
                $('.' + form).delay(500).slideDown();
            }
        });
    }
    checkoutLoginToggle();
    

/*============= Checkout Shipping Form Toggle ==============*/
    function checkoutShippingToggle(){
        var shipingFormToggle = $('.shipping-form-toggle');
        var shipingForm = $('.shipping-form');
        shipingFormToggle.on('click', function(){
            if( $(this).hasClass('active') ) {
                $(this).removeClass('active');
                shipingForm.slideUp();
            } else {
                $(this).addClass('active');
                shipingForm.slideDown();
            }
        });
    }
    checkoutShippingToggle();
    

/*============= Payment Method Toggle ==============*/
    function paymentMethodToggle(){
        var paymentMethodList = $('.payment-method-list li');
        var paymentFormToggle = $('.payment-form-toggle');
        var paymentForm = $('.payment-form');
        paymentMethodList.on('click', function(){
            paymentMethodList.removeClass('active');
            $(this).addClass('active');
            if( $(this).hasClass('payment-form-toggle') ) {
                paymentForm.slideDown()
            } else {
                paymentForm.slideUp()
            }
        });
    }
    paymentMethodToggle();

})(jQuery);