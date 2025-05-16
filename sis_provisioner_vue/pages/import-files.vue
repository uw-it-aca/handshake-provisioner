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
import Layout from "@/layout.vue";
import TableLoading from "@/components/table-loading.vue";
import ImportFile from "@/components/import-file.vue";
import CreateFile from "@/components/create-file.vue";
import { getFiles } from "@/utils/data";

export default {
  components: {
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
  },
  setup() {
    return {
      getFiles,
    };
  },
  data() {
    return {
      pageTitle: "Import Files",
      fileData: [],
      isLoading: true,
      errorResponse: null,
    };
  },
  methods: {
    loadFileList: function () {
      this.getFiles()
        .then((data) => {
          this.fileData = data;
        })
        .catch((error) => {
          this.errorResponse = error;
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
  mounted() {
    this.loadFileList();
  },
};
</script>
