import "regenerator-runtime/runtime";
import { useCustomFetch } from "@/composables/customFetch";

async function getFiles(fileType) {
  const url = "/api/v1/file/" + fileType;
  return useCustomFetch(url);
}

async function createFile(fileType, data) {
  const url = "/api/v1/" + fileType + "/file";
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({file: data}),
  });
}

async function importFile(fileType, fileId) {
  const url = "/api/v1/" + fileType + "/file/" + fileId;
  return useCustomFetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({}),
  });
}

async function deleteFile(fileType, fileId) {
  const url = "/api/v1/" + fileType + "/file/" + fileId;
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function getBlockedStudents() {
  return useCustomFetch("/api/v1/blocked-student/");
}

async function createBlockedStudent(data) {
  return useCustomFetch("/api/v1/blocked-student/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({student: data}),
  });
}

async function deleteBlockedStudent(studentId) {
  return useCustomFetch("/api/v1/blocked-student/" + studentId, {
    method: "DELETE",
  });
}

export {
  getFiles,
  createFile,
  importFile,
  deleteFile,
  getBlockedStudents,
  createBlockedStudent,
  deleteBlockedStudent,
};
