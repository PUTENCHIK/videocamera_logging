function format(number) {
    return String(number).padStart(2, '0');
}

export function formatDate(date) {
    if (typeof(date) == 'string' && !date.includes('T')) {
        return date;
    }
    let d = new Date(date);
    if (isNaN(d))
        return date.toString();
    return `${format(d.getDate())}.${format(d.getMonth()+1)}.${d.getFullYear()} ${format(d.getHours())}:${format(d.getMinutes())}:${format(d.getSeconds())}`;
}

export function getFormData(event) {
    let data = new FormData(event.target);
    return Object.fromEntries(data);
}

export function cloneObject(obj) {
    return JSON.parse(JSON.stringify(obj));
}

export function colorToHex(color) {
    return `#${format(color.r.toString(16))}${format(color.g.toString(16))}${format(color.b.toString(16))}`.toUpperCase();
}

export function colorToString(color) {
    return `${color.r}, ${color.g}, ${color.b}`;
}

export function getClassColor(object) {
    if (object.trackable_class !== null) {
        return object.trackable_class.color;
    } else {
        return {r: 128, g: 128, b: 128};
    }
}

export function firstToUpperCase(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}