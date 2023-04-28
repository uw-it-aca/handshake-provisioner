<template>
  <Layout :page-title="pageTitle">
    <template #content>
      <div class="row my-4">
        <div class="col">
          <axdd-card>
            <template #heading-action>
              <axdd-card-heading :level="2" class="my-2"
                >Blocked Students</axdd-card-heading
              >
              <axdd-card-action>
                <AddBlockedStudent
                  @studentUpdated="loadBlockedStudentList()"
                  ><i class="bi bi-plus-square text-dark me-2"></i>Add student
                </AddBlockedStudent
                >
              </axdd-card-action>
            </template>
            <template #body>
              <TableLoading v-if="isLoading"></TableLoading>
              <div v-if="studentData && studentData.length">
                <BlockedStudent
                  :students="studentData"
                  @studentUpdated="loadlockedStudentList()"
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
import dataMixin from "../mixins/data_mixin.js";
import Layout from "../layout.vue";
import TableLoading from "../components/table-loading.vue";
import BlockedStudent from "../components/blocked-student.vue";
import CreateBlockedStudent from "../components/create-blocked-student.vue";

export default {
  mixins: [dataMixin],
  components: {
    // app components
    Layout,
    TableLoading,
    BlockedStudent,
    CreateBlockedStudent,
  },
  data() {
    return {
      pageTitle: "Blocked Students",
      studentData: [],
      isLoading: true,
      timer: '',
    };
  },
  methods: {
    loadBlockedStudentList: function () {
      this.getBlockedStudents().then(
        (response) => {
          if (response.data) {
            this.studentData = response.data;
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
    this.loadBlockedStudentList();
    /* this.timer = setInterval(this.loadBlockedStudentList, 60000); */
  },
  beforeUnmount() {
    /* clearInterval(this.timer); */
  }
};
</script>
