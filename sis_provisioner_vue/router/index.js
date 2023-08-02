import { createWebHistory, createRouter } from "vue-router";
import { trackRouter } from "vue-gtag-next";

// page components
import ImportFiles from "@/pages/import-files.vue";
import BlockedStudents from "@/pages/blocked-students.vue";

const routes = [
  {
    path: "/",
    component: ImportFiles,
    pathToRegexpOptions: { strict: true },
    props: true,
  },
  {
    path: "/blocked-students",
    component: BlockedStudents,
    pathToRegexpOptions: { strict: true },
    props: true,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// vue-gtag-next router tracking
trackRouter(router);

export default router;
