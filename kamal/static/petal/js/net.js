const { Client } = require('elasticsearch')
const client = new Client({ node: 'http://localhost:9200' })
var label = []
for (i = 0; i <= 24; i++) {
    label.push(i)
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
async function processing(value) {
    const result = await client.search({
        index: index(),
        body: {
            query: {
                multi_match: {
                    query: "192.168.0.102",
                    fields: ['destination.ip', 'source.ip']
                }
            },
            size: value
        }
    })
    return result['hits']['hits']
}
async function threadingThress() {
    //now using elasticsearch module filter every thing
    const results = await client.search({
        index: index(),
        body: {
            query: {
                multi_match: {
                    query: "192.168.0.102",
                    fields: ['destination.ip', 'source.ip']
                }
            },
            size: 0
        }
    })
    return results['hits']['total']['value']
}
plotingdata = {}
class thresshold {
    HITS = 0
    constructor() {
        this.parser()
        console.log('COnstructor executed')
    }
    parser() {
        console.log('Parser excuted')
        var hit = threadingThress()
        if (hit !== this.HITS) {
            console.log('Parser excuted')
            var reqpacket = processing(hit)
            for (i = 0; i <= reqpacket.length - 1; i++) {
                console.log(reqpacket[i]['_source'])
            }
        }
    }
}
var thress = new thresshold()