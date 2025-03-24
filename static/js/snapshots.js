const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],

    data() {
        return {
            snapshots: [],
            loading: false
        }
    },

    methods: {
        loadSnapshots() {
            this.loading = true;
            fetch("/api/snapshots", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                }
            })
                .then(r => r.json())
                .then((r) => {
                    this.snapshots = r;
                    console.log(this.snapshots);                    
                    this.formatDates();
                });
            this.loading = false;
        },

        formatDates() {
            this.snapshots.forEach((snapshot) => {
                snapshot.created_at = formatDate(snapshot.created_at);
            });
        },
    },

    mounted() {
        this.loadSnapshots();
    }

}).mount("#app");