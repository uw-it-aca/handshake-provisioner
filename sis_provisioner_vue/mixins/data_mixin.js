import "regenerator-runtime/runtime";
import axios from "axios";

const dataMixin = {
  methods: {
    _getAxiosConfig: function () {
      const csrfToken = this.$store.state.csrfToken;
      const axiosConfig = {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
          "X-CSRFToken": csrfToken,
        },
      };
      return axiosConfig;
    },
    getFiles: async function () {
      return axios.get(
        "/api/v1/file/",
        {},
        this._getAxiosConfig()
      );
    },
    createFile: async function (file) {
      return axios.post(
        "/api/v1/file/",
        { file: file },
        this._getAxiosConfig()
      );
    },
    importFile: async function (fileId) {
      return axios.put(
        "/api/v1/file/" + fileId,
        {},
        this._getAxiosConfig()
      );
    },
    deleteFile: async function (fileId) {
      return axios.delete(
        "/api/v1/file/" + fileId,
        this._getAxiosConfig()
      );
    },
    getBlockedStudents: async function () {
      return axios.get(
        "/api/v1/blocked-student/",
        {},
        this._getAxiosConfig()
      );
    },
    createBlockedStudent: async function (student) {
      return axios.post(
        "/api/v1/blocked-student/",
        { student: student },
        this._getAxiosConfig()
      );
    },
    deleteBlockedStudent: async function (studentId) {
      return axios.delete(
        "/api/v1/blocked-student/" + studentId,
        this._getAxiosConfig()
      );
    },
  },
};

export default dataMixin;
