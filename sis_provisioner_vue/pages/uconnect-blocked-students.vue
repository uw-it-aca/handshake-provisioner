<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <BCard class="rounded-3 shadow-sm" header-bg-variant="transparent">
            <template #header>
              <h3>uConnect Blocked Students</h3>
              <HeaderMessage />
              <CreateBlockedStudent
                v-if="!isLoading"
                :apiPath="contextStore.context.uconnectBlockedUrl"
                @studentUpdated="loadBlockedStudentList()"
              />
            </template>
            <TableLoading v-if="isLoading"></TableLoading>
            <div v-if="studentData && studentData.length">
              <BlockedStudent
                v-if="!isLoading"
                :students="studentData"
                @studentUpdated="loadBlockedStudentList()"
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
  import BlockedStudent from "@/components/blocked-student.vue";
  import CreateBlockedStudent from "@/components/create-blocked-student.vue";
  import HeaderMessage from "@/components/header-message.vue";
  import { BCard } from "bootstrap-vue-next";
  import { useContextStore } from "@/stores/context";
  import { getBlockedStudents } from "@/utils/data";

  export default {
    components: {
      Layout,
      TableLoading,
      BlockedStudent,
      CreateBlockedStudent,
      HeaderMessage,
      BCard,
    },
    setup() {
      const contextStore = useContextStore();
      return {
        getBlockedStudents,
        contextStore,
      };
    },
    data() {
      return {
        pageTitle: "uConnect Blocked Students",
        studentData: [],
        isLoading: true,
        errorResponse: null,
      };
    },
    methods: {
      loadBlockedStudentList: function () {
        this.getBlockedStudents(this.contextStore.context.uconnectBlockedUrl)
          .then((data) => {
            this.studentData = data;
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
      this.loadBlockedStudentList();
    },
  };
</script>
