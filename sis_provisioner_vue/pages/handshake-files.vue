<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <BCard class="shadow-sm rounded-3" header-bg-variant="transparent">
            <template #header>
              <h3>Handshake Import Files</h3>
              <HeaderMessage />
              <CreateFile
                v-if="!isLoading"
                :apiPath="contextStore.context.handshakeFilesUrl"
                @fileUpdated="loadFileList()"
                ><i class="bi bi-plus-square text-dark me-2"></i>Create new
                file</CreateFile
              >
            </template>
            <TableLoading v-if="isLoading"></TableLoading>
            <div v-if="fileData && fileData.length">
              <ImportFile
                :files="fileData"
                @fileUpdated="loadFileList()"
              />
            </div>
            <div v-else>No data</div>
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
import HeaderMessage from "@/components/header-message.vue";
import { BCard } from "bootstrap-vue-next";
import { useContextStore } from "@/stores/context";
import { getFiles } from "@/utils/data";

export default {
  components: {
    Layout,
    TableLoading,
    ImportFile,
    CreateFile,
    HeaderMessage,
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
