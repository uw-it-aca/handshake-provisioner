<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#createBlockedStudentModal'"
    class="btn text-nowrap btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2"
    @click="getFormData()"
  >
    <slot></slot>
  </a>

  <!-- create blocked student modal -->
  <div
    ref="createBlockedStudentModal"
    class="modal fade text-start"
    :id="'createBlockedStudentModal'"
    tabindex="-1"
    aria-labelledby="createBlockedStudentModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="createBlockedStudentModalLabel">
            Add a blocked student
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-if="student">
          <div class="row">
            <div class="col">
              <label for="student-uwetid" class="form-label">UWNetID:</label>
              &nbsp;&nbsp;
              <input
                type="text"
                id="student-uwetid"
                name="username"
                size="10"
                v-model="student.username"
              />&nbsp;
            </div>
          </div>
          <div class="row">
            <div class="col">
              <label for="student-reason" class="form-label">Reason for block:</label>
              &nbsp;&nbsp;
              <input
                type="text"
                id="student-reason"
                name="reason"
                size="50"
                v-model="student.reason"
              />&nbsp;
            </div>
          </div>
        </div>
        <div class="modal-footer text-end">
          <div>
            <button
              type="button"
              class="btn btn-secondary me-2"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="saveStudent()"
            >
              Add student to blocked list
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import dataMixin from "../mixins/data_mixin.js";
import { Modal } from "bootstrap";

export default {
  mixins: [dataMixin],
  emits: ["studentUpdated"],
  props: {},
  data() {
    return {
      student: this.getDefaultStudent(),
      formErrors: {},
    };
  },
  methods: {
    getDefaultStudent() {
      return {
        username: "",
        reason: "",
      };
    },
    saveStudent() {
      var studentCreateModal = Modal.getInstance(
        document.getElementById("createBlockedStudentModal")
      );
      this.createBlockedStudent(this.student)
        .then(() => {
          this.$emit("studentUpdated");
          studentCreateModal.hide();
        })
        .catch((error) => {
          this.formErrors = error.response.data;
        });
    },
  },
  clearFormErrors() {
    this.formErrors = {};
  },
  resetForm() {
    this.clearFormErrors();
  },
};
</script>
