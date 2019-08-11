$(document).ready(function(){

// Request audio recording
//https://developers.google.com/web/updates/2012/09/Live-Web-Audio-Input-Enabled
//https://www.html5rocks.com/en/tutorials/getusermedia/intro/

// window.AudioContext = window.AudioContext ||
//                       window.webkitAudioContext;

// const context = new AudioContext()

// navigator.mediaDevices.getUserMedia({audio: true}).
//   then((stream) => {
//     const microphone = context.createMediaStreamSource(stream);
//     const filter = context.createBiquadFilter()
//     // microphone -> filter -> destination
//     microphone.connect(filter)
//     filter.connect(context.destination)
// })

//Change Username label from Django backend form to Email*
let usernameText = $("#div_id_username .col-form-label")
usernameText.text('Email*')

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



