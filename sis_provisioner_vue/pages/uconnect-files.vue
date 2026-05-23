<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <BCard class="shadow-sm rounded-3" header-bg-variant="transparent">
            <template #header>
              <div class="d-flex justify-content-between align-items-end">
                <h3>uConnect Import Files</h3>
                <CreateFile
                  v-if="!isLoading"
                  :apiPath="contextStore.context.uconnectFilesUrl"
                  @fileUpdated="loadFileList()"
                />
              </div>
              <p>
                View and manage data files that have been imported to uConnect.
              </p>
            </template>
            <TableLoading v-if="isLoading"></TableLoading>
            <div v-if="fileData && fileData.length">
              <ImportFile
                :files="fileData"
                @fileUpdated="loadFileList()"
              />
            </div>
            <div v-else class="fw-bold">No Import Files found</div>
          </BCard>
        </div>
      </div>
    </template>
  </Layout>
</template>

<script>
import Layout from "@/layouts/default.vue";
import TableLoading from "@/components/table-loading.vue";
import ImportFile from "@/components/import-file.vue";
import CreateFile from "@/components/create-file.vue";
import { BCard } from "bootstrap-vue-next";
import { useContextStore } from "@/stores/context";
import { getFiles } from "@/utils/data";

export default {
  components: {
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
    BCard,
  },
  setup() {
    const contextStore = useContextStore();
    return {
      getFiles,
      contextStore,
    };
  },
  data() {
    return {
      pageTitle: "uConnect Import Files",
      fileData: [],
      isLoading: true,
      errorResponse: null,
    };
  },
  methods: {
    loadFileList: function () {
      this.getFiles(this.contextStore.context.uconnectFilesUrl)
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
