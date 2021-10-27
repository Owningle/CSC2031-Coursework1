window.onload = function() {
    var lastKey = null
    var prevLen = 0

    const phone = document.getElementById('phone');

    phone.setAttribute('maxLength', 13)

    phone.addEventListener("input", (e) => {
        var number = e.target.value.replaceAll('-', '')

        cursorPos = e.target.selectionStart

        if (number.length > 4) {
            number = number.slice(0, 4) + '-' + number.slice(4)
        }
        if (number.length > 8) {
            number = number.slice(0, 8) + '-' + number.slice(8)
        }

        phone.value = number

        if (e.target.value.length - prevLen > 1) cursorPos++
        e.target.setSelectionRange(cursorPos, cursorPos);

        prevLen = e.target.value.length
    })

    phone.addEventListener("keydown", (e) => {
        lastKey = e.key
    })
}