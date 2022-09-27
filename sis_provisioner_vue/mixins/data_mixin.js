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
    saveFile: async function (file) {
      return axios.post(
        "/api/v1/file/",
        { file: file },
        this._getAxiosConfig()
      );
    },
  },
};

export default dataMixin;
