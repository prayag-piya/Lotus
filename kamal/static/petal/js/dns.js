const { Client } = require('elasticsearch')
const client = new Client({ node: 'http://localhost:9200' })
let time = []
let labels = []
let data = {}
let dataset

for (i = 0; i <= 24; i++) {
    if (i < 10) {
        t = '0' + i
        labels.push(t + ":00")
    }
    else {
        labels.push(i + ":00")
    }
    data[i] = 0
}
key = Object.keys(data)
console.log(key);
const process = async (count, value) => {
    document.getElementById('totaldns').innerHTML = count;
    for (i = 0; i <= value['hits']['hits'].length - 1; i++) {
        time = value['hits']['hits'][i]['_source']['@timestamp'].split('T')[1].slice(0, 2)
        if (time > 9) {
            if (time in data) {
                data[time.slice(1, 2)] += 1
            }
        }
        else {
            if (time.slice(1, 2) in data) {
                data[time.slice(1, 2)] += 1
            }
        }
    }

    dataset = Object.values(data)
    console.log(dataset)
    var trace1 = {
        x: labels,
        y: dataset,
        type: 'scatter'
    };
    Plotly.newPlot('myChart', [trace1]);
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
    url = 'packetbeat-7.12.0-' + cYear + cMonth + cDay + ''
    return url
}
const domain = async (value) => {
    const results = await client.search({
        index: index(),
        body: {
            query: {
                match: { 'network.protocol': 'dns' }
            },
            'size': value
        }
    })
    process(value, results)
}

const hits = async () => {
    const result = await client.search({
        index: index(),
        body: {
            query: {
                match: { 'network.protocol': 'dns' }
            }
        }
    })
    domain(result['hits']['total']['value'])
}

hits()