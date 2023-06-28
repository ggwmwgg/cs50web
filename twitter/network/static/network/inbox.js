document.addEventListener("DOMContentLoaded", function(event) {

    try {
        registrationFormListener();
    } catch (error) {
        //console.log("Registration form not found (probably logged in)");
    }
    try {
        loginFormListener();
    } catch (error) {
        //console.log("Login form not found (probably logged in)");
    }
    try {
        sidebarListener();
    } catch (error) {
        //console.log("Sidebar not found (probably not logged in)");
    }
    try {
        postListener();
    } catch (error) {
        //console.log("Post form not found (probably not logged in)");
    }
    try {
        profileButtonsListener();
    } catch (error) {
        //console.log("Profile buttons not found (probably not logged in)");
    }
    try {
        locationListener();
    } catch (error) {
        //console.log("Location not found (probably not logged in)");
    }
    try {
        popStateListener();
    } catch (error) {
        //console.log("Popstate not found (probably not logged in)");
    }

    // window.addEventListener('popstate', () => {
    //     window.location.reload();
    // });
    window.onload = function onLoad() {

    };

    //errorLoader();
    //locationListener();
    //postsLoader(1, "all");
    //addComment(44, "testir");

});
const standartImageUrl = "http://127.0.0.1:8000/static/network/user.png";
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Sending form for registration
function registrationFormListener() {
    const registrationButton = document.getElementById('registration-button');

    const usernameReg = document.getElementById('username-reg');
    const emailReg = document.getElementById('email-reg');
    const passwordReg = document.getElementById('password-reg');
    const confirmationReg = document.getElementById('confirmation-reg');

    // name_reg, username_reg, email_reg, bio_reg, url_reg, password_reg, confirmation_reg
    registrationButton.addEventListener('click', function (event) {
        event.preventDefault();

        // Validating passwords match
        if (registrationFormChecker() === true) {
            registrationFormSender();
        } else {
            console.log("Error");
        }
    });
    passwordReg.addEventListener("input", function() {
        passwordReg.classList.remove("is-invalid");
        passwordReg.parentElement.classList.remove("is-invalid");
        confirmationReg.classList.remove("is-invalid");
        confirmationReg.parentElement.classList.remove("is-invalid");

    });
    confirmationReg.addEventListener("input", function() {
        confirmationReg.classList.remove("is-invalid");
        confirmationReg.parentElement.classList.remove("is-invalid");
        passwordReg.classList.remove("is-invalid");
        passwordReg.parentElement.classList.remove("is-invalid");
    });
    usernameReg.addEventListener("input", function() {
        usernameReg.classList.remove("is-invalid");
        usernameReg.parentElement.classList.remove("is-invalid");
    });
    emailReg.addEventListener("input", function() {
        emailReg.classList.remove("is-invalid");
        emailReg.parentElement.classList.remove("is-invalid");
    });
}

// Checking if the form is valid
function registrationFormChecker() {
    let checked = true;

    const usernameErr = document.getElementById('username-error');
    const emailErr = document.getElementById('email-error');
    const passwordErr = document.getElementById('password-error');
    const usernameReg = document.getElementById('username-reg');
    const emailReg = document.getElementById('email-reg');
    const passwordReg = document.getElementById('password-reg');
    const confirmationReg = document.getElementById('confirmation-reg');

    // Validating passwords match
    if (passwordReg.value !== confirmationReg.value) {

        passwordReg.classList.add("is-invalid");
        passwordReg.parentElement.classList.add("is-invalid");
        confirmationReg.classList.add("form-control", "is-invalid");
        confirmationReg.parentElement.classList.add("is-invalid");
        passwordErr.innerHTML = "Passwords do not match."
        checked = false;
    }
    // Validating username (min 5 max 25)
    if (usernameReg.value.length < 5 || usernameReg.value.length > 25) {
        usernameReg.classList.add("is-invalid");
        usernameReg.parentElement.classList.add("is-invalid");
        usernameErr.innerHTML = "Username must be between 5 and 25 characters."
        checked = false;
    }
    // Validating email (regex should include @ and .)
    if (!emailReg.value.includes('@') || !emailReg.value.includes('.')) {
        emailReg.classList.add("is-invalid");
        emailReg.parentElement.classList.add("is-invalid");
        emailErr.innerHTML = "Email must be a valid email address."
        checked = false;
    }
    if (passwordReg.value.length < 5 || !passwordReg.value.length > 16) {

        passwordReg.classList.add("is-invalid");
        passwordReg.parentElement.classList.add("is-invalid");
        confirmationReg.classList.add("form-control", "is-invalid");
        confirmationReg.parentElement.classList.add("is-invalid");
        passwordErr.innerHTML = "Password must be at least 5 characters and no more than 16 characters."
        checked = false;
    }
    return checked;
}

// Registration form sender
function registrationFormSender() {

    const nameReg = document.getElementById('name-reg');
    const usernameReg = document.getElementById('username-reg');
    const emailReg = document.getElementById('email-reg');
    const bioReg = document.getElementById('bio-reg');
    const urlReg = document.getElementById('url-reg');
    const passwordReg = document.getElementById('password-reg');
    const confirmationReg = document.getElementById('confirmation-reg');
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const usernameErr = document.getElementById('username-error');
    const emailErr = document.getElementById('email-error');
    const passwordErr = document.getElementById('password-error');
    const registrationButton = document.getElementById('registration-button');
    const closeRegistrationButton = document.getElementById('close-reg');
    const statusReg = document.getElementById('status-reg');
    const statusRegText = document.getElementById('succ-reg');
    const statusRegTime = document.getElementById('redirect-time');
    fetch('/register', {
        method: 'POST',
        body: JSON.stringify({
            name: nameReg.value,
            username: usernameReg.value,
            email: emailReg.value,
            bio: bioReg.value,
            url: urlReg.value,
            password: passwordReg.value,
            confirmation: confirmationReg.value
        }),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,

        }
    })
    .then(response => {
        if (response.ok) {
            //location.reload();
            nameReg.disabled = true;
            nameReg.classList.add("is-valid");
            usernameReg.disabled = true;
            usernameReg.classList.add("is-valid");
            emailReg.disabled = true;
            emailReg.classList.add("is-valid");
            bioReg.disabled = true;
            bioReg.classList.add("is-valid");
            urlReg.disabled = true;
            urlReg.classList.add("is-valid");
            passwordReg.disabled = true;
            passwordReg.classList.add("is-valid");
            confirmationReg.disabled = true;
            confirmationReg.classList.add("is-valid");
            registrationButton.classList.add("disabled");
            closeRegistrationButton.classList.add("disabled");
            statusReg.classList.remove("d-none");
            statusRegText.classList.remove("d-none");

            let count = 3;

            function countdown() {
                if (count > 0) {
                    console.log(`You will be redirected in ${count}...`);
                    statusRegTime.textContent = count.toString();
                    count--;
                    setTimeout(countdown, 1000);
                } else {
                    location.reload();
                }
            }

            countdown();

        } else if (response.status === 400) {
            response.json().then(data => {
                if (data.error === "passwords_mismatch") {
                    passwordReg.classList.add("is-invalid");
                    passwordReg.parentElement.classList.add("is-invalid");
                    confirmationReg.classList.add("is-invalid");
                    passwordErr.innerHTML = "Passwords do not match."
                } else if (data.error === "username_taken") {
                    usernameReg.classList.add("is-invalid");
                    usernameReg.parentElement.classList.add("is-invalid");
                    usernameErr.innerHTML = "Username is already taken."
                } else if (data.error === "email_taken") {
                    emailReg.classList.add("is-invalid");
                    emailReg.parentElement.classList.add("is-invalid");
                    emailErr.innerHTML = "Email is already taken."
                } else if (data.error === "password_length") {
                    passwordReg.classList.add("is-invalid");
                    passwordReg.parentElement.classList.add("is-invalid");
                    confirmationReg.classList.add("is-invalid");
                    passwordErr.innerHTML = "Password must be at least 5 characters and no more than 16 characters."
                } else if (data.error === "username_length") {
                    usernameReg.classList.add("is-invalid");
                    usernameReg.parentElement.classList.add("is-invalid");
                    usernameErr.innerHTML = "Username must be between 5 and 10 characters."
                } else if (data.error === "email_invalid") {
                    emailReg.classList.add("is-invalid");
                    emailReg.parentElement.classList.add("is-invalid");
                    emailErr.innerHTML = "Email must be a valid email address."
                }
                return false;
            });
        }
    });
}
// Sending form for login
function loginFormListener() {
    const loginButton = document.getElementById('login-button');
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    const username = document.getElementById('username-login');
    const password = document.getElementById('password-login');
    const loginErr = document.getElementById('login-error-msg');
    loginButton.addEventListener('click', function (event) {
        event.preventDefault();
        const loginForm = document.getElementById('login-form');
        fetch('/login', {
            method: 'POST',
            body: JSON.stringify({
                username: username.value,
                password: password.value
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        })
        .then(response => {
            if (response.ok) {
                location.reload();
            } else if (response.status === 400) {
                response.json().then(data => {
                    username.classList.add("is-invalid");
                    password.classList.add("is-invalid");
                    loginErr.classList.remove("d-none");
                });
            }
        });
    });

    username.addEventListener("input", function() {
        username.classList.remove("is-invalid");
        loginErr.classList.add("d-none");
    });

    password.addEventListener("input", function() {
        password.classList.remove("is-invalid");
        loginErr.classList.add("d-none");
    });

}

function removeActive() {
    const profile = document.getElementById('profile-side');
    const allPosts = document.getElementById('all-posts-side');
    const following = document.getElementById('following-side');
    const followers = document.getElementById('followers-side');
    const saved = document.getElementById('saved-side');
    const logout = document.getElementById('logout-side');
    profile.classList.remove("active");
    allPosts.classList.remove("active");
    following.classList.remove("active");
    followers.classList.remove("active");
    saved.classList.remove("active");
    logout.classList.remove("active");
    viewsDisable();

}

function sidebarListener(event) {
    const profile = document.getElementById('profile-side');
    const allPosts = document.getElementById('all-posts-side');
    const following = document.getElementById('following-side');
    const followers = document.getElementById('followers-side');
    const saved = document.getElementById('saved-side');
    const logout = document.getElementById('logout-side');
    const profileView = document.querySelector('#profile_view');
    const allPostsView = document.querySelector('#all_posts_view');
    const followingView = document.querySelector('#following_posts_view');
    const followersView = document.querySelector('#followers_view');
    const savedView = document.querySelector('#saved_view');
    const pressedButton = this.id;

    if (pressedButton === "profile-side") {
        removeActive();
        viewsDisable();
        profile.classList.add("active");
        profileView.classList.remove("d-none");
        // Добавить загрузку профиля любого пользователя
        const allPostsView = document.querySelector('#all_posts_view');
        const user_id = parseInt(allPostsView.getAttribute("data-user-id"));
        profileLoader(user_id);
    } else if (pressedButton === "all-posts-side") {
        removeActive();
        viewsDisable();
        allPosts.classList.add("active");
        allPostsView.classList.remove("d-none");
        postsLoader(1, "all");
    } else if (pressedButton === "following-side") {
        removeActive();
        viewsDisable();
        following.classList.add("active");
        followingView.classList.remove("d-none");
        postsLoader(1, "following");
    } else if (pressedButton === "followers-side") {
        removeActive();
        viewsDisable();
        followers.classList.add("active");
        followersView.classList.remove("d-none");
        // Get user id
        const user_id = parseInt(followersView.getAttribute("data-user-id"));
        followerFollowingLoader("followers-m", user_id);
    } else if (pressedButton === "saved-side") {
        removeActive();
        viewsDisable();
        saved.classList.add("active");
        savedView.classList.remove("d-none");
        postsLoader(1, "saved");
    } else if (pressedButton === "logout-side") {
        //console.log("Logging out...")
    }
    profile.addEventListener("click", sidebarListener);
    allPosts.addEventListener("click", sidebarListener);
    following.addEventListener("click", sidebarListener);
    followers.addEventListener("click", sidebarListener);
    saved.addEventListener("click", sidebarListener);
    logout.addEventListener("click", sidebarListener);
}

function postSender(msg, modalM) {
    const text = msg.value;
    fetch('http://127.0.0.1:8000/post/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        text: text
      })
    })
    .then(response => {
        const postText = document.getElementById('post_text');
        const postTextM = document.getElementById('post_text_m');
        const postSendButton = document.getElementById('post_button_m');
        const postButton = document.getElementById('post_button');
        const postCloseButton = document.getElementById('post_close_button_m');
        const postSuccessDiv = document.getElementById('post_success_msg_m');
        const postSuccessDivMain = document.getElementById('post_success_msg');
        const modal = bootstrap.Modal.getInstance(document.getElementById('makePost'));
        if (response.status === 201) {
            if (modalM === "modal") {

                postTextM.disabled = true;
                postSendButton.disabled = true;
                postCloseButton.disabled = true;
                postSuccessDiv.classList.remove("d-none");
                setTimeout(function() {
                    modal.hide();
                    //console.log("Post created");
                    postTextM.disabled = false;
                    postTextM.value = "";
                    postSendButton.disabled = false;
                    postCloseButton.disabled = false;
                    postSuccessDiv.classList.add("d-none");
                    postsLoader(1, "all");
                }, 3000);

                postsLoader(1, "all");
            } else if (modalM === "normal-all") {
                postText.disabled = true;
                postButton.disabled = true;
                postSuccessDivMain.classList.remove("d-none");
                setTimeout(function() {
                    //console.log("Post created");
                    postText.disabled = false;
                    postButton.disabled = false;
                    postSuccessDivMain.classList.add("d-none");
                    postText.value = "";
                    postsLoader(1, "all");
                }, 3000);

            }
        } else if (response.status === 400) {
            response.json().then(data => {
                console.log(data.error);
                location.reload();
            });
        }
    });
}


function postUpdater(msg, id) {

    fetch('http://127.0.0.1:8000/post/create', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: msg,
        id: id
      })
    })
    .then(response => {
        if (response.status === 201) {
            //location.reload();
        } else if (response.status === 400) {
            response.json().then(data => {
                console.log(data.error);
            });
        }
    });
}

function postListener() {
    const postButtonM = document.getElementById('post_button_m');
    const postButton = document.getElementById('post_button');
    const postTextM = document.getElementById('post_text_m');
    const postText = document.getElementById('post_text');
    const progressArea = document.getElementById('myProgress');
    const progressBar = document.getElementById("myBar");
    const progressLabel = document.getElementById("myLabel");
    const progressAreaM = document.getElementById('myProgressM');
    const progressBarM = document.getElementById("myBarM");
    const progressLabelM = document.getElementById("myLabelM");
    postTextM.addEventListener("input", function() {
        if (postTextM.value.length > 0) {
            postButtonM.classList.remove("disabled");
        } else {
            postButtonM.classList.add("disabled");
        }
        postTextM.style.height = "";
        postTextM.style.height = (postTextM.scrollHeight + 2) + "px";
        progressAreaM.classList.remove("d-none");
        const progress = postTextM.value.length / 280 * 100;
        //progressLabel.innerHTML = `<b>${Math.round(progress)}%</b>`;
        progressLabelM.innerHTML = `<b>${postTextM.value.length}/280</b>`;
        if (progress === 100) {
            progressBarM.style.width = `100%`;
            progressBarM.style.backgroundImage = "linear-gradient(-45deg, #e42c39 0%, #dc3540 25%, #ed4d58 50%, #dc3540 75%, #e42c39 100%, #e42c39 100.1%)";
            progressBarM.style.backgroundColor = "#f26c75";
        } else {
            progressBarM.style.width = `${progress}%`;
            progressBarM.style.backgroundImage = "linear-gradient(-45deg, #0d6efd 0%, #00acff 25%, #0799fe 50%, #00acff 75%, #0d6efd 100%, #0d6efd 100.1%)";
            progressBarM.style.backgroundColor = "#0d6efd";
        }
    });
    postText.addEventListener("input", function() {
        if (postText.value.length > 0) {
            postButton.classList.remove("disabled");
        } else {
            postButton.classList.add("disabled");
        }
        postText.style.height = "";
        postText.style.height = (postText.scrollHeight + 2) + "px";
        progressArea.classList.remove("d-none");
        const progress = postText.value.length / 280 * 100;
        //progressLabel.innerHTML = `<b>${Math.round(progress)}%</b>`;
        progressLabel.innerHTML = `<b>${postText.value.length}/280</b>`;
        if (progress === 100) {
            progressBar.style.width = `100%`;
            progressBar.style.backgroundImage = "linear-gradient(-45deg, #e42c39 0%, #dc3540 25%, #ed4d58 50%, #dc3540 75%, #e42c39 100%, #e42c39 100.1%)";
            progressBar.style.backgroundColor = "#f26c75";
        } else {
            progressBar.style.width = `${progress}%`;
            progressBar.style.backgroundImage = "linear-gradient(-45deg, #0d6efd 0%, #00acff 25%, #0799fe 50%, #00acff 75%, #0d6efd 100%, #0d6efd 100.1%)";
            progressBar.style.backgroundColor = "#0d6efd";
        }



    });
    postButtonM.addEventListener('click', function (event) {
        event.preventDefault();

        postSender(postTextM, "modal");
        postTextM.value = "";
        progressAreaM.classList.add("d-none");
    });
    postButton.addEventListener('click', function (event) {
        event.preventDefault();
        postSender(postText, "normal-all");
        postText.value = "";
        progressArea.classList.add("d-none");


    });

}

function postsLoader(page_pl, type_pl, user_pl = undefined) {
    //if (type_pl === "all") {
    viewsDisable();
    let postsF;
    let allPostsView;
    let fetchUrl;
    if (type_pl === "all") {
        postsF = document.getElementById('all_posts');
        allPostsView = document.getElementById('all_posts_view');
        fetchUrl = `http://127.0.0.1:8000/post?page=${page_pl}&type=${type_pl}`;
    } else if (type_pl === "user") {
        postsF = document.getElementById('all_posts_profile');
        allPostsView = document.getElementById('profile_view');
        fetchUrl = `http://127.0.0.1:8000/post?page=${page_pl}&type=${type_pl}&user=${user_pl}`;
    } else if (type_pl === "following") {
        postsF = document.getElementById('following_posts');
        allPostsView = document.getElementById('following_posts_view');
        fetchUrl = `http://127.0.0.1:8000/post?page=${page_pl}&type=${type_pl}`;
    } else if (type_pl === "saved") {
        postsF = document.getElementById('all_posts_saved');
        allPostsView = document.getElementById('saved_view');
        fetchUrl = `http://127.0.0.1:8000/post?page=${page_pl}&type=${type_pl}`;
    }

    allPostsView.classList.remove("d-none");
    //console.log(postsF.scrollHeight);

    //postsF.innerHTML = "";


    fetch(fetchUrl)
    .then(response => response.json())
    .then(posts => {
        const highestDiv = document.createElement('div');
        highestDiv.id = "highest_div";
        const maxPosts = posts.results.length;
        if(posts.results.length === 0) {
            const postDiv = document.createElement('div');
            postDiv.className = "row";
            postDiv.innerHTML = `
                <div class="col">
                    <div class="card border-dark mb-1">
                        <div class="card-body">
                            <div class="row">
                                <div class="col-12">
                                    <div class="row">
                                        <div class="pb-3 pt-3">
                                            <div class="text-center fs-6 fw-semibold text-primary"><p>Nothing to see here yet.</p><p>No posts yet created.</p></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            postsF.appendChild(postDiv);
        } else {

            posts.results.forEach(post => {
                const postDiv = document.createElement('div');
                let imgUrl = "";
                let imageInit = "";
                try {
                    imageInit = document.getElementById("image-profile-init");
                    imgUrl = imageInit.getAttribute("src");
                } catch (error) {
                    //console.log("No image");
                }
                postDiv.className = "card border-dark mb-1";
                postDiv.innerHTML = `
                    <div class="card-body cardbd" data-post-id="${post.id}" data-user-id="${post.user_id}">
                        <div class="row">
                            <div class="col-1">
                                <img src="${post.image}" alt="" width="48" height="48" class="img-fluid rounded-circle user_image" style="min-width: 36px;">
                            </div>
                            <div class="col-11">
                                <div class="row">
                                    <div class="col-10 text-left pt-1">
                                        <a class="fw-bold text-decoration-none text-dark user-profile-link" href="/profile/${post.user_id}/1">${post.user}</a> <b class="fw-lighter"><a href="/profile/${post.user_id}/1" class="text-decoration-none text-dark username-profile-link">@${post.username}</a> · ${post.timestamp}</b>
                                    </div>
                                    <div class="col-2 mb-3" style="padding-left: 28px;">
                                        <div class="d-flex justify-content-end">
                                            <button class="btn btn-outline-secondary btn-sm rounded-pill edit-button ms-1 d-none" type="button">Edit</button>
                                            <button class="btn btn-danger btn-sm rounded-pill cancel-button ms-1 d-none" type="button">Cancel</button>
                                            <button class="btn btn-primary btn-sm rounded-pill save-button ms-1 d-none" type="button">Save</button>
                                        </div> 
                                    </div>
                                    <hr>
                                </div>
                                <div class="row post-area">
                                    <div class="pb-3 post-body-area">${post.body.replace(/\n/g, '<br>')}</div>
                                    <div class="pb-3 post-edit-area d-none">
                                        <label for="post-prefill" class="form-label"></label>
                                        <textarea class="form-control post-prefill-area">${post.body}</textarea>
                                    </div>
                                    <hr>
                                </div>
                                <div class="row mx-auto panel-view">
                                    <div class="col-4">
                                        <span class="icon-container">
                                            <i class="fa-regular fa-comment post_comments" data-toggle="tooltip" data-placement="top" title="Comments"></i>
                                            <span class="comments-count" id="comments_count">${post.comments_count}</span>
                                        </span>
                                    </div>
                                    <div class="col-4">
                                        <span class="icon-container">
                                            <i class="fa-regular fa-heart post_not_liked" data-toggle="tooltip" data-placement="top" title="Like"></i>
                                            <i class="fa-solid fa-heart post_liked d-none" data-toggle="tooltip" data-placement="top" title="Unlike" style="color: #de1717;"></i>
                                            <span class="likes-count" id="likes_count">${post.likes}</span>
                                        </span>
                                    </div>
                                    <div class="col-4">
                                        <span class="icon-container">
                                            <i class="fa-regular fa-bookmark fa-bookmark1 post_not_bookmarked" data-toggle="tooltip" data-placement="top" title="Bookmark"></i>
                                            <i class="fa-solid fa-bookmark fa-bookmark1 post_bookmarked d-none" data-toggle="tooltip" data-placement="top" title="Remove Bookmark"></i>
                                        </span>
                                    </div>
                                </div>
                                <div class="row mx-auto comm-panel-view d-none">
                                    <div class="col-4">
                                        <button type="button" class="btn btn-outline-danger rounded-pill btn-sm mb-1 comm-close">Close</button>
                                    </div>
                                    <div class="col-4">
                                        <span class="icon-container">
                                            <i class="fa-regular fa-heart post_not_liked_comm" data-toggle="tooltip" data-placement="top" title="Like"></i>
                                            <i class="fa-solid fa-heart post_liked_comm d-none" data-toggle="tooltip" data-placement="top" title="Unlike" style="color: #de1717;"></i>
                                            <span class="likes-count-comm" id="likes_count_m">${post.likes}</span>
                                        </span>
                                    </div>
                                    <div class="col-4">
                                        <span class="icon-container">
                                            <i class="fa-regular fa-bookmark fa-bookmark1 post_not_bookmarked_comm" data-toggle="tooltip" data-placement="top" title="Bookmark"></i>
                                            <i class="fa-solid fa-bookmark fa-bookmark1 post_bookmarked_comm d-none" data-toggle="tooltip" data-placement="top" title="Remove Bookmark"></i>
                                        </span>
                                    </div>
                                    
                                </div>
                            </div>
                        </div>
                        <div class="pt-3 comment-block d-none">
                            <div class="row">
                                <div class="col-12">
                                    <div class="list-group scroll-comments px-1 comment-inner border-top" style="height: 240px; overflow-y: auto">
    
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <div class="d-flex justify-content-between align-items-center mb-2 row">
                                <div class="col-1">
                                    <img src="${imgUrl}" alt="" width="27" height="27" class="img-fluid rounded-circle" style="min-width: 27px;">
                                </div>
                                <div class="col-11">
                                    <div class="input-group mb-1">
                                        <input type="text" class="form-control comm-input" placeholder="Put your comment here..." aria-label="Put your comment here..." aria-describedby="button-comment">
                                        <button class="btn btn-outline-primary comm-send" type="button" id="button-comment" disabled>Send</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                const post_liked = postDiv.querySelector('.post_liked');
                const postLikedComm = postDiv.querySelector('.post_liked_comm');
                const post_not_liked = postDiv.querySelector('.post_not_liked');
                const postNotLikedComm = postDiv.querySelector('.post_not_liked_comm');
                const saved = postDiv.querySelector('.post_bookmarked');
                const savedComm = postDiv.querySelector('.post_bookmarked_comm');
                const notSaved = postDiv.querySelector('.post_not_bookmarked');
                const notSavedComm = postDiv.querySelector('.post_not_bookmarked_comm');
                const image = postDiv.querySelector('.user_image');
                const editButton = postDiv.querySelector('.edit-button');
                const currentUserId = parseInt(postsF.getAttribute('data-user-id'));
                const postUserId = post.user_id;

                // Adding comment to post
                const commentInner = postDiv.querySelector('.comment-inner');
                commentInner.innerHTML = "";

                post.comments.forEach(comment => {
                    let url = comment.users_data[0].url;
                    if (comment.users_data[0].url === "") {
                        url = standartImageUrl;
                    }
                    const commentDiv = document.createElement('div');
                    commentDiv.className = "list-group-item list-group-item-action d-flex gap-3";
                    commentDiv.setAttribute("data-user-id", `${comment.users_data[0].user_id}`);
                    commentDiv.innerHTML = `
                        <img src="${url}" alt="twbs" width="28" height="28" class="rounded-circle flex-shrink-0 mt-2">
                        <div class="d-flex gap-2 w-100 justify-content-between">
                            <div>
                                <a class="mb-0" href="#"><a class="fw-semibold text-decoration-none text-dark name-comm" href="/profile/${comment.users_data[0].user_id}/1" style="font-size: 15px;">${comment.users_data[0].name}</a> <a class="fw-light text-decoration-none text-dark username-comm" href="/profile/${comment.users_data[0].user_id}/1" style="font-size: 15px;">@${comment.users_data[0].username}</a></a>
                                <p class="mb-0 opacity-75" style="font-size: 14px;">${comment.body}</p>
                            </div>
                            <small class="opacity-50 text-nowrap" style="font-size: 14px;">${comment.timestamp}</small>
                        </div>
                    `;

                    const ProfileLink = commentDiv.querySelector('.name-comm');

                    ProfileLink.addEventListener('click', () => {
                        profileLoader(comment.users_data[0].user_id);
                    });
                    commentInner.appendChild(commentDiv);
                });

                if (currentUserId === postUserId) {
                    editButton.classList.remove("d-none");
                    // Add event listener to edit button
                    editButton.addEventListener('click', () => {
                        const editArea = postDiv.querySelector('.post-edit-area');
                        const postBodyArea = postDiv.querySelector('.post-body-area');
                        const saveButton = postDiv.querySelector('.save-button');
                        const cancelButton = postDiv.querySelector('.cancel-button');
                        const postPrefillArea = postDiv.querySelector('.post-prefill-area');

                        editButton.classList.add("d-none");
                        saveButton.classList.remove("d-none");
                        cancelButton.classList.remove("d-none");
                        editArea.classList.remove("d-none");
                        postBodyArea.classList.add("d-none");
                        postPrefillArea.style.height = "auto";
                        postPrefillArea.value = post.body;
                        postPrefillArea.style.height = (postPrefillArea.scrollHeight + 2) + "px";
                        postPrefillArea.selectionStart = postPrefillArea.selectionEnd = postPrefillArea.value.length;
                        postPrefillArea.focus();

                        cancelButton.addEventListener('click', () => {
                            saveButton.classList.add("d-none");
                            cancelButton.classList.add("d-none");
                            editButton.classList.remove("d-none");
                            postBodyArea.classList.remove("d-none");
                            editArea.classList.add("d-none");
                        });
                        postPrefillArea.addEventListener('input', () => {
                            if (postPrefillArea.value !== post.body) {
                                saveButton.classList.remove("disabled");
                            } else {
                                saveButton.classList.add("disabled");
                            }
                            postPrefillArea.style.height = "";
                            postPrefillArea.style.height = (postPrefillArea.scrollHeight + 2) + "px";
                        });

                        saveButton.addEventListener('click', () => {
                            if (postPrefillArea.value === post.body) {
                                saveButton.classList.add("disabled");
                            } else {
                                postBodyArea.innerHTML = ``;
                                postBodyArea.innerHTML = postPrefillArea.value.replace(/\n/g, '<br>');
                                postUpdater(postPrefillArea.value, post.id);
                                saveButton.classList.add("d-none");
                                cancelButton.classList.add("d-none");
                                editButton.classList.remove("d-none");
                                postBodyArea.classList.remove("d-none");
                                editArea.classList.add("d-none");
                            }
                        });
                    });
                } else {
                    editButton.classList.add("d-none");
                }

                if (post.is_liked) {
                    post_liked.classList.remove("d-none");
                    postLikedComm.classList.remove("d-none");
                    post_not_liked.classList.add("d-none");
                    postNotLikedComm.classList.add("d-none");
                } else {
                    post_liked.classList.add("d-none");
                    postLikedComm.classList.add("d-none");
                    post_not_liked.classList.remove("d-none");
                    postNotLikedComm.classList.remove("d-none");
                }
                if (post.is_saved) {
                    saved.classList.remove("d-none");
                    savedComm.classList.remove("d-none");
                    notSaved.classList.add("d-none");
                    notSavedComm.classList.add("d-none");
                } else {
                    saved.classList.add("d-none");
                    savedComm.classList.add("d-none");
                    notSaved.classList.remove("d-none");
                    notSavedComm.classList.remove("d-none");
                }

                if (post.image === "") {
                    image.src = standartImageUrl;
                }

                const likeButton = postDiv.querySelector('.post_not_liked');
                const commLikeButton = postDiv.querySelector('.post_not_liked_comm');
                const unlikeButton = postDiv.querySelector('.post_liked');
                const commUnlikeButton = postDiv.querySelector('.post_liked_comm');
                const saveButton = postDiv.querySelector('.post_not_bookmarked');
                const commSaveButton = postDiv.querySelector('.post_not_bookmarked_comm');
                const unsaveButton = postDiv.querySelector('.post_bookmarked');
                const commUnsaveButton = postDiv.querySelector('.post_bookmarked_comm');
                const commentButton = postDiv.querySelector('.post_comments');
                const likesCount = postDiv.querySelector('.likes-count');
                const likesCountComm = postDiv.querySelector('.likes-count-comm');
                const commentsCount = postDiv.querySelector('.comments-count');
                const userProfileLink = postDiv.querySelector('.user-profile-link');
                const usernameProfileLink = postDiv.querySelector('.username-profile-link');
                if (!isNaN(currentUserId)) {
                    likeButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("like", "add", post.id);

                        likeButton.classList.add("d-none");
                        unlikeButton.classList.remove("d-none");
                        commLikeButton.classList.add("d-none");
                        commUnlikeButton.classList.remove("d-none");
                        likesCount.innerHTML = (parseInt(likesCount.innerHTML) + 1).toString();
                        likesCountComm.innerHTML = (parseInt(likesCountComm.innerHTML) + 1).toString();
                    });
                    commLikeButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("like", "add", post.id);

                        commLikeButton.classList.add("d-none");
                        commUnlikeButton.classList.remove("d-none");
                        likeButton.classList.add("d-none");
                        unlikeButton.classList.remove("d-none");

                        likesCount.innerHTML = (parseInt(likesCount.innerHTML) + 1).toString();
                        likesCountComm.innerHTML = (parseInt(likesCountComm.innerHTML) + 1).toString();
                    });

                    unlikeButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("like", "remove", post.id);

                        likeButton.classList.remove("d-none");
                        unlikeButton.classList.add("d-none");
                        commLikeButton.classList.remove("d-none");
                        commUnlikeButton.classList.add("d-none");
                        likesCount.innerHTML = (parseInt(likesCount.innerHTML) - 1).toString();
                        likesCountComm.innerHTML = (parseInt(likesCountComm.innerHTML) - 1).toString();
                    });
                    commUnlikeButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("like", "remove", post.id);

                        commLikeButton.classList.remove("d-none");
                        commUnlikeButton.classList.add("d-none");
                        likeButton.classList.remove("d-none");
                        unlikeButton.classList.add("d-none");
                        likesCount.innerHTML = (parseInt(likesCount.innerHTML) - 1).toString();
                        likesCountComm.innerHTML = (parseInt(likesCountComm.innerHTML) - 1).toString();
                    });
                    saveButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("bookmark", "add", post.id);

                        saveButton.classList.add("d-none");
                        unsaveButton.classList.remove("d-none");
                        commSaveButton.classList.add("d-none");
                        commUnsaveButton.classList.remove("d-none");
                    });
                    commSaveButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("bookmark", "add", post.id);

                        commSaveButton.classList.add("d-none");
                        commUnsaveButton.classList.remove("d-none");
                        saveButton.classList.add("d-none");
                        unsaveButton.classList.remove("d-none");
                    });
                    unsaveButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("bookmark", "remove", post.id);

                        saveButton.classList.remove("d-none");
                        unsaveButton.classList.add("d-none");
                        commSaveButton.classList.remove("d-none");
                        commUnsaveButton.classList.add("d-none");
                        if(type_pl === "saved") {
                            postDiv.remove();
                        }
                    });
                    commUnsaveButton.addEventListener('click', function (event) {
                        event.preventDefault();
                        msgmthd("bookmark", "remove", post.id);

                        commSaveButton.classList.remove("d-none");
                        commUnsaveButton.classList.add("d-none");
                        saveButton.classList.remove("d-none");
                        unsaveButton.classList.add("d-none");
                    });
                    userProfileLink.addEventListener('click', function (event) {
                        event.preventDefault();
                        profileLoader(post.user_id);
                    });
                    usernameProfileLink.addEventListener('click', function (event) {
                        event.preventDefault();
                        profileLoader(post.user_id);
                    });
                    commentButton.addEventListener('click', function (event) {
                        event.preventDefault();

                        const panelView = postDiv.querySelector('.panel-view');
                        const commPanelView = postDiv.querySelector('.comm-panel-view');
                        const sendField = postDiv.querySelector('.comment-block');
                        const closePanelButton = postDiv.querySelector('.comm-close');
                        const inputField = postDiv.querySelector('.comm-input');
                        const buttonSend = postDiv.querySelector('.comm-send');

                        panelView.classList.add("d-none");
                        commPanelView.classList.remove("d-none");
                        sendField.classList.remove("d-none");
                        setTimeout(() => {
                            commentInner.scrollTop = commentInner.scrollHeight;
                        }, 0);

                        inputField.focus();
                        closePanelButton.addEventListener('click', function (event) {
                            event.preventDefault();
                            panelView.classList.remove("d-none");
                            commPanelView.classList.add("d-none");
                            sendField.classList.add("d-none");
                        });
                        inputField.addEventListener("input", function (event) {
                            buttonSend.disabled = inputField.value.length <= 0;
                        });
                        buttonSend.addEventListener('click', function (event) {
                            event.preventDefault();
                            const msg = inputField.value;

                            addComment(post.id, msg);

                            inputField.value = "";
                            buttonSend.disabled = true;
                            const currentDate = new Date();
                            const day = currentDate.getDate().toString().padStart(2, '0');
                            const month = (currentDate.getMonth() + 1).toString().padStart(2, '0');
                            const year = currentDate.getFullYear().toString();
                            const hours = currentDate.getHours().toString().padStart(2, '0');
                            const minutes = currentDate.getMinutes().toString().padStart(2, '0');
                            const formattedDate = `${day}.${month}.${year} ${hours}:${minutes}`;
                            const imageInit = document.getElementById("image-profile-init");
                            const name = imageInit.getAttribute("data-name");
                            const username = imageInit.getAttribute("data-username");
                            const userId = imageInit.getAttribute("data-user-id");
                            const commentD = document.createElement('div');

                            commentD.className = "list-group-item list-group-item-action d-flex gap-3";
                            commentD.setAttribute("data-user-id", `${userId}`);
                            commentD.innerHTML = `
                                <img src="${imgUrl}" alt="twbs" width="28" height="28" class="rounded-circle flex-shrink-0 mt-2">
                                <div class="d-flex gap-2 w-100 justify-content-between">
                                    <div>
                                        <a class="mb-0" href="#"><a class="fw-semibold text-decoration-none text-dark" href="#" style="font-size: 15px;">${name}</a> <a class="fw-light text-decoration-none text-dark" href="#" style="font-size: 15px;">@${username}</a></a>
                                        <p class="mb-0 opacity-75" style="font-size: 14px;">${msg}</p>
                                    </div>
                                    <small class="opacity-50 text-nowrap" style="font-size: 14px;">${formattedDate}</small>
                                </div>
                            `;
                            commentInner.appendChild(commentD);
                            commentsCount.innerHTML = (parseInt(commentsCount.innerHTML) + 1).toString();
                            setTimeout(() => {
                                commentInner.scrollTop = commentInner.scrollHeight;
                            }, 0);
                        });
                    });
                }
                postsF.appendChild(postDiv);
                //console.log(postsF.childNodes.length);
                while (postsF.childNodes.length > maxPosts) {
                    postsF.removeChild(postsF.firstChild);
                }
            });

            // Add buttons (after foreach above)
            const currentPage = posts.current_page;
            const numPages = posts.num_pages;
            const hasPrevious = posts.has_previous;
            const hasNext = posts.has_next;
            const ButtonsDiv = document.createElement('div');
            ButtonsDiv.id = "buttons-nav";
            ButtonsDiv.className = "mb-2 pt-3";
            ButtonsDiv.innerHTML = `
                <ul class="pagination justify-content-center">
                    <li class="page-item prev_b">
                        <a class="page-link" href="#">Previous</a>
                    </li>
                    <li class="page-item f_b"><a class="page-link f_b_text" href="#">1</a></li>
                    <li class="page-item s_b"><a class="page-link s_b_text" href="#">2</a></li>
                    <li class="page-item t_b"><a class="page-link t_b_text" href="#">3</a></li>
                    <li class="page-item next_b">
                        <a class="page-link" href="#">Next</a>
                    </li>
                </ul>
            `;

            const prevButton = ButtonsDiv.querySelector('.prev_b');
            const nextButton = ButtonsDiv.querySelector('.next_b');
            const firstButton = ButtonsDiv.querySelector('.f_b');
            const firstButtonText = ButtonsDiv.querySelector('.f_b_text');
            const secondButton = ButtonsDiv.querySelector('.s_b');
            const secondButtonText = ButtonsDiv.querySelector('.s_b_text');
            const thirdButton = ButtonsDiv.querySelector('.t_b');
            const thirdButtonText = ButtonsDiv.querySelector('.t_b_text');
            const nextPage = currentPage + 1;
            const prevPage = currentPage - 1;

            firstButtonText.innerHTML = prevPage.toString();
            secondButtonText.innerHTML = currentPage;
            secondButton.classList.add("active");
            thirdButtonText.innerHTML = nextPage.toString();

            if (hasPrevious) {
                prevButton.classList.remove("disabled");
            } else {
                prevButton.classList.add("disabled");
            }

            if (hasNext) {
                nextButton.classList.remove("disabled");
            } else {
                nextButton.classList.add("disabled");
            }

            if (numPages === 1) {
                secondButton.classList.add("d-none");
                thirdButton.classList.add("d-none");
            }

            if (currentPage === 1) {
                thirdButton.classList.add("d-none");
                firstButtonText.innerHTML = 1;
                firstButton.classList.add("active");
                secondButtonText.innerHTML = 2;
                secondButton.classList.remove("active");
                prevButton.classList.add("disabled");
                // Add listeners
                secondButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(2, "user", user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(2, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(2, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(2, type_pl);
                    }
                });
                nextButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(2, "user", user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(2, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(2, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(2, type_pl);
                    }
                });
            } else if (currentPage === numPages) {
                thirdButton.classList.add("d-none");
                firstButtonText.innerHTML = prevPage.toString();
                secondButtonText.innerHTML = numPages;
                secondButton.classList.add("active");
                nextButton.classList.add("disabled");
                firstButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(prevPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(prevPage, type_pl);
                    }
                });
                prevButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(prevPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(prevPage, type_pl);
                    }
                });
            } else {
                prevButton.classList.remove("disabled");
                nextButton.classList.remove("disabled");
                firstButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(prevPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(prevPage, type_pl);
                    }
                });
                prevButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(prevPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(prevPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(prevPage, type_pl);
                    }
                });

                thirdButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(nextPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(nextPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(nextPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(nextPage, type_pl);
                    }
                });
                nextButton.addEventListener('click', function (event) {
                    event.preventDefault();
                    if (type_pl === "user") {
                        postsLoader(nextPage, type_pl, user_pl);
                    } else if (type_pl === "all") {
                        postsLoader(nextPage, type_pl);
                    } else if (type_pl === "following") {
                        postsLoader(nextPage, type_pl);
                    } else if (type_pl === "saved") {
                        postsLoader(nextPage, type_pl);
                    }
                });
            }
            postsF.append(ButtonsDiv);
            const pgPage = parseInt(page_pl);
            if (pgPage === 1) {
                allPostsView.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                    inline: "nearest"
                });
            } else {
                ButtonsDiv.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                    inline: "nearest"
                });

            }
        }
    })
    .catch(error => console.error(error));
    let func;
    let hrefURL;
    if (type_pl === "all") {
        hrefURL = `/posts/all/${page_pl}`;
        func = "all";
    } else if (type_pl === "user") {
        hrefURL = `/profile/${user_pl}/${page_pl}`;
        func = "profile";
    } else if (type_pl === "following") {
        hrefURL = `/posts/following/${page_pl}`;
        func = "following";
    } else if (type_pl === "saved") {
        hrefURL = `/posts/saved/${page_pl}`;
        func = "saved";
    }
    //window.location.href = hrefURL;
    //history.pushState(null, null, hrefURL);
    //window.location.href = hrefURL;
    const state = {
        "func" : func,
        "type" : type_pl,
        "id" : user_pl,
        "page" : page_pl
    }
    //console.log(history.state);
    // if (history.state) {
    //     history.replaceState(state, null, hrefURL);
    // } else {
    //     history.pushState(state, null, hrefURL);
    // }
    if (history.state && history.state.func === func && history.state.type === type_pl && history.state.id === user_pl && history.state.page === page_pl) {
        history.replaceState(state, null, hrefURL);
    } else {
        history.pushState(state, null, hrefURL);
    }
    //const container = document.getElementById("scroll-kek");
    const allPostsViewA = document.getElementById("scroll-kek");

    //allPostsViewA.scrollTo(0, allPostsViewA.scrollHeight);
    //allPostsViewA.scrollBy(0, -1);

    //allPostsViewA.scrollTop = allPostsView.scrollHeight;

    //console.log(history.state);
    //allPostsView.scroll;


}

function profileLoader(id, pg_number = 1) {
    removeActive();
    viewsDisable();

    // HTML elements
    const profileView = document.querySelector('#profile_view');
    profileView.classList.remove("d-none");
    profileView.setAttribute("data-curr-id", id);
    const editProfileButton = profileView.querySelector('#edit-profile-button');
    const followButton = profileView.querySelector('#follow-profile-button');
    const unfollowButton = profileView.querySelector('#unfollow-profile-button');
    const nameText = profileView.querySelector('#name-profile-text');
    const usernameText = profileView.querySelector('#username-profile-text');
    const numberOfPostsText = profileView.querySelector('#posts-profile-text');
    const numberOfFollowersText = profileView.querySelector('#followers-profile-text');
    const numberOfFollowingText = profileView.querySelector('#following-profile-text');
    const aboutText = profileView.querySelector('#bio-profile-text');
    const profileImage = profileView.querySelector('#image-profile');
    const currUserId = parseInt(profileView.getAttribute("data-user-id"));
    const loadedId = parseInt(profileView.getAttribute("data-curr-id"));
    const profileButton = document.querySelector('#profile-side');
    if (currUserId === loadedId) {
        profileButton.classList.add("active");
    }
    // Hide buttons
    editProfileButton.classList.add("d-none");
    followButton.classList.add("d-none");
    unfollowButton.classList.add("d-none");
    // Fetching profile data
    fetch(`http://127.0.0.1:8000/user?profile=${id}`)
    .then(response => response.json())
    .then(profile => {
        if(profile.same === true) {
            // REMOVE THIS WHEN EDIT PROFILE IS READY
            //editProfileButton.classList.remove("d-none");
        } else {
            if (profile.is_following === true) {
                unfollowButton.classList.remove("d-none");
            } else if (profile.is_following === false) {
                followButton.classList.remove("d-none");
            }
        }

        if(profile.url === "") {
            profileImage.src = standartImageUrl;
        } else {
            profileImage.src = profile.url;
        }
        nameText.innerHTML = profile.name;
        usernameText.innerHTML = `@${profile.username}`;
        numberOfPostsText.innerHTML = profile.posts_count;
        numberOfFollowersText.innerHTML = profile.followers_count;
        numberOfFollowingText.innerHTML = profile.following_count;

        if(profile.bio === "") {
            aboutText.innerHTML = "Here should be some information about user, but he didn't write anything about himself...=(";
        } else {
            aboutText.innerHTML = profile.bio;
        }

        postsLoader(pg_number, "user", id);
    })
    .catch(error => console.error(error));
}

function profileButtonsListener() {
    const profileView = document.querySelector('#profile_view');
    profileView.classList.remove("d-none");
    let currentProfileId;
    const editProfileButton = profileView.querySelector('#edit-profile-button');
    const followButton = profileView.querySelector('#follow-profile-button');
    const unfollowButton = profileView.querySelector('#unfollow-profile-button');
    const numberOfFollowersText = profileView.querySelector('#followers-profile-text');
    const numberOfFollowingText = profileView.querySelector('#following-profile-text');
    // Adding event listeners
    editProfileButton.addEventListener('click', function (event) {
        event.preventDefault();
    });
    followButton.addEventListener('click', function (event) {
        event.preventDefault();
        currentProfileId = profileView.getAttribute("data-curr-id");
        followUnfollow("follow", currentProfileId);
        followButton.classList.add("d-none");
        unfollowButton.classList.remove("d-none");
        const newNumber = parseInt(numberOfFollowersText.innerHTML) + 1;
        numberOfFollowersText.innerHTML = newNumber.toString();
    });
    unfollowButton.addEventListener('click', function (event) {
        event.preventDefault();
        currentProfileId = profileView.getAttribute("data-curr-id");
        followUnfollow("unfollow", currentProfileId);
        unfollowButton.classList.add("d-none");
        followButton.classList.remove("d-none");
        const newNumber = parseInt(numberOfFollowersText.innerHTML) - 1;
        numberOfFollowersText.innerHTML = newNumber.toString();
    });
    numberOfFollowersText.addEventListener('click', function (event) {
        event.preventDefault();
        currentProfileId = profileView.getAttribute("data-curr-id");
        followerFollowingLoader("followers", currentProfileId);
    });
    numberOfFollowingText.addEventListener('click', function (event) {
        event.preventDefault();
        currentProfileId = profileView.getAttribute("data-curr-id");
        followerFollowingLoader("following", currentProfileId);
    });
}
function viewsDisable() {
    const profileView = document.querySelector('#profile_view');
    const allPostsView = document.querySelector('#all_posts_view');
    const followingView = document.querySelector('#following_posts_view');
    const followersView = document.querySelector('#followers_view');
    const savedView = document.querySelector('#saved_view');
    const errorView = document.querySelector('#error_view');
    profileView.classList.add("d-none");
    allPostsView.classList.add("d-none");
    followingView.classList.add("d-none");
    followersView.classList.add("d-none");
    savedView.classList.add("d-none");
    errorView.classList.add("d-none");
}

function msgmthd(method, action, post_id) {
    fetch('http://127.0.0.1:8000/post', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        post_id: post_id,
        method: method,
        action: action
      })
    })
    .then(response => {
        if (response.status === 201) {
            //location.reload();
        } else if (response.status === 400) {
            response.json().then(data => {
                console.log(data.error);
            });
        }
    });
}

function addComment(post_id, msg) {
    fetch('http://127.0.0.1:8000/post', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        post_id: post_id,
        method: "comment",
        action: "None",
        text: msg
      })
    })
    .then(response => {
        if (response.status === 201) {
            //location.reload();
        } else if (response.status === 400) {
            response.json().then(data => {
                console.log(data.error);
            });
        }
    });
}

function followUnfollow(method, id) {
    fetch('http://127.0.0.1:8000/user', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        method: method,
        id: id
      })
    })
    .then(response => {
        if (response.status === 201) {
            //location.reload();
        } else if (response.status === 400) {
            response.json().then(data => {
                console.log(data.error);
            });
        }
    });
}

function followerFollowingLoader(type, id) {
    let fetchUrl;
    let area;
    const modalWindow = document.querySelector('#followersBackdrop');
    const title = modalWindow.querySelector('#followersBackdropLabel');
    const modal = new bootstrap.Modal(modalWindow);
    if (type === "followers") {
        area = modalWindow.querySelector('.m-fill-area');
        title.innerHTML = "Followers";
        fetchUrl = `http://127.0.0.1:8000/user?followers=${id}`;
    } else if (type === "following") {
        area = modalWindow.querySelector('.m-fill-area');
        title.innerHTML = "Following";
        fetchUrl = `http://127.0.0.1:8000/user?following=${id}`;
    } else if (type === "followers-m") {
        area = document.querySelector('#all_followers-m');
        fetchUrl = `http://127.0.0.1:8000/user?followers=${id}`;
    }
    area.innerHTML = ``;
    fetch(fetchUrl)
    .then(response => response.json())
    .then(users => {
        if(type === "followers-m") {
            const newDiv = document.createElement('div');
            newDiv.innerHTML = `<p class="h3 text-center">Followers</p><hr>`;
            area.appendChild(newDiv);
        }
        users.follow.forEach(user => {
            let url;
            if (user.url === "") {
                url = standartImageUrl;
            } else {
                url = user.url;
            }
            const userDiv = document.createElement('div');
            userDiv.className = "list-group-item d-flex align-items-center";
            userDiv.innerHTML = `
                <img src="" alt="" width="38" height="38" class="rounded-circle flex-shrink-0 me-3 image-m-follow"/>
                <div class="flex-fill">
                    <div><a class="text-dark foll-font-m text-decoration-none fw-semibold name-m"></a></div>
                    <div><a class="text-dark foll-font text-decoration-none username-m" style="color: rgba(255, 255, 255, 0.3);"></a></div>
                </div>
                <a class="btn btn-outline-primary rounded-pill follow-m-button">Follow</a>
                <a class="btn btn-outline-secondary rounded-pill unfollow-m-button">Unfollow</a>
            `;
            const image = userDiv.querySelector('.image-m-follow');
            const name = userDiv.querySelector('.name-m');
            const username = userDiv.querySelector('.username-m');
            const followButton = userDiv.querySelector('.follow-m-button');
            const unfollowButton = userDiv.querySelector('.unfollow-m-button');
            image.src = url;
            name.innerHTML = user.name;
            username.innerHTML = `@${user.username}`;
            if (user.is_followed) {
                followButton.classList.add("d-none");
                unfollowButton.classList.remove("d-none");
            } else if (!user.is_followed) {
                followButton.classList.remove("d-none");
                unfollowButton.classList.add("d-none");
            }
            followButton.addEventListener('click', () => {
                followUnfollow("follow", user.id);
                followButton.classList.add("d-none");
                unfollowButton.classList.remove("d-none");
            });
            unfollowButton.addEventListener('click', () => {
                followUnfollow("unfollow", user.id);
                followButton.classList.remove("d-none");
                unfollowButton.classList.add("d-none");
            });
            name.addEventListener('click', () => {
                profileLoader(user.id);
            });
            username.addEventListener('click', () => {
                profileLoader(user.id);
            });
            area.appendChild(userDiv);
        });
    })
    .catch(error => console.error(error));

    if (type === "followers" || type === "following") {
        modal.show();
        if (type === "followers") {
            //history.pushState(null, null, `/posts/saved/${page_pl}`);
        } else if (type === "following") {
            //history.pushState(null, null, `/posts/saved/${page_pl}`);
        }

    } else if (type === "followers-m") {
        const state = {
            "func" : "followers",
            "type" : type,
            "id" : id
        }
        if (history.state && history.state.func === "followers" && history.state.type === type && history.state.id === id) {
            history.replaceState(state, null, `/followers`);
        } else {
            history.pushState(state, null, `/followers`);
        }
        console.log(history.state);
    }
}

function errorLoader() {
    viewsDisable();
    const errorView = document.querySelector('#error_view');
    errorView.classList.remove('d-none');
    const state = {
        "func" : "404",
    }
    if (history.state && history.state.func === "404") {
        history.replaceState(state, null, `/404`);
    } else {
        history.pushState(state, null, `/404`);
    }
    //history.pushState(state, null, hrefURL);
    console.log(history.state);
}

function locationListener() {
    const allPosts = document.querySelector('#all-posts-side');
    const savedPosts = document.querySelector('#saved-side');
    const profileB = document.querySelector('#profile-side');
    const following = document.querySelector('#following-side');
    const followers = document.querySelector('#followers-side');
    const followersView = document.querySelector('#followers_view');
    const allPostsView = document.querySelector('#all_posts_view');
    const savedPostsView = document.querySelector('#saved_view');
    const profileView = document.querySelector('#profile_view');
    const followingView = document.querySelector('#following_posts_view');
    const userId = followersView.getAttribute('data-user-id');
    if (window.location.href.endsWith("#")) {
        history.pushState(null, null, window.location.href.slice(0, -1));
    }

    // Get the path from the URL
    const path = new URL(window.location.href).pathname;

    // Split the path into parts
    const parts = path.split('/');

    if (parts[1] === "") {
        postsLoader(1, "all");
    } else if (parts[1] === "followers") {
        followerFollowingLoader("followers-m", userId);
        viewsDisable();
        removeActive();

        followers.classList.add('active');
        followersView.classList.remove('d-none');
    } else if (parts[1] === "posts") {
        viewsDisable();
        removeActive();

        if (parts[2] !== "") {
            if (parts[2] === "all") {
                allPosts.classList.add('active');
                allPostsView.classList.remove('d-none');
            } else if (parts[2] === "following") {
                following.classList.add('active');
                followingView.classList.remove('d-none');
            } else if (parts[2] === "saved") {
                savedPosts.classList.add('active');
                savedPostsView.classList.remove('d-none');
            }
            if (parts[3] !== "") {
                postsLoader(parts[3], parts[2]);
            }
        }
    } else if (parts[1] === "profile") {
        viewsDisable();
        removeActive();

        profileView.classList.remove('d-none');
        const profileId = parseInt(parts[2]);
        const currentUserId = parseInt(userId);
        if (parts[2] !== "") {
           if (profileId === currentUserId) {
               profileB.classList.add('active');
           }
           profileLoader(parts[2], parseInt(parts[3]));
        }
    } else if (parts[1].includes("404")) {
        errorLoader();
    } else {
        errorLoader();
    }
}

function popStateListener() {
    window.addEventListener('popstate', event => {
        if (event.state === null) {
            console.log("Some Error Occurred!:(");
        } else {
            const allPosts = document.querySelector('#all-posts-side');
            const savedPosts = document.querySelector('#saved-side');
            const profileB = document.querySelector('#profile-side');
            const following = document.querySelector('#following-side');
            const followers = document.querySelector('#followers-side');
            viewsDisable();
            removeActive();
            const currentUserId = parseInt(document.getElementById("all_posts_view").getAttribute("data-user-id"));

            if (event.state.func === "all") {
                allPosts.classList.add("active");
                let pageNumber = 1;
                if (event.state.page) {
                    pageNumber = event.state.page;
                }
                postsLoader(pageNumber, "all");
            } else if (event.state.func === "profile") {

                let pageNumber = 1;
                const profileId = parseInt(event.state.id);
                if (event.state.page) {
                    pageNumber = event.state.page;
                }
                if (currentUserId === profileId) {
                    profileB.classList.add("active");
                    //console.log("current user");
                    profileLoader(event.state.id, pageNumber);
                } else {
                    profileLoader(event.state.id, pageNumber);
                }
                // all profile following saved
            } else if (event.state.func === "following") {
                let pageNumber = 1;
                if (event.state.page) {
                    pageNumber = event.state.page;
                }
                following.classList.add("active");
                postsLoader(pageNumber, "following");
            } else if (event.state.func === "saved") {
                savedPosts.classList.add("active");
                let pageNumber = 1;
                if (event.state.page) {
                    pageNumber = event.state.page;
                }
                postsLoader(pageNumber, "saved");
            } else if (event.state.func === "followers") {
                const followersView = document.querySelector('#followers_view');
                followersView.classList.remove("d-none");
                followers.classList.add("active");
                followerFollowingLoader("followers-m", event.state.id);
            } else if (event.state.func === "404") {
                errorLoader();
            }
        }
    });
}

