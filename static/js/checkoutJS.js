document.querySelector('.closeBtn').addEventListener('click', function () {
    document.querySelector('.payment-form').style.display = 'none';
});
document.querySelector('.purchase').addEventListener('click', function () {
    document.querySelector('.payment-form').style.display = 'flex';
});
document.querySelector('#purchase').addEventListener('click', function () {
    document.querySelector('.payment-form').style.display = 'flex';
});

document.querySelector('.cashondeliverybtn').addEventListener('click', function () {
    document.querySelector('.cashondelivery-form').style.display = 'flex';
});
document.querySelector('.closeBtn1').addEventListener('click', function () {
    document.querySelector('.cashondelivery-form').style.display = 'none';
});

document.querySelector('.creditcardbtn').addEventListener('click', function () {
    document.querySelector('.creditcard-form').style.display = 'flex';
});
document.querySelector('.closeBtn2').addEventListener('click', function () {
    document.querySelector('.creditcard-form').style.display = 'none';
});

function updateTotal() {
    const totalAmountElements = document.querySelectorAll('#totalAmount');
    totalAmountElements.forEach(element => {
        const totalValue = 'PHP ' + element.getAttribute('data-total');
        element.textContent = totalValue;
    });
}
window.addEventListener("DOMContentLoaded", updateTotal);
function changeStatus(){
    var element = document.getElementById("onlinestatus");
    element.style.backgroundColor = "green";
}
