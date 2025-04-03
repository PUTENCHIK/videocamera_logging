function format(number) {
    return String(number).padStart(2, '0');
}

export function formatDate(date) {
    let d = new Date(date);
    return `${d.getFullYear()}-${format(d.getMonth()+1)}-${format(d.getDate())} ${format(d.getHours())}:${format(d.getMinutes())}:${format(d.getSeconds())}`;
}

export function getFormData(event) {
    let data = new FormData(event.target);
    return Object.fromEntries(data);
}

export function cloneObject(obj) {
    return JSON.parse(JSON.stringify(obj));
}