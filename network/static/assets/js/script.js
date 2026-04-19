function addlike(postid,likecount){
    // document.body.style.backgroundColor="red";
    const countelem = document.querySelector(`#like-${postid}`);
    const unlikebtn = document.querySelector(`#unlike_btn-${postid}`);
    const likebtn = document.querySelector(`#like_btn-${postid}`);



   fetch(`/like/${postid}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        likecount = result.total_likes;
       
        countelem.innerHTML = likecount;
        if (result.liked){
            likebtn.classList.add("hidden");
            unlikebtn.classList.remove("hidden");
        }
      
    
    });

}

function unlike(postid,likecount){
    // document.body.style.backgroundColor="red";
    const countelem = document.querySelector(`#like-${postid}`);
    const unlikebtn = document.querySelector(`#unlike_btn-${postid}`);
    const likebtn = document.querySelector(`#like_btn-${postid}`);



   fetch(`/unlike/${postid}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        likecount = result.total_likes;

        countelem.innerHTML = likecount;
        if (result.liked === false){
            likebtn.classList.remove("hidden");
            unlikebtn.classList.add("hidden");
        }
        else{
            console.log("if not working")
        }
      
    
    });

}



