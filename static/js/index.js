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
            }).then(function (r) {
                app.vue.keows.push({
                    id: r.data.id,
                    keow_content: self.keow,
                });
                self.keow = "";
            });
        
        },
    }
};

app.vue = Vue.createApp(app.data).mount("#app");

app.load_data = function () {
    axios.get(get_keows_url).then(function (r) {
        app.vue.keows = r.data.keows;
    });
}

app.load_data();

