<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2" class="my-2"
                >Import Files</axdd-card-heading
              >
              <axdd-card-action>

                <CreateFile @fileUpdated="getFileList()"
                  ><i class="bi bi-plus-square text-dark me-2"></i>Create new
                  file</CreateFile
                >


              </axdd-card-action>
            </template>
            <template #body>
              <axdd-tabs-display :tabs-id="'files'">
                <template #panels>
                  <table-loading v-if="isLoading"></table-loading>
                  <div v-if="fileData && fileData.length">
                    <file :files="fileData" />
                  </div>
                  <div v-else>No data</div>
                </template>
              </axdd-tabs-display>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </layout>
</template>

<script>
import dataMixin from "../mixins/data_mixin.js";
import {
  Card,
  CardHeading,
  CardAction,
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";
import Layout from "../layout.vue";
import ImportFile from "../components/file.vue";
import TableLoading from "../components/table-loading.vue";
import CreateFile from "../components/create-file.vue";

export default {
  mixins: [dataMixin],
  components: {
    layout: Layout,
    file: ImportFile,
    CreateFile,
    "table-loading": TableLoading,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
    "axdd-tabs-list": TabsList,
    "axdd-tabs-display": TabsDisplay,
    "axdd-tabs-item": TabsItem,
    "axdd-tabs-panel": TabsPanel,
  },
  data() {
    return {
      pageTitle: "Import Files",
      fileData: [],
      isLoading: true,
    };
  },
  methods: {
    getFileList() {
      this.getFiles()
        .then((response) => response.json())
        .then((data) => {
          this.fileData = data;
          this.isLoading = false;
        })
        .catch((error) => {
          this.requestError = error;
        });
    },
  },
  mounted() {
    this.getFileList();
  },
};
</script>
