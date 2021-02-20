const { Client } = require('elasticsearch')
const client = new Client({ node: 'http://localhost:9200' })
let time = []
let labels = []
let data = {}
let dataset
const process = async (count, value) => {
    document.getElementById('totaldns').innerHTML = count;
    for (var i = 0; i <= value['hits']['hits'].length - 1; i++) {
        console.log(value['hits']['hits'][i]['_source']['@timestamp'])
        let timestamp = value['hits']['hits'][i]['_source']['@timestamp'].split('T')
        time.push(timestamp[1])
        if (i <= 24) {
            labels.push('' + i + '' + ':00')
            data[i] = 0
        }
    }
    var key = Object.keys(data)
    for (var i = 0; i <= time.length - 1; i++) {
        var t = time[i].slice(0, 2)
        if (t in key) {
            data[t] += 1
        }
    }
    dataset = Object.values(data)
    console.log(data)

    var ctx = document.getElementById('myChart');
    let chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "Past 24 DNS request",
                borderColor: 'rgb(127, 99, 132)',
                data: dataset
            }]
        },
        options: {
        }
    });
}

const domain = async (value) => {
    const results = await client.search({
        index: 'packetbeat-7.10.2-2021.01.25-000001',
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
        index: 'packetbeat-7.10.2-2021.01.25-000001',
        body: {
            query: {
                match: { 'network.protocol': 'dns' }
            }
        }
    })
    domain(result['hits']['total']['value'])
}

hits()

