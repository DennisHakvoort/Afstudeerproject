document.getElementById('back-button').onclick = function () {
    window.location.href = "popup.html";
}

const userIdInput = document.getElementById("user-id-input")
const userIdSubmit = document.getElementById("user-id-submit")
const urlInput = document.getElementById("url-input")
const urlSubmit = document.getElementById("url-submit")
const confluenceInput = document.getElementById("confluence-input")
const confluenceSubmit = document.getElementById("confluence-submit")

chrome.storage.sync.get(['userId', 'url', 'confluence'], function (result) {
    if (result.userId !== undefined) {
        userIdInput.value = result.userId
    } else {
        userIdInput.value = ""
    }

    if (result.url !== undefined) {
        urlInput.value = result.url
    } else {
        urlInput.value = ""
    }

    if (result.confluence !== undefined) {
        confluenceInput.value = result.confluence
    } else {
        confluenceInput.value = ""
    }
});

userIdSubmit.onclick = function () {
    setUserId();
}

urlSubmit.onclick = function () {
    setUrl();
}

confluenceSubmit.onclick = function () {
    setConfluence();
}

userIdInput.addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        event.preventDefault();
        userIdSubmit.click();
    }
});

urlInput.addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        event.preventDefault();
        urlSubmit.click();
    }
});

confluenceInput.addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        event.preventDefault();
        confluenceSubmit.click();
    }
});

function setUserId() {
    const newUserId = userIdInput.value
    if (newUserId.length > 0) {
        chrome.storage.sync.set({userId: newUserId})
    } else {
        chrome.storage.sync.remove(["userId"])
    }
}


function setUrl() {
    const newUrl = urlInput.value
    if (newUrl.length > 0) {
        chrome.storage.sync.set({url: newUrl})
    } else {
        chrome.storage.sync.remove(["url"])
    }
}


function setConfluence() {
    const newConfluence = confluenceInput.value
    if (newConfluence.length > 0) {
        chrome.storage.sync.set({confluence: newConfluence})
    } else {
        chrome.storage.sync.remove(["confluence"])
    }
}
