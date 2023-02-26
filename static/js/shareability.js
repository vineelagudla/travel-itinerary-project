'use strict';

const shareRadioButtons = document.querySelectorAll('input[name="shareability"]');
for(const radioButton of shareRadioButtons){
    radioButton.addEventListener('change', function (evt) {
        if(this.value == 2) {
            enableFriendsShareability();
        }
        else {
            disableFriendsShareability();
        }
    });
}

let friendsEmails = [];

function enableFriendsShareability() {
    const friendsEmail = document.querySelector("#friends-email");
    friendsEmail.innerHTML = 'Enter your friend\'s email <input type="text" id="friend-email"> <button id="add-email">Add</button><br><br>';
    friendsEmail.insertAdjacentHTML('beforeend', '<label style="vertical-align:middle">Added friends <textarea class="form-control" id="friends-email-tb" name="friends-email-ta" readonly></textarea></label><br><br>');

    const addEmailButton = document.querySelector("#add-email");
    addEmailButton.addEventListener('click', function (evt) {
        evt.preventDefault();
        const emailText = document.querySelector("#friend-email");
        const emailsTextbox = document.querySelector("#friends-email-tb");
        friendsEmails.push(emailText.value);
        let emailsVal = "";
        for (const email of friendsEmails) {
            if(emailsVal != "") {
                emailsVal += "\n";
            }
            emailsVal += email;
        }
        console.log(emailsVal);
        emailsTextbox.value = emailsVal;
        emailText.value = "";
    });
}

function disableFriendsShareability() {
    const friendsEmail = document.querySelector("#friends-email");
    friendsEmail.innerHTML = "";
}