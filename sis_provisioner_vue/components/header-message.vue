<template>
  <div>
    <p v-show="$route.path == '/'">
      On this page, you can see the files that have been imported to Handshake.
      To manually import a new Handshake file:
      <br/>
      <ol>
        <li>Click &quot;Create new file&quot;, and select the enrollment term.</li>
        <li>The &quot;CSV Generated&quot; column indicates the status of the
        file-creation process.</li>
        <li>Once created, click &quot;Import to Handshake&quot; to import the file.</li>
      </ol>
    </p>
    <p v-show="$route.path.includes('/handshake-blocked-students')">
      View and manage students who are currently blocked from Handshake.
    </p>
    <p v-show="$route.path.includes('/uconnect-files')">
      On this page, you can see the files that have been imported to uConnect.
      To manually import a new uConnect file:
      <br/>
      <ol>
        <li>Click &quot;Create new file&quot;, and select the enrollment term.</li>
        <li>The &quot;CSV Generated&quot; column indicates the status of the
        file-creation process.</li>
        <li>Once created, click &quot;Import to uConnect&quot; to import the file.</li>
      </ol>
    </p>
    <p v-show="$route.path.includes('/uconnect-blocked-students')">
      View and manage students who are currently blocked from uConnect.
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
