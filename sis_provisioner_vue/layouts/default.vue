<!-- eslint-disable vue/no-v-html -->
<template>
  <!-- layout.vue: this is where you override the layout -->
  <STopbarNeo
    :app-name="appName"
    :app-root-url="appRootUrl"
    :page-title="pageTitle"
    :user-name="context.userName"
    :sign-out-url="context.signOutUrl"
    :background-class="'bg-body'"
  >
    <template #settings>
      <SProfile :user-netid="context.userName">
        <a :href="context.signOutUrl" class="text-white"> Sign out </a>
      </SProfile>
      <SColorMode color-class="text-white" class="ms-2" />
    </template>
    <template #navigation>
      <ul class="navbar-nav my-xl-0 my-2 me-auto text-white">
        <li class="nav-item me-5">
          <router-link
            :to="'/'"
            active-class="active"
            class="nav-link px-0 text-white"
            ><i class="bi bi-file-text-fill me-2"></i>Handshake
            files</router-link
          >
        </li>
        <li class="nav-item me-5">
          <router-link
            :to="'/handshake-blocked-students'"
            active-class="active"
            class="nav-link px-0 text-white"
            ><i class="bi bi-people-fill me-2"></i>Handshake blocked
            students</router-link
          >
        </li>
        <li class="nav-item me-5">
          <router-link
            :to="'/uconnect-files'"
            active-class="active"
            class="nav-link px-0 text-white"
            ><i class="bi bi-file-text-fill me-2"></i>uConnect
            files</router-link
          >
        </li>
        <li class="nav-item me-5">
          <router-link
            :to="'/uconnect-blocked-students'"
            active-class="active"
            class="nav-link px-0 text-white"
            ><i class="bi bi-people-fill me-2"></i>uConnect blocked
            students</router-link
          >
        </li>
      </ul>
    </template>

    <template #main>
      <div class="row my-5">
        <div class="col">
          <slot name="content"></slot>
        </div>
      </div>
    </template>
    <template #footer></template>
  </STopbarNeo>
</template>

<script>
  import { useContextStore } from "@/stores/context";
  import { BLink, BButton } from "bootstrap-vue-next";
  import { STopbarNeo, SProfile, SColorMode } from "solstice-vue";

  export default {
    name: "HandshakeApp",
    components: {
      BLink,
      BButton,
      STopbarNeo,
      SProfile,
      SColorMode,
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
        appName: "Handshake & uConnect Imports",
        appRootUrl: "/",
      };
    },
    computed: {
      context() {
        return this.contextStore.context;
      },
    },
    created: function () {
      // constructs page title in the following format "Page Title - AppName"
      document.title = this.pageTitle + " - " + this.appName;
    },
    methods: {},
  };
</script>

<style lang="scss" scoped>
  .chevron .bi-chevron-right {
    display: inline-block;
    transition: transform 0.35s ease;
    transform-origin: 0.5em 50%;
    font-weight: bolder;
  }

  .chevron[aria-expanded="true"] .bi-chevron-right {
    transform: rotate(90deg);
  }

  .bi-chevron-right::after {
    font-weight: bolder !important;
  }
</style>
