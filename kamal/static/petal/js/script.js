var number;
var nData = {}
var byts = []
var labels = []
for (i = 0; i <= 24; i++) {
    if (i < 10) {
        t = '0' + i
        labels.push(t + ":00")
    }
    else {
        labels.push(i + ":00")
    }
    nData[i] = 0
}
const userProfile = async (url) => {
    try {
        const userInfo = await fetch(url)
        const data = await userInfo.json()
        return data
    }
    catch (err) {
        console.log('Error :(', err)
    }
}

function countPacket(data) {
    let count = document.getElementById('count');
    value = data['hits']['total']['value']
    count.innerHTML = value;
}

function hitselk(data) {
    rawData = data['hits']['hits']
    for (i = 0; i <= rawData.length - 1; i++) {
        time = rawData[i]['_source']['@timestamp'].split('T')[1]
        time = time.slice(0, 2)

        if (time > 9) {
            if (time in nData) {
                nData[time.slice(1, 2)] += 1
            }
        }
        else {
            if (time.slice(1, 2) in nData) {
                nData[time.slice(1, 2)] += 1
            }
        }
    }
    draw()
}

// function hitselk(data) {
//     rawData = data['hits']['hits']
//     for (var i = 0; i <= rawData.length - 1; i++) {
//         date = rawData[i]['_source']['@timestamp']
//         date = date.split('T')[0]
//         keys = Object.keys(nData)
//         console.log(date)
//         var byts = rawData[i]['_source']['network']['bytes']
//         if (byts == undefined) {
//             byts = 0
//         }
//         if (!(date in keys)) {
//             nData[date] = new Array()
//         }
//         nData[date].push(byts);
//         //console.log(nData)
//     }
//     draw()
// }
function sum(input) {

    if (toString.call(input) !== "[object Array]")
        return false;

    var total = 0;
    for (var i = 0; i < input.length; i++) {
        if (isNaN(input[i])) {
            continue;
        }
        total += Number(input[i]);
    }
    return total;
}


function draw() {
    console.log(byts)
    var data = Object.values(nData)

    var trace1 = [{
        x: labels,
        y: data,
        name: 'Traffic analysis',
        type: 'bar'
    }];
    var layout = {
        title: 'Traffic per day',
        backgroundColor: 'rgb(241, 119, 119)',
        yaxis: {
            range: [0, 100]
        },
        xaxis: {

        }
    };
    var myChart = document.getElementById('myChart')

    Plotly.newPlot(myChart, trace1, layout, { responsive: true, });

}

function index() {
    let currentDate = new Date();
    let cDay = currentDate.getDate()
    let cMonth = currentDate.getMonth() + 1
    let cYear = currentDate.getFullYear()
    if (cMonth < 10) {
        cMonth = '.0' + cMonth
    }
    else {
        cMonth = '.' + cMonth
    }
    if (cDay < 10) {
        cDay = '.0' + cDay
    }
    else {
        cDay = '.' + cDay
    }
    url = 'http://127.0.0.1:9200/packetbeat-7.12.0-' + cYear + cMonth + cDay + '/'
    return url
}

userProfile(index() + '_search')
    .then((data) => {
        number = data['hits']['total']['value']
        countPacket(data)
        return number
    })
    .then((data) => {
        let took = index() + '_search/?size=' + data
        userProfile(took)
            .then(data => { hitselk(data) })

    })










// function parsedata() {
//     alert('parsing');
//     fetch(url)
//         .then(response => response.json())
//         .then(data => countPacket(data));
//     setTimeout(parsedata, 30000);
// }

// let timerId = setTimeout(parsedata(), 2000);