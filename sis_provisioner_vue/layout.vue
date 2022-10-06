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
    <template #aside>
      <p class="text-light-gray bg-dark-purple rounded-3 p-3 small">
        Welcome to the Handshake Import tool! On this page, you can browse files
        that have been imported to Handshake.
        <br /><br />
        To import a new file:
        <br/><br/>
        <ol>
          <li>Click &quot;Create new file&quot;, and select the enrollment term.</li>
          <br/>
          <li>The &quot;CSV Generated&quot; column indicates the status of the
          file-creation process</li>
          <br/>
          <li>Once created, click &quot;Import to Handshake&quot; to import the file.</li>
        </ol>
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
