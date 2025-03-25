const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],

    data() {
        return {
            snapshots: [],
            colors: {},
            loading: false,
            objectBboxHoverId: 0,
        }
    },

    methods: {
        loadSnapshots() {
            fetch("/api/snapshots", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
                .then(r => r.json())
                .then((r) => {
                    this.snapshots = r;
                    this.formatDates();
                });
        },

        formatDates() {
            this.snapshots.forEach((snapshot) => {
                snapshot.created_at = formatDate(snapshot.created_at);
            });
        },

        generateObjectsBoxes(object) {
            let c = object.trackable_class.id - 1;
            let color = `${this.colors[c][0]}, ${this.colors[c][1]}, ${this.colors[c][2]}`;
            return {
                'width': `${object.bbox.x2-object.bbox.x1}px`,
                'height': `${object.bbox.y2-object.bbox.y1}px`,
                'top': `${object.bbox.y1}px`,
                'left': `${object.bbox.x1}px`,
                'border-color': `rgb(${color})`,
            }
        },

        loadClassColors() {
            fetch("/api/class_colors", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
                .then(r => r.json())
                .then((r) => {
                    this.colors = r;
                });
        },

        handlerObjectIconMouseover(id, class_id) {
            this.objectBboxHoverId = id;
            let c = class_id - 1;
            let color = `${this.colors[c][0]}, ${this.colors[c][1]}, ${this.colors[c][2]}`;
            document.documentElement.style.setProperty('--color-bbox-hover', `rgba(${color}, 0.2)`);
        },

        handlerObjectIconMouseleave() {
            this.objectBboxHoverId = 0;
        },
    },

    mounted() {
        this.loading = true;
        this.loadSnapshots();
        this.loadClassColors();
        this.loading = false;
    }

}).mount("#app");