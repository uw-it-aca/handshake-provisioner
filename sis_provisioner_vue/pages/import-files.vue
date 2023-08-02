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
                <CreateFile
                  @fileUpdated="loadFileList()"
                  ><i class="bi bi-plus-square text-dark me-2"></i>Create new
                  file</CreateFile
                >
              </axdd-card-action>
            </template>
            <template #body>
              <TableLoading v-if="isLoading"></TableLoading>
              <div v-if="fileData && fileData.length">
                <ImportFile
                  :files="fileData"
                  @fileUpdated="loadFileList()"
                />
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
import dataMixin from "@/mixins/data_mixin.js";
import Layout from "@/layout.vue";
import TableLoading from "@/components/table-loading.vue";
import ImportFile from "@/components/import-file.vue";
import CreateFile from "@/components/create-file.vue";

export default {
  mixins: [dataMixin],
  components: {
    // app components
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
  },
  data() {
    return {
      pageTitle: "Import Files",
      fileData: [],
      isLoading: true,
      timer: '',
    };
  },
  methods: {
    loadFileList: function () {
      this.getFiles().then(
        (response) => {
          if (response.data) {
            this.fileData = response.data;
            this.isLoading = false;
          }
        }
      ).catch(
        (error) => {
          this.requestError = error;
          this.isLoading = false;
        }
      );
    },
  },
  mounted() {
    this.loadFileList();
    this.timer = setInterval(this.loadFileList, 60000);
  },
  beforeUnmount() {
    clearInterval(this.timer);
  }
};
</script>
