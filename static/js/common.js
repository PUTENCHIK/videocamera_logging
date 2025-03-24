function formatDate(date) {
    function format(number) {
        return String(number).padStart(2, '0');
    }

    let d = new Date(date);
    return `${d.getFullYear()}-${format(d.getMonth()+1)}-${format(d.getDate())} 
            ${format(d.getHours())}:${format(d.getMinutes())}:${format(d.getSeconds())}`;
}