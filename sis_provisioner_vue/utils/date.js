import dayjs from "dayjs";

function formatDate(dateString) {
  const date = dayjs(dateString);
  return date.format("MMM D, YYYY h:mm A");
}

export { formatDate };
