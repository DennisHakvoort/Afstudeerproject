var baseUrl
var userId
var confluenceUrl
var maxBodyLength = 150
// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

chrome.storage.sync.get(['userId', 'url', 'confluence'], function (result) {
    if (result.userId !== undefined) {
        userId = result.userId
    } else {
        display_incorrect_configuration_message()
    }

    if (result.url !== undefined) {
        baseUrl = result.url
    } else {
        display_incorrect_configuration_message()
    }

    if (result.confluence !== undefined) {
        confluenceUrl = result.confluence
    } else {
        display_incorrect_configuration_message()
    }
});

document.getElementById('settings-button').onclick = function () {
    window.location.href = "settings.html";
}

document.getElementById('search-button').onclick = function () {
    search();
}

document.getElementById("search-input").addEventListener("keyup", function (event) {
    // Number 13 is the "Enter" key on the keyboard
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("search-button").click();
    }
});


// Open a new connection, using the GET request on the URL endpoint
function search() {
    const searchInput = document.getElementById("search-input")
    const searchQuery = searchInput.value
    searchInput.value = ""

    request.open('POST', baseUrl + "/search/")
    request.setRequestHeader("Content-Type", "application/json");

    request.onload = function () {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response)


        if (request.status === 200) {
            display_search_results(data)
        } else {
            display_error_message(request.status, request.statusText)
        }
    }

    request.send(JSON.stringify({
        "query": searchQuery,
        "user_id": userId
    }));
}

function display_error_message(errorTitle, errorText) {
    const content = document.getElementById('content')
    const resultContainer = document.createElement('div')
    resultContainer.setAttribute('class', 'error')
    content.appendChild(resultContainer)

    const error = document.createElement('h1')
    error.textContent = errorTitle
    resultContainer.appendChild(error)

    const message = document.createElement('p')
    message.textContent = errorText
    resultContainer.appendChild(message)
}

function display_incorrect_configuration_message() {
    display_error_message("Configuratie niet compleet", "Vul alstublieft de configuratie aan in de instellingen.")
}

function display_search_results(results) {
    const content = document.getElementById('content')
    // remove children
    while (content.firstChild) {
        content.removeChild(content.lastChild);
    }
    if (results.length === 0) {
        display_error_message("No documents found")
        return
    }
    results.forEach((result) => {
        const resultContainer = document.createElement('a')
        resultContainer.setAttribute('class', 'search-result')
        resultContainer.setAttribute('href', confluenceUrl + "/pages/viewpage.action?pageId=" + result.document_id)
        resultContainer.setAttribute("target", "_blank")
        content.appendChild(resultContainer)

        const title = document.createElement('h1')
        title.textContent = result.title_raw
        resultContainer.appendChild(title)

        const description = document.createElement('p')
        description.setAttribute('class', 'description')
        let documentBody = result.body_raw
        description.setAttribute('title', documentBody)
        if (documentBody.length > maxBodyLength)
            documentBody = documentBody.substring(0, maxBodyLength) + "..."
        description.textContent = documentBody
        resultContainer.appendChild(description)

        const space = document.createElement('p')
        space.setAttribute('class', 'space')
        space.textContent = result.space
        resultContainer.appendChild(space)
    })
}