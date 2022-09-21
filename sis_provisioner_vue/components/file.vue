<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50">Name</th>
        <th scope="col">&nbsp;</th>
        <th scope="col">Created</th>
        <th scope="col">Imported</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="(file, index) in files" :key="index">
        <td>
          <div>
            <span v-if="file.name == null" class=""></span>
            <span v-else>{{ file.name }}</span>
          </div>
        </td>
        <td class="align-middle">
          <a
            v-bind:href="file.download_url"
            title="Download file"
            class="btn btn-outline-dark-beige btn-sm rounded-pill px-3"
            >Download
          </a>
        </td>
        <td>
          <div class="small text-muted">
            {{ formatDate(file.created_date) }}
          </div>
        </td>
        <td>
          <div class="small text-muted">
            <span v-if="file.processed_date == null" class="">No</span>
            <span v-else>
              {{ formatDate(file.processed_date) }}
            </span>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { formatDate } from "../helpers/utils";

export default {
  name: "file",
  props: {
    files: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
    };
  },
  methods: {
    formatDate,
  },
};
</script>

<style lang="scss">
.table tbody {
  tr:last-of-type {
    border-color: transparent !important;
  }
}
</style>
