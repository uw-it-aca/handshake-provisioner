<template>
  <div class="text-light">
    <ul class="nav flex-column mb-5">
      <li class="nav-item mb-1">
        <router-link
          :to="'/'"
          active-class="bg-dark-purple rounded-3"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          ><i class="bi bi-calendar-check me-2"></i>Import files</router-link
        >
      </li>
      <li class="nav-item mb-1">
        <router-link
          :to="'/caseload'"
          class="nav-link text-gray d-block px-3 py-2 bg-dark-purple-hover rounded-3"
          :class="
            $route.path.includes('/caseload') ? 'bg-dark-purple rounded-3' : ''
          "
          ><i class="bi bi-people-fill me-2"></i>Blocked students</router-link
        >
      </li>
      <li aria-hidden="true" class="nav-item mt-1 mb-2">
        <a
          href="#"
          class="nav-link disabled text-gray d-block p-0 internal-link"
          ><hr class="m-0 bg-gray" />
          <span class="visually-hidden">Navigation separator</span></a
        >
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>
