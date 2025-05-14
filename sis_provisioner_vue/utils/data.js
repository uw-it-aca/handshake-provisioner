import "regenerator-runtime/runtime";
import { useCustomFetch } from "@/composables/customFetch";

async function getFiles() {
  return useCustomFetch("/api/v1/file/");
}

async function createFile(data) {
  return useCustomFetch("/api/v1/file/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({file: data}),
  });
}

async function importFile(fileId) {
  return useCustomFetch("/api/v1/file/" + fileId, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({}),
  });
}

async function deleteFile(fileId) {
  return useCustomFetch("/api/v1/file/" + fileId, {
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
  getFiles.
  createFile,
  importFile,
  deleteFile,
  getBlockedStudents,
  createBlockedStudent,
  deleteBlockedStudent,
};
