<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#createFileModal'"
    class="btn text-nowrap btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2"
  >
    <slot></slot>
  </a>

  <!-- create file modal -->
  <div
    ref="createFileModal"
    class="modal fade text-start"
    :id="'createFileModal'"
    tabindex="-1"
    aria-labelledby="createFileModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="createFileModalLabel">Create a Handshake Import File</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body" v-if="file">
          <div class="row">
            <div class="col">
              <label class="form-label">Select the enrollment term:</label>
              &nbsp;&nbsp;
              <input
                type="radio"
                id="academic-term-current"
                name="academic_term"
                value="current"
                v-model="file.academic_term"
              />&nbsp;
              <label for="academic-term-current" class="form-label">
                {{ term.current }}
              </label>&nbsp;&nbsp;
              <input
                type="radio"
                id="academic-term-next"
                name="academic_term"
                value="next"
                v-model="file.academic_term"
              />&nbsp;
              <label for="academic-term-next" class="form-label">
                {{ term.next }}
              </label><br />
            </div>
          </div>
          <div class="row">
            <div class="col">
              <label class="form-label">
                Is this a <strong>TEST</strong> file?
              </label>&nbsp;&nbsp;
              <input
                type="checkbox"
                id="is-test-file"
                name="is_test_file"
                v-model="file.is_test_file"
              />&nbsp;
              <label for="is-test-file" class="form-label">Yes</label>
              <br />
            </div>
          </div>
        </div>
        <div class="modal-footer text-end">
          <div>
            <button
              type="button"
              class="btn btn-secondary me-2"
              data-bs-dismiss="modal"
            >Close
            </button>
            <button type="button" class="btn btn-primary" @click="saveFile()">
              Create file
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
  emits: ["fileUpdated"],
  props: {},
  data() {
    return {
      term: {
        current: window.handshake.current_term,
        next: window.handshake.next_term
      },
      file: this.getDefaultFile(),
      formErrors: {},
    };
  },
  methods: {
    getDefaultFile() {
      return {
        academic_term: "next",
        is_test_file: true,
      };
    },
    saveFile() {
      var fileCreateModal = Modal.getInstance(
        document.getElementById("createFileModal")
      );
      this.createFile(this.file)
        .then(() => {
          this.$emit("fileUpdated");
          fileCreateModal.hide();
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
