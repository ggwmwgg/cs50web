document.addEventListener('DOMContentLoaded', function () {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })

    // Send email modal form listener
    sendEmailFormListener();
    // Send email button listener
    sendEmailListener();

    const textarea1 = document.getElementById("replyMessage");
    textarea1.addEventListener("input", function () {
        this.style.height = "";
        this.style.height = this.scrollHeight + "px";
    });

    // Use buttons to toggle between views
    document.querySelector('#inbox').addEventListener('click', () => {
        $("#emails-view").fadeOut(400, function () {
            loadMailbox('inbox');
            $("#emails-view").fadeIn(400);
        });
    });
    document.querySelector('#sent').addEventListener('click', () => {
        $("#emails-view").fadeOut(400, function () {
            loadMailbox('sent');
            $("#emails-view").fadeIn(400);
        });
    });
    document.querySelector('#archived').addEventListener('click', () => {
        $("#emails-view").fadeOut(400, function () {
            loadMailbox('archive');
            $("#emails-view").fadeIn(400);
        });
    });

    // By default, load the inbox
    loadMailbox('inbox');

    // Listener for back button
    backButtonListener();

    // Listener for archive button
    archiveButtonListener();

    // Listener for unarchive button
    unarchiveButtonListener();

    // Listener for read button
    readButtonListener();

    // Listener for unread button
    unreadButtonListener();

    // Listener for reply button
    replyButtonListener();

    // Listener for close reply tab button
    replyCloseButtonListener();

    // Listener for send reply button
    replySendButtonListener();

});


function loadMailbox(mailbox) {

    // Show the mailbox and hide other views
    const emailsView = document.querySelector('#emails-view');
    const emailContentView = document.querySelector('#email-content-view');
    const container = document.querySelector('#whole-container');

    // hide the email content view and sent emails form
    emailContentView.classList.add("d-none");
    emailsView.classList.remove("d-none");
    container.classList.add("border");

    // Show the mailbox name
    emailsView.innerHTML = `<h3 class="text-center">${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
    loadInbox(mailbox);
}

function loadInbox(type) {
    fetch(`/emails/${type}`)
        .then(response => response.json())
        .then(emails => {
            for (let i = 0; i < emails.length; i++) {
                let email = emails[i];
                const formattedDate = formatDate(email.timestamp)
                let element = document.createElement('button');
                element.type = "button";
                if (type === "inbox") {
                    if (email.read === true) {
                        element.classList.add("bg-body-secondary");
                        element.className = "list-group-item list-group-item-action list-group-item-secondary";
                        element.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
              <span class="text-truncate w-50" style="flex: 2 2 0;">
                ${email.sender}
              </span>
              <span class="text-truncate w-50" style="flex: 3 3 0;">${email.subject} - ${email.body}</span>
              <span class="text w-50 float-right" style="flex: 1 1 0;">${formattedDate}</span>
            </div>
          `;
                    } else {
                        element.className = "list-group-item list-group-item-action";

                        element.innerHTML = `
            <div class="d-flex w-100 justify-content-between">
              <span class="text-truncate w-50" style="flex: 2 2 0;">
                <strong>${email.sender}</strong>
              </span>
              <span class="text-truncate w-50" style="flex: 3 3 0;"><strong>${email.subject}</strong> - ${email.body}</span>
              <span class="text w-50 float-right" style="flex: 1 1 0;">${formattedDate}</span>
            </div>
          `;
                    }
                } else {
                    element.className = "list-group-item list-group-item-action";
                    element.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
            <span class="text-truncate w-50" style="flex: 2 2 0;">
              <strong>${email.sender}</strong>
            </span>
            <span class="text-truncate w-50" style="flex: 3 3 0;"><strong>${email.subject}</strong> - ${email.body}</span>
            <span class="text w-50 float-right koker" style="flex: 1 1 0;">${formattedDate}</span>
          </div>
        `;
                }
                document.querySelector('#emails-view').append(element);
                element.addEventListener('click', () => {
                    showEmail(email, type);
                });
            }
        });
}

function showEmail(email, type) {

    fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
    })
        .then(() => {
            const emailsView = document.querySelector('#emails-view');
            const emailContentView = document.querySelector('#email-content-view');
            const container = document.querySelector('#whole-container');
            $("#emails-view").fadeOut(400, function () {
                emailsView.classList.add("d-none");
                $("#email-content-view").fadeIn(400);
                emailContentView.classList.remove("d-none");
            });
            container.classList.remove("border");
            fetch(`/emails/${email.id}`)
                .then(response => response.json())
                .then(nemail => {
                    document.querySelector('#email-content-id').innerHTML = nemail.id;
                    document.querySelector('#email-content-sender').innerHTML = nemail.sender;
                    document.querySelector('#email-content-subject').innerHTML = nemail.subject;
                    document.querySelector('#email-content-body').innerHTML = `<pre style="white-space: pre-wrap;">${nemail.body}</pre>`;
                    document.querySelector('#email-content-recipient').innerHTML = nemail.recipients;
                    document.querySelector('#email-content-date').innerHTML = formatDate(nemail.timestamp);

                    prefillReplyMessage(nemail.id, nemail.sender, nemail.recipients, nemail.subject, nemail.body, formatDate(nemail.timestamp));

                    const replyButton = document.querySelector('#email-content-reply');
                    const readButton = document.querySelector('#email-content-read');
                    const unreadButton = document.querySelector('#email-content-unread');
                    const archiveButton = document.querySelector('#email-content-archive');
                    const unarchiveButton = document.querySelector('#email-content-unarchive');
                    if (type === "inbox") {
                        if (nemail.read === true) {
                            readButton.classList.add("d-none");
                            unreadButton.classList.remove("d-none");
                        } else {
                            readButton.classList.remove("d-none");
                            unreadButton.classList.add("d-none");
                        }
                        if (nemail.archived === false) {
                            archiveButton.classList.remove("d-none");
                            unarchiveButton.classList.add("d-none");
                        } else {
                            archiveButton.classList.add("d-none");
                            unarchiveButton.classList.remove("d-none");
                        }
                        replyButton.classList.remove("d-none");

                    } else if (type === 'archive') {
                        if (nemail.archived === false) {
                            archiveButton.classList.remove("d-none");
                            unarchiveButton.classList.add("d-none");
                        } else {
                            archiveButton.classList.add("d-none");
                            unarchiveButton.classList.remove("d-none");
                        }
                    } else if (type === 'sent') {
                        archiveButton.classList.remove("d-none");
                    }
                });
        });
}

function prefillReplyMessage(emailId, from, to, subject, message, date) {
    const email = document.querySelector('#email').innerHTML;
    document.querySelector('#replyTo').value = from;
    document.querySelector('#replyFrom').value = email;
    document.querySelector('#replySubject').value = `Re: ${subject}`;
    const msg = document.querySelector('#replyMessage')
    msg.value = `On ${date} ${from} wrote:
${message}
---------------------------------------------------------------------------------


`;
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString("pl-PL", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
    }) + " " + date.toLocaleTimeString("pl-PL", {
        hour: "2-digit",
        minute: "2-digit"
    });
}

function sendEmail(exampleModal) {
    const message = exampleModal.querySelector('#message-text').value;
    const toSend = exampleModal.querySelector('#message-to').value;
    const subject = exampleModal.querySelector('#message-subject').value;
    fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: toSend,
            subject: subject,
            body: message
        })
    })
        .then((response) => {
            if (response.status === 201) {
                $("#emails-view").fadeOut(400, function () {
                    showAlert('success', 'Message sent successfully');
                    loadMailbox('sent');
                    $("#emails-view").fadeIn(400);
                });
            } else if (response.status === 400) {
                showAlert('error', 'Message failed to send');
            }
        });
    // Closing the modal
    const modal = bootstrap.Modal.getInstance(exampleModal)
    modal.hide();
}

function backButtonListener() {
    const backButton = document.querySelector('#email-content-back');
    backButton.addEventListener("click", () => {
        $('#replySlider').slideUp('slow');
        const replyButton = document.querySelector('#email-content-reply');
        const replySendButton = document.querySelector('#email-content-send');
        const closeButton = document.querySelector('#email-content-send-close');
        replyButton.classList.add("d-none");
        replySendButton.classList.add("d-none");
        closeButton.classList.add("d-none");
        const type = document.querySelector("#emails-view h3").innerHTML.toLowerCase();
        $("#email-content-view").animate({
            left: "100%",
            opacity: 0
        }, 400, function () {
            loadMailbox(type);
            $("#email-content-view").css({
                left: "0",
                opacity: 1
            });
            $("#emails-view").fadeIn(400);
        });
    });
}

function archiveButtonListener() {
    const archiveButton = document.querySelector('#email-content-archive');
    archiveButton.addEventListener("click", () => {
        // getting email id from the email-content-id
        const email = document.querySelector('#email-content-id').innerHTML;
        fetch(`/emails/${email}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
        })
            .then(() => {
                $("#emails-view").fadeOut(400, function () {
                    showAlert('success', 'Message archived successfully')
                    loadMailbox('archive');
                    $("#emails-view").fadeIn(400);
                });
            });
    });
}

function unarchiveButtonListener() {
    const unarchiveButton = document.querySelector('#email-content-unarchive');
    unarchiveButton.addEventListener("click", () => {
        const email = document.querySelector('#email-content-id').innerHTML;
        fetch(`/emails/${email}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
        })
            .then(() => {
                $("#emails-view").fadeOut(400, function () {
                    showAlert('success', 'Message moved to inbox')
                    loadMailbox('inbox');
                    $("#emails-view").fadeIn(400);
                });
            });
    });
}

function readButtonListener() {
    // add event listener to the read button
    const readButton = document.querySelector('#email-content-read');
    readButton.addEventListener("click", () => {
        const email = document.querySelector('#email-content-id').innerHTML;
        fetch(`/emails/${email}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
        })
            .then(() => {
                $("#emails-view").fadeOut(400, function () {
                    showAlert('success', 'Message marked as read')
                    loadMailbox('inbox');
                    $("#emails-view").fadeIn(400);
                });
            });
    });
}

function unreadButtonListener() {
    // add event listener to the unread button
    const unreadButton = document.querySelector('#email-content-unread');
    unreadButton.addEventListener("click", () => {
        const email = document.querySelector('#email-content-id').innerHTML;
        fetch(`/emails/${email}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: false
            })
        })
            .then(() => {
                $("#emails-view").fadeOut(400, function () {
                    showAlert('success', 'Message marked as unread');
                    loadMailbox('inbox');
                    $("#emails-view").fadeIn(400);
                });
            });
    });
}

function sendEmailListener() {
    const submitBtn = exampleModal.querySelector('#submitBtn');
    submitBtn.addEventListener('click', (event) => {
        const exampleModal = document.getElementById('exampleModal');
        event.preventDefault();
        sendEmail(exampleModal);
    });
}

function sendEmailFormListener() {
    const exampleModal = document.getElementById('exampleModal')
    exampleModal.addEventListener('show.bs.modal', event => {
        const button = event.relatedTarget
        const sender = button.getAttribute('data-sender')
        const modalTitle = exampleModal.querySelector('.modal-title')
        const modalBodyInput = exampleModal.querySelector('.modal-body input')
        modalTitle.textContent = `New message`
        modalBodyInput.value = sender
    })
}

function replyButtonListener() {
    document.querySelector('#email-content-reply').addEventListener('click', () => {
        const replyButton = document.querySelector('#email-content-reply');
        const replySendButton = document.querySelector('#email-content-send');
        const closeButton = document.querySelector('#email-content-send-close');
        const msg = document.querySelector('#replyMessage')
        replyButton.classList.add("d-none");
        replySendButton.classList.remove("d-none");
        closeButton.classList.remove("d-none");
        $('#replySlider').slideDown('slow');
        msg.focus();
    });
}

function replyCloseButtonListener() {
    document.querySelector('#email-content-send-close').addEventListener('click', () => {
        const replyButton = document.querySelector('#email-content-reply');
        const replySendButton = document.querySelector('#email-content-send');
        const closeButton = document.querySelector('#email-content-send-close');
        replyButton.classList.remove("d-none");
        replySendButton.classList.add("d-none");
        closeButton.classList.add("d-none");
        $('#replySlider').slideUp('slow');
    });
}

function replySendButtonListener() {
    document.querySelector('#email-content-send').addEventListener('click', () => {
        const message = document.querySelector('#replyMessage').value;
        const to = document.querySelector('#replyTo').value;
        const subject = document.querySelector('#replySubject').value;
        console.log(message);
        fetch('/emails', {
            method: 'POST',
            body: JSON.stringify({
                recipients: to,
                subject: subject,
                body: message
            })
        })
            .then((response) => {
                if (response.status === 201) {
                    const replyButton = document.querySelector('#email-content-reply');
                    const replySendButton = document.querySelector('#email-content-send');
                    const closeButton = document.querySelector('#email-content-send-close');
                    replyButton.classList.add("d-none");
                    replySendButton.classList.add("d-none");
                    closeButton.classList.add("d-none");
                    $("#replySlider").slideUp('slow');
                    $("#email-content-view").animate({
                        right: "100%",
                        opacity: 0
                    }, 400, function () {
                        showAlert('success', 'Message sent successfully');
                        loadMailbox('sent');
                        $("#email-content-view").css({
                            right: "0",
                            opacity: 1
                        });
                        $("#emails-view").fadeIn(400);
                    });
                } else if (response.status === 400) {
                    showAlert('error', 'Message failed to send');
                }
            });
    });
}

function showAlert(type, message) {
    const alertContainer = document.getElementById("alertContainer");

    const alertDiv = document.createElement("div");
    alertDiv.classList.add("toast");
    alertDiv.setAttribute("role", "alert");
    alertDiv.setAttribute("aria-live", "assertive");
    alertDiv.setAttribute("aria-atomic", "true");

    const headerDiv = document.createElement("div");
    headerDiv.classList.add("toast-header");

    const icon = document.createElement("i");
    if (type === "success") {
        icon.classList.add("fa-solid");
        icon.classList.add("fa-bell");
        headerDiv.classList.add("bg-body-secondary");
    } else if (type === "error") {
        icon.classList.add("fa-solid");
        icon.classList.add("fa-triangle-exclamation");
        headerDiv.classList.add("bg-danger-subtle");
    }
    icon.classList.add("rounded");
    icon.classList.add("pe-2");
    icon.setAttribute("aria-hidden", "true");
    headerDiv.appendChild(icon);

    const types = document.createElement("strong");
    types.classList.add("me-auto");
    if (type === "success") {
        types.innerHTML = 'SUCCESS!';
    } else if (type === "error") {
        types.innerHTML = 'ERROR!';
    }
    headerDiv.appendChild(types);

    const closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.classList.add("btn-close");
    closeButton.setAttribute("data-bs-dismiss", "toast");
    closeButton.setAttribute("aria-label", "Close");
    headerDiv.appendChild(closeButton);
    alertDiv.appendChild(headerDiv);

    const bodyDiv = document.createElement("div");
    bodyDiv.classList.add("toast-body");
    bodyDiv.innerHTML = message;
    alertDiv.appendChild(bodyDiv);

    alertContainer.appendChild(alertDiv);

    const toast = new bootstrap.Toast(alertDiv);
    toast.show();
}
