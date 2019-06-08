$(document).ready(function(){


//Change Username label from Django backend form to Email*
let usernameText = $("#div_id_username .col-form-label")
usernameText.text('Email*')


//Change orange pratik to grey
// let pratik = $(".favBtn")

// pratik.click(function(){
//     // alert('yoYo')
//     // $(this).attr("src", "/static/resources/img/pratik.png")
//     // $(this).toggleClass("pratik")
//     // $(this).toggleClass("pratik-selected")
//     var src = $(this).attr('src');
//     var newsrc = (src=='/static/resources/img/pratik.png') ? '/static/resources/img/pratik-selected.png' : '/static/resources/img/pratik.png';
//     $(this).attr('src', newsrc );
// })

// Change grey pratik to orange
// let pratik = $(".pratik")

// pratik.click(function(){
//     $(this).attr("src", "/static/resources/img/pratik-selected.png")
//     $(this).toggleClass("pratik-selected")
//     $(this).toggleClass("pratik")
// })

//Animate dropdown menu
let x = true
$(".dropdown-animator, .drpdwn-item").click(function(){
    if (x==true){
        anime({
            targets: '.appear-on-dropdown',
            opacity: 1,
            easing: 'easeInOutQuad',
        });
        x = !x
        console.log("opacity1")
    } else {
        anime({
            targets: '.appear-on-dropdown',
            opacity: 0,
            easing: 'easeInOutQuad',
        });
        x = !x
        console.log("opacity0")
    }
});



});



