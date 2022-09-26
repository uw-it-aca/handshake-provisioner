<template>
  <a
    role="button"
    data-bs-toggle="modal"
    :data-bs-target="'#createFileModal'"
    class="btn text-nowrap btn-sm btn-outline-gray text-dark rounded-3 px-3 py-2"
    @click="getFormData()"
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
          <h5 class="modal-title" id="createFileModalLabel">Create a file</h5>
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
              <label class="form-label">Choose the term:</label>
              <input
                type="radio"
                id="academic-term-current"
                name="academic_term"
                value="current"
                v-model="file.academic_term"
              /><br/><br/>
              <label for="academic-term-current" class="form-label"
                > Current term (...)</label
              >
              <input
                type="radio"
                id="academic-term-next"
                name="academic_term"
                value="next"
                v-model="file.academic_term"
              />
              <label for="academic-term-next" class="form-label"
                > Next term (...)</label
              ><br />
            </div>
          </div>
          <div class="row">
            <div class="col">
              <input
                type="checkbox"
                id="is-test-file"
                name="is_test_file"
                value="true"
                v-model="file.is_test_file"
              />
              <label for="is-test-file" class="form-label"
                > This is a <strong>TEST</strong> file.</label
              ><br />
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
            <button type="button" class="btn btn-primary" @click="createFile()">
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
  emits: ["fileCreated"],
  props: {},
  data() {
    return {
      file: this.getDefaultFile(),
      formErrors: {},
    };
  },
  methods: {
    getDefaultFile() {
      return {
        academic_term: "next",
        is_test_file: "true",
      };
    },
    createFile() {
      var fileCreateModal = Modal.getInstance(
        document.getElementById("createFileModal")
      );
      this.saveFile(this.file.academic_term, this.file.is_test_file)
        .then(() => {
          this.$emit("fileCreated");
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
