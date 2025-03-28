function format(number) {
    return String(number).padStart(2, '0');
}

function formatDate(date) {
    let d = new Date(date);
    return `${d.getFullYear()}-${format(d.getMonth()+1)}-${format(d.getDate())} ${format(d.getHours())}:${format(d.getMinutes())}:${format(d.getSeconds())}`;
}

function clone_object(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function get_color(color) {
    return `#${format(color.r.toString(16))}${format(color.g.toString(16))}${format(color.b.toString(16))}`.toUpperCase();
}