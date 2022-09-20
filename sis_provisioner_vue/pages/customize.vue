// about.vue

<template>
  <layout :page-title="pageTitle">
    <!-- page content -->
    <template #content>
      <div class="row">
        <div class="col">
          Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tempora
          magni ex a repudiandae ab error nam quaerat? Hic, natus. Facilis
          pariatur consectetur veniam sunt odio officiis vero expedita debitis
          ad.
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import Layout from "../layout.vue";

export default {
  name: "PagesCustomize",
  components: {
    layout: Layout,
  },
  data() {
    return {
      pageTitle: "Customizing your app",
    };
  },
  methods: {},
};
</script>
