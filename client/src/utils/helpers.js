function format(number) {
    return String(number).padStart(2, '0');
}

export function formatDate(date) {
    let d = new Date(date);
    return `${format(d.getDate())}.${format(d.getMonth()+1)}.${d.getFullYear()} ${format(d.getHours())}:${format(d.getMinutes())}:${format(d.getSeconds())}`;
}

export function getFormData(event) {
    let data = new FormData(event.target);
    return Object.fromEntries(data);
}

export function cloneObject(obj) {
    return JSON.parse(JSON.stringify(obj));
}

export function getColor(color) {
    return `#${format(color.r.toString(16))}${format(color.g.toString(16))}${format(color.b.toString(16))}`.toUpperCase();
}