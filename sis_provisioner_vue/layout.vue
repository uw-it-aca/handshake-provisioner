<template>
  <!-- layout.vue: this is where you override the layout -->
  <axdd-sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="userName"
    :sign-out-url="signOutUrl"
  >
    <template #profile>
      <axdd-profile
        :user-netid="userName"
        :signout-url="signOutUrl"
      ></axdd-profile>
    </template>
    <template #navigation>
      <ul class="nav flex-column mb-5">
        <li class="nav-item mb-1">
          <router-link
            class="nav-link text-light bg-dark-purple-hover rounded me-1 px-2 py-1"
            active-class="bg-dark-purple"
            :to="'/surveys'"
            ><i class="bi bi-check-lg me-2"></i>Import Files</router-link
          >
        </li>
        <li class="nav-item mb-1">
          <router-link
            class="nav-link text-light bg-dark-purple-hover rounded me-1 px-2 py-1"
            active-class="bg-dark-purple"
            :to="'/gradebooks'"
            ><i class="bi bi-percent me-2"></i>Other...</router-link
          >
        </li>
      </ul>
    </template>
    <template #aside>
      <p class="text-light-gray bg-dark-purple rounded-3 p-3 small">
        Welcome to the Handshake Import tool!
        <br /><br />
        Browse files that have been imported to Handshake.
        <br /><br />
      </p>
    </template>
    <template #main>
      <!-- main section override -->
      <slot name="title">
        <h1 class="visually-hidden">{{ pageTitle }}</h1>
      </slot>

      <slot name="content"></slot>
    </template>
    <template #footer> </template>
  </axdd-sidebar>
</template>

<script>
import { Sidebar, Profile } from "axdd-components";

export default {
  components: {
    "axdd-sidebar": Sidebar,
    "axdd-profile": Profile,
  },
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "Handshake Imports",
      appRootUrl: "/",
      userName: document.body.getAttribute("data-user-name"),
      signOutUrl: document.body.getAttribute("data-signout-url"),

      // automatically set year
      currentYear: new Date().getFullYear(),
    };
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
