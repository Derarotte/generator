import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/generate/:moduleId',
        name: 'Generate',
        component: () => import('../views/Generate.vue')
    }
]

export default createRouter({
    history: createWebHistory(),
    routes
})
