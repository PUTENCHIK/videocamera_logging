const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],

    data() {
        return {
            snapshots: [],
            loading: false,
            objectBboxHoverId: 0,
            default_color: {r: 128, g: 128, b: 128},
            objects_styles: {}
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

        handlerObjectIconMouseover(id, color) {
            this.objectBboxHoverId = id;
            let color_str = `${color.r}, ${color.g}, ${color.b}`;
            document.documentElement.style.setProperty('--color-bbox-hover', `rgba(${color_str}, 0.2)`);
        },

        handlerObjectIconMouseleave() {
            this.objectBboxHoverId = 0;
        },

        getSnapshotImageSizes(id) {
            
            console.log(img_snapshot);
            
            if (img_snapshot === undefined) {
                return {
                    width: 640,
                    height: 480,
                }
            } else {
                return {
                    width: img_snapshot[0].width,
                    height: img_snapshot[0].height,
                } 
            }
        },

        onSnapshotImageLoaded(snapshot) {
            let img_snapshot = this.$refs['snapshot_' + snapshot.id][0];
            snapshot.objects.forEach((object) => {
                let color;
                if (object.trackable_class !== null) {
                    color = object.trackable_class.color;
                } else {
                    color = this.default_color;
                }
                let color_str = `${color.r}, ${color.g}, ${color.b}`;
                let sizes = {
                    width: img_snapshot.width,
                    height: img_snapshot.height,
                }
                
                this.objects_styles[object.id] = {
                    'width': `${(object.bbox.x2-object.bbox.x1) * sizes.width}px`,
                    'height': `${(object.bbox.y2-object.bbox.y1) * sizes.height}px`,
                    'top': `${(object.bbox.y1) * sizes.height}px`,
                    'left': `${(object.bbox.x1) * sizes.width}px`,
                    'border-color': `rgb(${color_str})`,
                }
            });
        },
    },

    mounted() {
        this.loading = true;
        this.loadSnapshots();
        this.loading = false;
    }

}).mount("#app");