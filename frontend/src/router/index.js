import { createWebHistory, createRouter } from "vue-router";

const routes = [
    {
        path: "/",
        name: "welcome",
        component: () => import("@/views/Welcome.vue"),
    },

    {
        path: "/chat",
        name: "chat",
        component: () => import("@/views/Chat.vue"),
    },
];

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes,
});

export default router;