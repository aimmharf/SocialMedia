document.addEventListener("DOMContentLoaded", function(){
    document.querySelector(".btn-post").style.display = 'none';
    document.querySelector("#js-input-content").addEventListener("keyup", function() {
        console.log("h")
        if (document.querySelector("#js-input-content").value.length > 0) {
            document.querySelector(".btn-post").style.display = 'block'
        } else {
            document.querySelector(".btn-post").style.display = 'none';
        }
    })
    document.querySelectorAll(".comment-container").forEach((container) => {
        container.style.display = 'none';
    })

    document.querySelector(".btn-post").addEventListener("click", post_content)
    document.querySelectorAll(".img-like-button").forEach((button) => {
        getLikeCount(button)
       
        button.addEventListener("click", function(){
        
        like_post(button)
    })})
    document.querySelectorAll(".img-dislike-button").forEach((button) => {
        getdisLikeCount(button)
        button.addEventListener("click", function() {
            
            dislikePost(button)
        })
    })
    document.querySelectorAll("#btn-comment").forEach((button) => {
        
        button.addEventListener("click", () => {
            
            comment(button)
        })
    })
    document.querySelectorAll(".comment-post-container").forEach((container) => {
        loadPostComments(container,0)
    })
    
    document.querySelectorAll(".suggested-btn-followw").forEach((button) => {
        button.addEventListener("click", function(){
            if (button.innerHTML == 'Follow'){
                suggested_followw(button)
            }else{suggested_unfollow(button)}
            
        })
    })
})

const p = document.createElement('p')
async function post_content() {
    // Getting the input content
    const inputContent = document.querySelector("#js-input-content")
    
    // POSTING THE DATA TO THE BACKEND
    let response = await fetch("/post_api", {
        method: 'POST', 
        body: JSON.stringify( {
            'Post': inputContent.value
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
          }

    })
    
    


    // ADD POST MESSAGE SUCCESSFULL
    inputContent.value = ''
    p.innerHTML = 'Posted successfully!'
    p.style.margin = '0'
    document.querySelector(".post-element2-container").append(p)


    // UPDATING THE POSTS ON THE PAGE
    update_posts()
    

}

async function get_content() {
    let response = await fetch("/get_api")
    //let r = await response.json()
    return await response.json()
}

function load_posts() {
    get_content().then((response) => {
        // GETTING THE CONTENT FROM THE BACKEND
        const content = response
        const a = JSON.parse(content)
       
        // CREATING A NEW POST AND ADDING THEM TO THE PAGE
        for (let i=0; i<a.length; i++) {
            const postContainer = document.querySelector(".all-posts-container2").cloneNode(true)
            postContainer.querySelector("#full-name").innerHTML = `${a[i].fields.first_name} ${a[i].fields.last_name}`
            postContainer.querySelector("#username").innerHTML = `@${a[i].fields.username}`
            postContainer.querySelector(".post-text").innerHTML = `${a[i].fields.post}`
            document.querySelector(".all-posts-container1").append(postContainer)


        }
    })
    
}

function update_posts() {
    get_content().then((response) => {
        // GETTING THE LAST POST
        const a = JSON.parse(response)
        const b = a.slice(-1)
        
        // CREATING A NEW POST FOR THE LAST POST
        
        
            
            const postContainer = document.querySelector(".comment-post-container").cloneNode(true)
            postContainer.querySelector("#full-name").innerHTML = `${b[0].fields.first_name} ${b[0].fields.last_name}`
            postContainer.querySelector("#username").innerHTML = `@${b[0].fields.username}`
            postContainer.querySelector(".post-text").innerHTML = `${b[0].fields.post}`
            document.querySelector(".all-posts-container1").prepend(postContainer)
            postContainer.style.borderColor='black';
            window.location.reload()
            
           // TODO: MAKE THE NEW CONTAINER MANUALLY
            

         


           
    })

   
}



async function getCurrentUser() {
    // GETTING THE CURRENT USER FROM THE BACKEND
    const response = await fetch("/current_user")
    const a = await response.json()
    return a
}

async function like_post(button) {

    // GET THE POST DETAILS
    const container = button.parentNode.parentNode.parentNode.parentNode

   // GETTING THE CURRENT USER
   getCurrentUser().then(async function(response) {
    // POSTING THE DATA TO THE BACKEND
    const postResponse = await fetch("/like_post", {
        method: 'post',
        body: JSON.stringify({
            'current_user': response,
            'id': container.querySelector("#post-id").innerHTML          
        }) 
    })
    const a = postResponse
    
    getLikeCount(button)
    changeLikeButtonColor(container, a.status)
    /*
    changeDisLikeButtonColor(button, a.status)
    getdisLikeCount(button)
    */
    revertDislike(button)
   })
   

}

async function getLikeCount(button) {
    const container = button.parentNode.parentNode.parentNode.parentNode
    console.log()
    const postResponse = await fetch(`/like_count/${container.querySelector("#post-id").innerHTML}`)
    let a = await postResponse.json()
    const likeCount = JSON.parse(a)
    button.parentNode.parentNode.querySelector("#like-count").innerHTML = likeCount['count']
    
   

}

function changeLikeButtonColor(button, status) {
   
    if (status == 201) {
        button.querySelector(".img-like-button").style.backgroundImage = "url('static/css/images/icon-like.png')"
    } else {
        button.querySelector(".img-like-button").style.backgroundImage = "url('static/css/images/download.png')"
    }
    
}

async function dislikePost(button) {
    // Get the post details
    const container = button.parentNode.parentNode.parentNode.parentNode

   // Get the user
   getCurrentUser().then(async function(response) {
    // fetching the url
    const postResponse = await fetch("/dislike_post", {
        method: 'post',
        body: JSON.stringify({
            'current_user': response,
            'id': container.querySelector("#post-id").innerHTML
            
        })
        
        
        
    })
    const a = postResponse
    
    getdisLikeCount(button)
    
    
    changeDisLikeButtonColor(container, a.status)
    revertLike(button)
   })
}

async function getdisLikeCount(button) {
    const container = button.parentNode.parentNode.parentNode.parentNode
    const postResponse = await fetch(`/dislike_count/${container.querySelector("#post-id").innerHTML}`)
    let a = await postResponse.json()
    const dislikeCount = JSON.parse(a)
    
    button.parentNode.parentNode.querySelector("#dislike-count").innerHTML = dislikeCount['count']
    
    
    
}

function changeDisLikeButtonColor(button, status) {
    
    if (status == 201) {
        button.querySelector(".img-dislike-button").style.backgroundImage = "url('static/css/images/dislike.png')"
    } else {
        button.querySelector(".img-dislike-button").style.backgroundImage = "url('static/css/images/dislike.jpeg')"
    }
}

function revertDislike(button) {
    const a = button.parentNode.parentNode
    changeDisLikeButtonColor(a, 201)
    getdisLikeCount(button)
}

function revertLike(button) {
    const a = button.parentNode.parentNode
    changeLikeButtonColor(a, 201)
    getLikeCount(button)
}


async function comment(button) {
    const a = button.parentNode.parentNode.parentNode.parentNode.parentNode
    const userInput = document.createElement("input")
    const btnSubmit = document.createElement("button")
    const pUsername = document.createElement("p")
    const btnCancel = document.createElement("button")

    // Get the user 
    const userCurrent = await fetch("/get_user")
    const response = await userCurrent.json()
    console.log(response.user)

    // SET ATTRIBUTES
    userInput.placeholder = 'Add a comment';
    userInput.className = 'comment-input';
    userInput.autofocus = true;
    btnSubmit.type = 'submit'
    btnSubmit.id = 'btn-comment-submit';
    btnCancel.id = 'btn-comment-cancel'


    btnSubmit.innerHTML = 'Comment'
    btnCancel.innerHTML = 'Cancel'
    pUsername.innerHTML = `@${response.user}`

    // STYLING
    a.style.display = 'grid';
    a.style.gridRowGap = '20px';
    a.querySelector(".comment-container").style.display = 'grid'
    button.disabled = true

    

    // ADD TO THE DOM
    a.querySelector(".js-comment-container").style.display = 'grid'
    a.querySelector(".comment-user-names-container").append(pUsername)
    a.querySelector(".comment-input-container").append(userInput)
    a.querySelector(".comment-btn-submit-container").append(btnSubmit)
    a.querySelector(".comment-btn-submit-container").append(btnCancel)
    

    // WAITING FOR USER TO CLICK THE SUBMIT
    a.querySelector("#btn-comment-submit").addEventListener("click", async function(){
        a.querySelector(".js-comment-container").style.display = 'grid'
        a.querySelector(".comment-user-names-container").removeChild(pUsername)
        a.querySelector(".comment-input-container").removeChild(userInput)
        a.querySelector(".comment-btn-submit-container").removeChild(btnSubmit)
        a.querySelector(".comment-btn-submit-container").removeChild(btnCancel)
        a.querySelector(".js-comment-container").style.display = 'none'
        button.disabled = false
        const postResponse = await fetch(`/comment/${a.querySelector("#post-id").innerHTML}`, {
            method: 'post', 
            body: JSON.stringify({
                'username': response.user,
                'id': a.querySelector("#post-id").innerHTML,
                'comment': userInput.value
            })
        })
        console.log(a)
        loadPostComments(a,1)
    })
    a.querySelector("#btn-comment-cancel").addEventListener("click", function() {
        console.log("hi")
        a.querySelector(".comment-user-names-container").removeChild(pUsername)
        a.querySelector(".comment-input-container").removeChild(userInput)
        a.querySelector(".comment-btn-submit-container").removeChild(btnSubmit)
        a.querySelector(".comment-btn-submit-container").removeChild(btnCancel)
        a.querySelector(".js-comment-container").style.display = 'none'
        button.disabled = false
    })
    
}


async function loadPostComments(container, num) {
    if (num == 0) {
        const getResponse = await fetch(`/comment/${container.querySelector("#post-id").innerHTML}`)
        const response = await getResponse.json()
        for (let i=0; i<response.length; i++) {
            const pUsername = document.createElement("p")
            const pComment = document.createElement("p")
            const commentDiv = document.createElement("div")
            commentDiv.className = 'post-comment'

            pUsername.innerHTML = response[i].user;
            pComment.innerHTML = response[i].comment;
            container.querySelector("#comment-number").innerHTML = response.length
        
            commentDiv.append(pUsername);
            commentDiv.append(pComment);

            container.querySelector(".all-comments").append(commentDiv)


    }
    
    } else {
        const getResponse = await fetch(`/comment/${container.querySelector("#post-id").innerHTML}`)
        const response = await getResponse.json()
        
        const pUsername = document.createElement("p")
        const pComment = document.createElement("p")
        const commentDiv = document.createElement("div")
        commentDiv.className = 'post-comment'

        pUsername.innerHTML = response[0].user;
        pComment.innerHTML = response[0].comment;
        container.querySelector("#comment-number").innerHTML = response.length
        
        commentDiv.append(pUsername);
        commentDiv.append(pComment);

        container.querySelector(".all-comments").append(commentDiv)
    }

}


async function suggested_followw(button) {
    const userf = button.parentNode.parentNode.querySelector("#suggested-username").innerHTML
    const current_u = await getCurrentUser()
    
    
    
    get_url = await fetch("/follow_user", {
        method:'post',
        body: JSON.stringify({
            'current_user': current_u,
            'user_being_followed': userf.slice(1),
            'follow_id':'1'
        })
    })
    response = await get_url
    console.log(response)
    button.style.backgroundColor = 'green';
    button.innerHTML = 'Following'
    
}


async function suggested_unfollow(button) {
    const userf = button.parentNode.parentNode.querySelector("#suggested-username").innerHTML
    const current_u = await getCurrentUser()
    
    
    
    get_url = await fetch("/follow_user", {
        method:'post',
        body: JSON.stringify({
            'current_user': current_u,
            'user_being_followed': userf.slice(1),
            'follow_id':'2'
        })
    })
    response = await get_url
    console.log(response)
    button.style.backgroundColor = '#0080FF';
    button.innerHTML = 'Follow';
}