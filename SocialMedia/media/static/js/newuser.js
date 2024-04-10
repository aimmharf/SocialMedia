document.addEventListener("DOMContentLoaded", function(){
    document.querySelector(".body-super-container").style.display = 'none';
   setIntroduction()
    document.querySelector("#btn-setup-profile").addEventListener("click", setContent)
    document.querySelector("#btn-submit").addEventListener("click" ,submitContent)
})


function setIntroduction() {
    document.querySelector("#to").style.opacity = '0';
    document.querySelector("#talkme").style.opacity = '0';
    document.querySelector("#btn-setup-profile").style.opacity = '0';
    document.querySelector("#skip-setting-profile").style.opacity = '0';
    document.querySelector("#welcome").style.animation = 'k 1s';
    setTimeout(function() {
        document.querySelector("#to").style.animation = 'k 3s';
        document.querySelector("#to").style.opacity = '1';
    }, 1100)
    setTimeout(function() { 
        document.querySelector("#talkme").style.animation = 'k 3s';
        document.querySelector("#talkme").style.opacity = '1'
    }, 1200)
    setTimeout(function() {
        document.querySelector("#btn-setup-profile").style.animation = 'k 3s';
        document.querySelector("#skip-setting-profile").style.animation = 'k 3s'
        document.querySelector("#skip-setting-profile").style.opacity = '1';
        document.querySelector("#btn-setup-profile").style.opacity = '1'
    }, 3000)
    
   
}   



function setContent() {
    document.querySelector("body").style.backgroundImage = 'linear-gradient(to bottom right, #FDFCFB, #E2D1C3)'
    document.querySelector("body").style.height = '100vh'
    document.querySelector(".super-container").style.display = 'none';
    document.querySelector(".body-super-container").style.display = 'grid';
    document.querySelector(".body-super-container").style.animation = 'k 2s';

    
}


p = document.createElement("p");
function submitContent(event) {
    imgUrl = document.querySelector("#profile-input").value 
    username = document.querySelector("#username-input").value
    firstname = document.querySelector("#firstname-input").value
    lastname = document.querySelector("#lastname-input").value
    bio = document.querySelector("#bio-text").value
    
    if (imgUrl == '' || username == '' || firstname == '' || lastname == '' || bio == '') {
        console.log(imgUrl)
        console.log(username)
        console.log(firstname)
        console.log(lastname)
        console.log(bio)
        console.log("ran")
        event.preventDefault()
        
        p.innerHTML = 'ALL FIELDS MUST NOT BE BLANK';
        p.style.textAlign = 'center';
        p.style.color = 'red';
        document.querySelector("body").append(p)
    }
    
}