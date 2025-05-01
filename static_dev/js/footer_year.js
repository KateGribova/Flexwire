let dateField = document.getElementById('date');
let nowDate = new Date();

let serverTime = Date.parse('{% now "Y-m-d G:i:s" %}');
let clientTime = nowDate.getTime();

if (Math.abs(clientTime - serverTime) < 24 * 60 * 60 * 1000) {
    dateField.innerHTML = nowDate.getFullYear().toString();
}
