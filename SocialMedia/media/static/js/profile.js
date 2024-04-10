
document.addEventListener("DOMContentLoaded", function(){
    
    document.querySelector(".btn-follow").addEventListener("click", function(){follow()})
})


function follow() {
    if (document.querySelector(".btn-follow").innerHTML == 'Follow') {
        follow_user("1")
    } else {
        follow_user("2")
    }
   
    
    
}


async function getCurrentUser() {
    const response = await fetch("/current_user")
    const a = await response.json()
    return a
    
}

async function follow_user(id) {
    getCurrentUser().then(async function(response) {
        let follow_id = null
        if (id == "1") {
            follow_id = "1"
        } else{follow_id = "2"}
       
        let a = window.location.pathname
        let c =a.toString(a)
        console.log(c.slice(9))
        const post_Response = await fetch("/follow_user", {
            method: 'post',
            body: JSON.stringify({
                "current_user": response,
                "user_being_followed": c.slice(9),
                "follow_id": follow_id
            })
        })
        const result = await post_Response.json()
        console.log(result)
    }).then(() => {
        if (id=='1') {
            document.querySelector(".btn-follow").innerHTML = 'Unfollow'
        document.querySelector(".btn-follow").style.backgroundColor = '#FF3333'
    } else {document.querySelector(".btn-follow").innerHTML = 'Follow'
    document.querySelector(".btn-follow").style.backgroundColor = '#0066CC'}
        

    })
    
}



async function unFollowUser() {
    getCurrentUser().then(async function(response) {
        let a = window.location.pathname
        let c =a.toString(a)
        console.log(c.slice(9))
        const post_Response = await fetch("/remove_follower", {
            method: 'post',
            body: JSON.stringify({
                "current_user": response,
                "user_being_followed": c.slice(9),
                
            })
        })
        const result = await post_Response.json()
        console.log(result)
    }).then(() => {
        
    })


    
}