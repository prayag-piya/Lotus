let url = 'http://127.0.0.1:8000/api/packet/packetview/'
function countPacket(data) {
    let count = document.getElementById('count');
    count.innerHTML = data.length;
}

// function parsedata() {
//     alert('parsing');
//     fetch(url)
//         .then(response => response.json())
//         .then(data => countPacket(data));
//     setTimeout(parsedata, 30000);
// }

// let timerId = setTimeout(parsedata(), 2000);

fetch(url)
    .then(response => response.json())
    .then(data => countPacket(data));



