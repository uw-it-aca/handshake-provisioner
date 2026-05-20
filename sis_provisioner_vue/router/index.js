import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import HandshakeFiles from "@/pages/handshake-files.vue";
import UconnectFiles from "@/pages/uconnect-files.vue";
import HandshakeBlockedStudents from "@/pages/handshake-blocked-students.vue";
import UconnectBlockedStudents from "@/pages/uconnect-blocked-students.vue";

const routes = [
  {
    path: "/",
    component: HandshakeFiles,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/uconnect-files",
    component: UconnectFiles,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/handshake-blocked-students",
    component: HandshakeBlockedStudents,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/uconnect-blocked-students",
    component: UconnectBlockedStudents,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// vue-gtag-next router tracking
trackRouter(router);

export default router;
