<template>
  <div class="container-xl">
    <div class="px-3">
      <header
        class="d-flex justify-content-between align-items-center pb-3 my-4 border-bottom"
      >
        <div class="h4 flex-fill">
          <i class="bi bi-cup-straw me-1 text-purple"></i>
          <a href="/" class="text-reset text-decoration-none">{{ appName }}</a>
        </div>
      </header>

      <main>
        <h1 class="">{{ pageTitle }}</h1>
        <slot name="content" />
      </main>

      <footer class="pt-2 mt-5 mb-3 text-muted border-top">
        Copyright &copy; {{ new Date().getFullYear() }} University of Washington
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: "LayoutComp",
  components: {},
  props: {
    pageTitle: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      // minimum application setup overrides
      appName: "Handshake Provisioner",
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
