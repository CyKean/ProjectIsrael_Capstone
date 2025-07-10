import { createApp } from 'vue'
import App from './App.vue'
import router from './routes/index.js'
import './style.css'  // Make sure this import exists
import "toastr/build/toastr.min.css";
import { createVuetify } from 'vuetify';
import 'vuetify/styles'; 
import { createPinia } from 'pinia'

// createApp(App).use(router).mount('#app')
const vuetify = createVuetify();
const app = createApp(App);
app.use(createPinia())
app.use(router);
app.use(vuetify);
app.mount('#app');

if ('Notification' in window && Notification.permission !== 'granted') {
    Notification.requestPermission().then((permission) => {
      console.log('Notification permission:', permission)
    })
  }
  