$(document).ready(function(){

    //Using howler.js

    var sound = new Howl({
        src: ['../../../media/songs/a.mp3']
    });

    duration.innerHTML = self.formatTime(Math.round(sound.duration()));

    $('.play-button').click(function(){
        console.log("Yousefo")
        sound.play();
    })

    $('.card').click(function(){
        console.log("Masefi")
        sound.seek(60);
    });
    
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



