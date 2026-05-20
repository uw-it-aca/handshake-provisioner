<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2" class="my-2"
                >Handshake Import Files</axdd-card-heading
              >
              <axdd-card-action>
                <CreateFile
                  v-if="!isLoading"
                  :apiPath="contextStore.context.handshakeFilesUrl"
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
import { useContextStore } from "@/stores/context";
import { getFiles } from "@/utils/data";

export default {
  components: {
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
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
      pageTitle: "Handshake Import Files",
      fileData: [],
      isLoading: true,
      errorResponse: null,
    };
  },
  methods: {
    loadFileList: function () {
      this.getFiles(this.contextStore.context.handshakeFilesUrl)
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
