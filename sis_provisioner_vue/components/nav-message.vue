<template>
  <div class="text-light">
    <p
      v-show="$route.path == '/'"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      Welcome to the Handshake Import tool! On this page, you can browse files
      that have been imported to Handshake.
      <br /><br />
      To import a new file:
      <br/><br/>
      <ol>
        <li>Click &quot;Create new file&quot;, and select the enrollment term.</li>
        <br/>
        <li>The &quot;CSV Generated&quot; column indicates the status of the
        file-creation process.</li>
        <br/>
        <li>Once created, click &quot;Import to Handshake&quot; to import the file.</li>
      </ol>
    </p>

    <p
      v-show="$route.path.includes('/blocked-students')"
      class="text-light-gray bg-dark-purple rounded-3 p-3 small"
    >
      View and manage students who are currently blocked from Handshake.
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>
