var current_url = location.href;

function clearAllIntervals() {
    var id = window.setInterval(function() {}, 0);
    while (id--) {
        window.clearInterval(id);
    }
}

//SPA Request GET, load page /user/...
function loadPageUsers(pagePath, pushState = true) {
    if(pagePath === "home")
        clearAllIntervals(); 

    $.ajax({
        url: `/users/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/users/${pagePath}`);
            }
            current_url = `/users/${pagePath}/`;
            bindFormEvent();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /tournaments/...
function loadPageTournament(pagePath, tournamentName = '', pushState = true) {
    if(!pagePath) {
        return(console.log("I got you haha: ", pagePath));}
    $.ajax({
        url: `/tournaments/${pagePath}/?tournament_name=${tournamentName}`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/tournaments/${pagePath}`);
            }
            current_url = `/tournaments/${pagePath}/?tournament_name=${tournamentName}`;
            bindFormEvent();
            if (document.getElementById('tournament-name')) {
                initTournamentPage();
            }
            initializeGameTournament();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load play tournament `/${response.tournament_name}/play/${response.game_id}/`
function loadPagePlayTournament(tournament_name, game_id, pushState = true) {
    if(!tournament_name || !game_id) {
        return(console.error("tournamet_name or game_id doesn't exist", pagePath));}
    let pagePath = `${tournament_name}/play/${game_id}`
    $.ajax({
        url: `/tournaments/${pagePath}`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/tournaments/${pagePath}`);
            }
            current_url = `/tournaments/${pagePath}`;
            bindFormEvent();
            initializeGameTournament();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /matchmaking/...
function loadPageMatchmaking(pagePath, pushState = true) {
    $.ajax({
        url: `/matchmaking/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                 history.pushState({ path: pagePath, content: response.html }, '', `/matchmaking/${pagePath}`);
            }
            current_url = `/matchmaking/${pagePath}/`;
            bindFormEvent();
            if (typeof initializeGame === 'function') {
                initializeGame();
            } 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /user/...
function loadPageGames(pagePath, pushState = true) {
    $.ajax({
        url: `/games/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            console.log("pagePath: ", pagePath);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/games/${pagePath}`);
            }
            current_url = `/games/${pagePath}/`;
            bindFormEvent();
            if (typeof initializeGame === 'function' && pagePath === 'play') {
                initializeGame();
            }
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load Setting page
function loadPageUsersSettings(pagePath, pushState = true) {
    event.preventDefault();
    var profileData = $('#profileData');

    if (profileData.is(':visible')) {
        profileData.hide();
    } else {
        $.ajax({
            url: `/users/${pagePath}/`,
            success: function(response) {
                $('#profileData').html(response.html);
                $('#profileData').show();
                current_url = `/users/${pagePath}/`;
                bindFormEvent(); 
            },
            error: function(error) {
                console.error('Error loading the page:', error);
            }
        });
    }
}

//SPA Request GET, load page /Blockchain/...
function loadPageBlockchain(pagePath, pushState = true) {
    $.ajax({
        url: `/blockchain/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/blockchain/${pagePath}`);
            }
            current_url = `/blockchain/${pagePath}/`;
            bindFormEvent();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page /Aouth/...
function loadPageAouth(pagePath, pushState = true) {
    $.ajax({
        url: `/aouth/${pagePath}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: pagePath, content: response.html }, '', `/${pagePath}`);
            }
            current_url = `/aouth/${pagePath}/`;
            bindFormEvent();
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//SPA Request GET, load page profile of a friend /user/...
function loadPageFriendProfile(username, pushState = true) {
    $.ajax({
        url: `/users/friend-profile/${username}/`,
        success: function(response) {
            $('#app-content').html(response.html);
            if (pushState) {
                history.pushState({ path: `/users/friend-profile/${username}`, content: response.html }, '', `/users/friend-profile/${username}`);
            }
            current_url = `/users/friend-profile/${username}/`;
            bindFormEvent(); 
        },
        error: function(error) {
            console.error('Error loading the page:', error);
        }
    });
}

//set localstorage for connection via 42AOUTH with 2FA enable
function setLocalStorageAndLoadPage() {
    const accessToken = document.getElementById('access_token').value;
    const refreshToken = document.getElementById('refresh_token').value;
    const csrfToken = document.getElementById('csrf_token').value;
    const redirectUrl = document.getElementById('redirect_url').value;

    if (accessToken && refreshToken && csrfToken) {
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('csrf_token', csrfToken);

        loadPageUsers(redirectUrl.replace(/^\//, ''), true);
    } else {
        console.error('Missing tokens');
        window.location.href = '/login';
        current_url = '/aouth/login/';
    }
}

//SPA Request POST, Form register, login, 2FA
function bindFormEvent() {
    //REgister
    $('#registerForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
                
            }
        });
    });
    //TwoFactor'twoFactorAouth"
    $('#twoFactorAouth').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success') {
                    localStorage.setItem('access_token', response.access_token);
                    localStorage.setItem('refresh_token', response.refresh_token);
                    localStorage.setItem('csrf_token', response.csrf_token);
                    loadPageUsers(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    //connectTournament
    $('#connectTournament').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success')
                    loadPageTournament(response.redirectUrl.replace(/^\//, ''), true);
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    //generateTournament
    $('#generateTournament').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.status === 'success')
                    loadPageTournament(response.redirectUrl.replace(/^\//, ''), true);
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    $('#Set_image').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success image changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#Set_username').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success username changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    // Setting change the Password
    $('#Set_password').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success password changed");
               
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    // Setting change the 2factor
    $('#2faForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Success 2faForm");
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#enable_2fa').off('change').on('change', function(e) {
        e.preventDefault();
        bindFormEvent()
        $('#2faForm').submit();
        
    });
    //Auth login 
    $('#loginForm').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                console.log("Response received:", response);
                if (response.redirectUrl == 'home') {
                    localStorage.setItem('access_token', response.access_token);
                    localStorage.setItem('refresh_token', response.refresh_token);
                    localStorage.setItem('csrf_token', response.csrf_token);
                    loadPageUsers(response.redirectUrl.replace(/^\//, ''), true);
                }
                else if (response.status === 'success') {
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                } else {
                    console.log('Success with unexpected status:', response.message);
                    loadPageAouth(response.redirectUrl.replace(/^\//, ''), true);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });

    $('#searchFriends').off('submit').on('submit', function(e) {
        e.preventDefault();
        const queryData = $(this).serialize();
        
        $.ajax({
            type: 'GET',
            url: this.action,
            data: queryData,
            success: function(response) {
                $('#app-content').html(response.html);
                history.pushState({ path: '', content: response.html }, '', window.location.pathname);
                bindFormEvent();
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
    
    $('#AddFriends').off('submit').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            type: 'POST',
            url: this.action,
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                loadPageUsers('friend', true);
                // bindFormEvent();
            },
            error: function(xhr, status, error) {
                console.error("Error submitting form:", error);
            }
        });
    });
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            $('#imagePreview').attr('src', e.target.result);
        }
        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}


$(document).ready(function() {
    bindFormEvent();

    $("#file-upload").change(function() {
        readURL(this);
    });

    $(document).on('pjax:end', function() {
        bindFormEvent();
    });
    history.replaceState({ path: window.location.pathname, content: $('#app-content').html() }, '', window.location.pathname);

    $('body').on('click', '#goBackButton', function()
    {
        window.history.back();
    });
});


function setupGoBackButton() {
    $('#goBackButton').on('click', function() {
        window.history.back();
    });
}

function clean_matchmaking(){
    console.log("clean_match call");
    const data = new FormData();

    const csrfToken = localStorage.getItem('csrf_token');
    data.append('csrfmiddlewaretoken', csrfToken);
    const success = navigator.sendBeacon('/users/redirect/', data);
    if (!success) {
        console.error('Error sending matchmaking clean request');
    }
}

function leaveMatchmakingQueue() {
    console.log("leaveMatchmaking call");
    const data = new FormData();
    const csrfToken = localStorage.getItem('csrf_token');
    data.append('csrfmiddlewaretoken', csrfToken);

    const success = navigator.sendBeacon('/matchmaking/matchmaking_remote_leave/', data);
    if (!success) {
        console.error('Error sending leave matchmaking queue request');
    }
}

window.addEventListener('popstate', async function(event)
{
    // console.log("new url", current_url);
 
    
    if ((current_url === "/matchmaking/matchmaking_remote" || current_url === "/matchmaking/matchmaking_remote/")
        && (window.location.pathname === "/users/home" || window.location.pathname === "/users/home/")){
        console.log("check1");
        window.history.pushState(null, null, window.location.href);
        if (typeof handleLeaveMatchmaking === 'function') {
            clean_matchmaking();
            handleLeaveMatchmaking();
        }
        else {
            clean_matchmaking();
            loadPageUsers('home');
        }
    }
    else if ((current_url === "/matchmaking/matchmaking_remote" || current_url === "/matchmaking/matchmaking_remote/")
        && (window.location.pathname === "/matchmaking/matchmaking_remote" || window.location.pathname === "/matchmaking/matchmaking_remote/")){
        console.log("check2");
        clean_matchmaking();
        window.history.pushState(null, null, window.location.href);
        loadPageUsers('home');

    }
    else if (current_url === "/games/results" || current_url === "/games/results/"){
        window.history.pushState(null, null, window.location.href);
        loadPageUsers('home');
    }
    else if (window.location.pathname === '/aouth/twofactor/') {
        window.history.pushState(null, null, window.location.href);
        loadPageAouth('aouth_logout');
    }
    else if (current_url === "/games/game-in-progress" || current_url === "/games/game-in-progress/"){
        window.history.pushState(null, null, window.location.href);
        loadPageUsers('home');
    }
    else if (current_url === "/users/home" || current_url === "/users/home/" 
        || window.location.pathname === "/users/home" || window.location.pathname === "/users/home/") {
        window.history.pushState(null, null, window.location.href);
        loadPageUsers('home');
    }
    else if (event.state) {
        console.log("WTF");
        $('#app-content').html(event.state.content);
        bindFormEvent();
    }
});


window.onbeforeunload = function() {
    // console.log("event ombeforeunnload call url:", current_url);
    // console.log("event ombeforeunnload call2 url:", window.location.pathname);

    if (current_url === "/matchmaking/matchmaking_remote" || current_url === "/matchmaking/matchmaking_remote/") {
        console.log("You left the matchmaking Queue <<");
        clean_matchmaking();
        leaveMatchmakingQueue();
    }
    else if(window.location.pathname === "/matchmaking/matchmaking_remote" || window.location.pathname === "/matchmaking/matchmaking_remote/")
    {
        console.log("You left the matchmaking Queue <<");
        clean_matchmaking();
        leaveMatchmakingQueue();
    }
}

window.addEventListener('unload', async function(event){
 // console.log("Unload event call: ",current_url);

 // if (current_url === "/matchmaking/matchmaking_remote" || current_url === "/matchmaking/matchmaking_remote/") {
     // await clean_matchmaking();
     // leaveMatchmakingQueu();
     // console.log("You left the matchmaking Queue <<");
 // }
});