<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col">Name</th>
        <th scope="col">Created</th>
        <th scope="col">CSV Generated</th>
        <th scope="col">Imported</th>
        <th scope="col">&nbsp;</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="file in files" :key="file.id">
        <td>
          <div>
            <span>{{ file.name }}</span>
            <span v-if="file.generated_date != null" class="">&nbsp;
              <a
                role="button"
                :href="file.api_path"
                title="Download this file"
                class="btn btn-outline-dark-beige btn-sm rounded-circle"
              ><i class="bi bi-download"></i></a>
            </span>
          </div>
        </td>
        <td>
          <div class="small text-muted">
            {{ formatDate(file.created_date) }}<br/>
            {{ file.created_by }}
          </div>
        </td>
        <td>
          <div class="small text-muted">
            <span v-if="file.generated_date == null" class="">
              <span v-if="file.process_id == null" class="">
                <i>Waiting for job to start</i>
              </span>
              <span v-else>
                <i>Job in progress</i>
              </span>
            </span>
            <span v-else>
              {{ formatDate(file.generated_date) }}
            </span>
          </div>
        </td>
        <td>
          <div class="small text-muted">
            <span v-if="file.imported_date == null" class="">
              <span v-if="file.generated_date != null" class="">
                <a
                  title="Import this file to Handshake"
                  class="btn btn-outline-dark-beige btn-sm rounded-pill px-3"
                  v-on:click="saveImport(file.id)"
                >Import to Handshake</a>
              </span>
            </span>
            <span v-else>
              {{ formatDate(file.imported_date) }}
            </span>
          </div>
        </td>
        <td>
          <div>
            <a
              role="button"
              title="Delete this file"
              class="btn btn-outline-dark-beige btn-sm rounded-circle"
              v-on:click="saveDelete(file.id)"
            ><i class="bi bi-trash-fill"></i></a>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import { importFile, deleteFile } from "@/utils/data";
import { formatDate } from "@/utils/date";

export default {
  emits: ["fileUpdated"],
  props: {
    files: {
      type: Array,
      required: true,
    },
  },
  setup() {
    return {
      importFile,
      deleteFile,
      formatDate,
    };
  },
  data() {
    return {
    };
  },
  methods: {
    saveImport(fileId) {
      this.importFile(fileId)
        .then((data) => {
          this.$emit("fileUpdated");
        })
        .catch((error) => {
          console.log(error);
        });
    },
    saveDelete(fileId) {
      if (confirm("Delete this file? This action is permanent.")) {
        this.deleteFile(fileId)
          .then((data) => {
            this.$emit("fileUpdated");
          })
          .catch((error) => {
            console.log(error);
          });
      }
    },
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
