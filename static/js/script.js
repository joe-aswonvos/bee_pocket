document.addEventListener("DOMContentLoaded", function () {

  // Ensure modals have proper z-index when opened
  const modalElements = document.querySelectorAll(".modal");
  modalElements.forEach((modal) => {
    modal.addEventListener("show.bs.modal", function () {
      // Set modal to higher z-index immediately
      modal.style.zIndex = "1050";

      setTimeout(() => {
        // Configure backdrop properly
        const backdrop = document.querySelector(".modal-backdrop");
        if (backdrop) {
          backdrop.style.zIndex = "1040";
        }

        // Make ALL modal content elements explicitly interactive
        const modalDialog = modal.querySelector(".modal-dialog");
        if (modalDialog) {
          modalDialog.style.pointerEvents = "auto";
          modalDialog.style.zIndex = "1060";
        }

        const modalContent = modal.querySelector(".modal-content");
        if (modalContent) {
          modalContent.style.pointerEvents = "auto";
          modalContent.style.opacity = "1";
          modalContent.style.zIndex = "1060";
        }

        // Ensure all form elements within the modal are interactive
        const formElements = modal.querySelectorAll(
          "input, select, button, textarea, a"
        );
        formElements.forEach((el) => {
          el.style.pointerEvents = "auto";
          el.style.opacity = "1";
        });
      }, 0);
    });
  });

  const defaultBeepocketSelect = document.getElementById("beepocket_select");
  if (defaultBeepocketSelect.value) {
    showItemInstances(defaultBeepocketSelect.value);
  }
});

function showItemInstances(beepocketId) {
  if (!beepocketId) return;

  // Fetch and display item instances for the selected BeePocket
  fetch(`/create/item_instances/${beepocketId}/`)
    .then((response) => response.json())
    .then((data) => {
      const itemInstancesDiv = document.getElementById("item_instances");
      itemInstancesDiv.innerHTML = "";
      data.item_instances.forEach((instance) => {
        const card = document.createElement("div");
        card.className = "col-md-12";
        card.innerHTML = `
                    <div class="card mb-3">
                        <div class="card-header">
                            ${instance.item_name}
                        </div>
                        <div class="card-body">
                            <p class="card-text">Created By: ${instance.created_by}</p>
                            <p class="card-text">Created On: ${instance.created_on}</p>
                            <p class="card-text">Active Status: ${instance.active_status}</p>
                            <p class="card-text">Approved: ${instance.approved}</p>
                            <a href="/create/approve_item_instance/${instance.id}/" class="btn btn-success btn-sm" title="Approve Instance">
                                <span class="material-icons">check_circle</span>
                            </a>
                            <a href="/create/edit_item_instance/${instance.id}/" class="btn btn-warning btn-sm" title="Edit Instance">
                                <span class="material-icons">edit</span>
                            </a>
                            <a href="/create/delete_item_instance/${instance.id}/" class="btn btn-danger btn-sm" title="Delete Instance">
                                <span class="material-icons">delete</span>
                            </a>
                        </div>
                    </div>
                `;
        itemInstancesDiv.appendChild(card);
      });
    });
}
