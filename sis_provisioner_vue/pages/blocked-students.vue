<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2" class="my-2"
                >Handshake Blocked Students</axdd-card-heading
              >
              <axdd-card-action>
                <CreateBlockedStudent
                  @studentUpdated="loadBlockedStudentList()"
                  ><i class="bi bi-plus-square text-dark me-2"></i>Add student
                </CreateBlockedStudent
                >
              </axdd-card-action>
            </template>
            <template #body>
              <TableLoading v-if="isLoading"></TableLoading>
              <div v-if="studentData && studentData.length">
                <BlockedStudent
                  :students="studentData"
                  @studentUpdated="loadBlockedStudentList()"
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
import BlockedStudent from "@/components/blocked-student.vue";
import CreateBlockedStudent from "@/components/create-blocked-student.vue";
import { useContextStore } from "@/stores/context";
import { getBlockedStudents } from "@/utils/data";

export default {
  components: {
    Layout,
    TableLoading,
    BlockedStudent,
    CreateBlockedStudent,
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
      pageTitle: "Handshake Blocked Students",
      studentData: [],
      isLoading: true,
      errorResponse: null,
    };
  },
  methods: {
    loadBlockedStudentList: function () {
      this.getBlockedStudents(this.contextStore.context.blockedStudentsUrl)
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
