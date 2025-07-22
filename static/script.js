import home from './components/home.js'
import login from './components/login.js'
import register from './components/register.js'
import navbar from './components/navbar.js'
import footer from './components/footer.js'

const routes = [
    {path: '/', component: home},
    {path: '/login', component: login},
    {path: '/register', component: register},
]

const router = new VueRouter({
    routes // route : route

})

const app = new Vue({
    el: "#app",
    router, // router : router
    template: `
    <div class="container">
        <nav-bar></nav-bar>
        <router-view></router-view>
        <foot></foot>
    </div>
    `,
    data: {
        section: "frontend",
    },
    components: {
        'nav-bar': navbar,
        'foot': footer
    }
})