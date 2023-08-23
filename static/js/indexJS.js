function popupForms() {
  
  document.querySelector('.closeBtn3').addEventListener('click',function(){
  document.querySelector('.success-form').style.display ='none';
  });
 
}

function disableCart(){
  var cartBtn = document.getElementById("cart");
  cartBtn.disabled = true;

  var cartIconBtn = document.getElementById("cartIcon");
  cartIconBtn.disabled = true;

  var addtocartBtn = document.getElementById("addtocart");
  addtocartBtn.disabled = true;
}

function changeStatus(){
  var element = document.getElementById("onlinestatus");
  element.style.backgroundColor = "green";
}

