// home.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->

    <template #content>
      <div class="row">
        <div class="col">
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Facilis sit
          eligendi assumenda aliquid vero iste, id animi repudiandae adipisci,
          ipsam facere illum tenetur cumque! Voluptatem placeat praesentium amet
          vel excepturi?
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";

export default {
  name: "PagesHome",
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Welcome to Handshake...",
    };
  },
  methods: {},
};
</script>
