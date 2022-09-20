import dayjs from "dayjs";

function formatDate(dateString) {
  const date = dayjs(dateString);
  return date.format("MMMM D, YYYY");
}

function downloadFile(url) {
  fetch(url).catch((error) => {
    alert(error);
  });
}

export { formatDate, downloadFile };
