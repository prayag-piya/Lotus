var whitelist = document.getElementsByClassName('whitelist')
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getToken('csrftoken');
for (var i = 0; i < whitelist.length; i++) {
    whitelist[i].addEventListener('click', function () {
        var domain = this.dataset.action;
        var url = '/rules/'
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'name': domain })
        })
            .then(response => {
                location.reload();
                return response.json();
            })


    })
}

function reload() {
    location.reload()
}