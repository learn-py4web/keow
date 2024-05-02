"use strict";

// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


app.data = {    
    data: function() {
        return {
            // Complete as you see fit.
            keows: [],
            keow: "",
        }
    },
    methods: {
        // Complete as you see fit.
        add_keow: function () {
            let self = this;
            axios.post(add_keow_url, {
                keow_content: this.keow,
                thumb: 0,
            }).then(function (r) {
                app.vue.keows.push({
                    id: r.data.id,
                    keow_content: self.keow,
                    thumb: 0,
                });
                self.keow = "";
            });
        },
        // Thumbs code. 
        thumb_set: function (keow_idx, thumb) {
            let keow = app.vue.keows[keow_idx];
            keow.thumb = thumb;
            axios.post(set_thumb_url, {keow_id: keow.id, thumb: thumb}).then(
                function (r) {
                    keow.total = r.data.total;
                }   
            );
        },
        thumb_out: function (keow_idx) {
            let keow = app.vue.keows[keow_idx];
            keow.thumb_display = keow.thumb;
        },
        thumb_over: function (keow_idx, thumb) {
            let keow = app.vue.keows[keow_idx];
            keow.thumb_display = thumb;
        },
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    axios.get(get_keows_url).then(function (r) {
        let ks = r.data.keows;
        for (let k of ks) {
            k.thumb_display = k.thumb;
        }
        app.vue.keows = ks;
    });
}

app.load_data();

