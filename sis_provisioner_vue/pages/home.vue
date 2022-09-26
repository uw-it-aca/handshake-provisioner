<template>
  <Layout :page-title="pageTitle">
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
              <TableLoading v-if="isLoading"></TableLoading>
              <div v-if="fileData && fileData.length">
                <ImportFile :files="fileData" />
              </div>
              <div v-else>No data</div>
            </template>
          </axdd-card>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import dataMixin from "../mixins/data_mixin.js";
import { Card, CardHeading, CardAction } from "axdd-components";
import Layout from "../layout.vue";
import TableLoading from "../components/table-loading.vue";
import ImportFile from "../components/import-file.vue";
import CreateFile from "../components/create-file.vue";

export default {
  mixins: [dataMixin],
  components: {
    // app components
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
    // axdd-components
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
    "axdd-card-action": CardAction,
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
