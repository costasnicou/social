document.addEventListener('DOMContentLoaded', function () {
    const editBtns = document.querySelectorAll('.edit_btn');

    editBtns.forEach(editBtn => {
        editBtn.onclick = function () {
            const id = editBtn.getAttribute("id");
            const editForms = document.querySelectorAll('.edit-post-form');
            const editForm = document.querySelector(`#edit-form-${id}`);
            const allPosts = document.querySelectorAll('.post');
            const post = document.querySelector(`#post-${id}`);
           
            // editForms.classList.add("hidden");       
            editForms.forEach(hideeditForm=>{
        
                hideeditForm.classList.add('hidden');
                    

            });

            allPosts.forEach(hidepost=>{
        
                hidepost.classList.remove('hidden');
                    

            });
            
        
            post.classList.add('hidden');
        
            editForm.classList.remove('hidden');
            editForm.querySelector('textarea').focus();

          
          
            
        }
    });

    const editPostForms = document.querySelectorAll('.edit-post-form');
    editPostForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const postId = this.id.split('-').pop(); 
            // const parent = form;
           
            const content = this.querySelector("textarea").value;
            const post = document.querySelector(`#post-${postId}`);
            form.classList.add("hidden");
            post.classList.remove("hidden");
            
            post.firstElementChild.innerText = content;
            const formcontent = new FormData(this);
            formcontent.append(`save-edited-post-${postId}`,"True");
           
            fetch(`/save_edited_post/${postId}`, {
                method: "POST",
                body: formcontent
            })
            .then(response => response.json())
            .then(data => console.log(data))
            .catch(err => console.error(err));
        
        });
    });


    
});
