function luckyDip() {

    var values = new Set();

    while (values.size < 6) {
        let randomBuffer = new Uint32Array(1);
        window.crypto.getRandomValues(randomBuffer);
        let randomNumber = randomBuffer[0] / (0xFFFFFFFF);
        let min = Math.ceil(1);
        let max = Math.floor(60);
        let value = Math.floor(randomNumber * (max - min + 1)) + min;
        values.add(value)
    }

    values = Array.from(values)

    for (let i = 0; i < 6; i++) {
        document.getElementById("no" + (i + 1)).value = values[i];
    }
}