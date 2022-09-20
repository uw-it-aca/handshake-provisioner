<template>
  <table class="table mb-0">
    <thead class="small">
      <tr>
        <th scope="col" class="w-50 ps-0">Name</th>
        <th scope="col">&nbsp;</th>
        <th scope="col">Created</th>
        <th scope="col">Role</th>
        <th scope="col">Owner</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="index in 4" :key="index">
        <td class="ps-0 placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
          <div><span class="placeholder bg-light-gray col-5"></span></div>
        </td>
        <td class="align-middle">
          <button
            type="button"
            disabled
            class="btn btn-sm placeholder bg-light-gray text-muted rounded-pill px-3"
          >
            Download
          </button>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
        </td>
        <td class="placeholder-glow">
          <div><span class="placeholder bg-light-gray col-10"></span></div>
        </td>
      </tr>
    </tbody>
  </table>
</template>
