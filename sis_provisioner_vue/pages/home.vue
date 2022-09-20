<template>
  <layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #body>
              <axdd-card-heading :level="2" class="my-2"
                >Import Files</axdd-card-heading
              >
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
import {
  Card,
  CardHeading,
  TabsList,
  TabsDisplay,
  TabsItem,
  TabsPanel,
} from "axdd-components";
import Layout from "../layout.vue";
import ImportFile from "../components/file.vue";
import TableLoading from "../components/table-loading.vue";

export default {
  components: {
    layout: Layout,
    file: ImportFile,
    "table-loading": TableLoading,
    "axdd-card": Card,
    "axdd-card-heading": CardHeading,
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
    getFileData() {
      fetch("/api/v1/file")
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
    // fetch the file data
    this.getFileData();
    //setTimeout(this.getFileData, 3000);
  },
};
</script>
