<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col">UWNetID</th>
        <th scope="col">Added</th>
        <th scope="col">Reason</th>
        <th scope="col">&nbsp;</th>
      </tr>
    </thead>
    <tbody class="table-group-divider">
      <tr v-for="student in students" :key="student.id">
        <td>
          <div>
            <span>{{ student.username }}</span>
          </div>
        </td>
        <td>
          <div class="small text-muted">
            {{ formatDate(student.added_date) }}<br/>{{ student.added_by }}
          </div>
        </td>
        <td>
          <div class="small text-muted">
            {{ student.reason }}
          </div>
        </td>
        <td>
          <div>
            <a
              role="button"
              title="Unblock this student"
              class="btn btn-outline-dark-beige btn-sm rounded-pill px-3"
              v-on:click="saveDelete(student.id)"
            >Unblock student</a>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import dataMixin from "@/mixins/data_mixin.js";
import { formatDate } from "@/helpers/utils";

export default {
  mixins: [dataMixin],
  emits: ["studentUpdated"],
  props: {
    students: {
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
    saveDelete(studentId) {
      if (confirm("Unblock this student?")) {
        this.deleteBlockedStudent(studentId)
          .then(() => {
            this.$emit("studentUpdated");
          })
          .catch((error) => {
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
