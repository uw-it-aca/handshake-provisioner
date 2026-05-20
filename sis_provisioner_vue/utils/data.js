import "regenerator-runtime/runtime";
import { useCustomFetch } from "@/composables/customFetch";

async function getFiles(url) {
  return useCustomFetch(url);
}

async function createFile(url, data) {
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({file: data}),
  });
}

async function importFile(url) {
  return useCustomFetch(url, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({}),
  });
}

async function deleteFile(url) {
  return useCustomFetch(url, {
    method: "DELETE",
  });
}

async function getBlockedStudents(url) {
  return useCustomFetch(url);
}

async function createBlockedStudent(url, data) {
  return useCustomFetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=UTF-8",
    },
    body: JSON.stringify({student: data}),
  });
}

async function deleteBlockedStudent(url) {
  return useCustomFetch(url, {
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
