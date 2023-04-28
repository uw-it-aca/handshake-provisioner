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
      <NavMenu />
    </template>
    <template #aside>
      <NavMessage />
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
import NavMenu from "./components/nav-menu.vue";
import NavMessage from "./components/nav-message.vue";

export default {
  components: {
    NavMenu,
    NavMessage
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
