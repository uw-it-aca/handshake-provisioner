<template>
  <!-- layout.vue: this is where you override the layout -->
  <axdd-sidebar
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="contextStore.context.userName"
    :sign-out-url="contextStore.context.signOutUrl"
  >
    <template #profile>
      <axdd-profile
        :user-netid="contextStore.context.userName"
        :signout-url="contextStore.context.signOutUrl"
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
import NavMenu from "@/components/nav-menu.vue";
import NavMessage from "@/components/nav-message.vue";
import { useContextStore } from "@/stores/context";

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
  setup() {
    const contextStore = useContextStore();

    return {
      contextStore,
    };
  },
  data() {
    return {
      appName: "Handshake Imports",
      appRootUrl: "/",
    };
  },
  computed: {
    currentYear() {
      return new Date().getFullYear();
    },
  },
  created: function () {
    // constructs page title in the following format "Page Title - AppName"
    document.title = this.pageTitle + " - " + this.appName;
  },
};
</script>
