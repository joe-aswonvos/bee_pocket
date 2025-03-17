document.addEventListener("DOMContentLoaded", function () {
  // Ensure modals have proper z-index when opened
  const modalElements = document.querySelectorAll(".modal");
  modalElements.forEach((modal) => {
    modal.addEventListener("show.bs.modal", function () {
      document.body.appendChild(modal);

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

  // Initialize Bootstrap toasts if present
  var toastElList = [].slice.call(document.querySelectorAll(".toast"));
  var toastList = toastElList.map(function (toastEl) {
    return new bootstrap.Toast(toastEl);
  });
  toastList.forEach((toast) => toast.show());

  // Check if the element with id "beepocket_select" exists before running the script
  const defaultBeepocketSelect = document.getElementById("beepocket_select");
  if (defaultBeepocketSelect) {
    if (defaultBeepocketSelect.value) {
      showItemInstances(defaultBeepocketSelect.value);
    }
  }

  // Check if the element with id "item_category" exists before adding event listener
  const itemCategorySelect = document.getElementById("item_category");
  if (itemCategorySelect) {
    itemCategorySelect.addEventListener("change", function () {
      var newCategoryInput = document.getElementById("new_category_name");
      if (this.value === "new") {
        newCategoryInput.style.display = "block";
      } else {
        newCategoryInput.style.display = "none";
      }
    });
  }
});

function editComment(commentId) {
  document.getElementById(`comment-text-${commentId}`).classList.add("d-none");
  document
    .getElementById(`edit-comment-form-${commentId}`)
    .classList.remove("d-none");
}

function cancelEdit(commentId) {
  document
    .getElementById(`comment-text-${commentId}`)
    .classList.remove("d-none");
  document
    .getElementById(`edit-comment-form-${commentId}`)
    .classList.add("d-none");
}

function showItemInstances(beepocketId) {
  if (!beepocketId) return;

  // Fetch and display item instances for the selected BeePocket
  fetch(`/create/item_instances/${beepocketId}/`)
    .then((response) => response.json())
    .then((data) => {
      const itemInstancesDiv = document.getElementById("item_instances");
      itemInstancesDiv.innerHTML = "";

      // Sort items: approved items at the bottom
      const sortedItems = data.item_instances.sort(
        (a, b) => a.approved - b.approved
      );

      sortedItems.forEach((instance) => {
        const card = document.createElement("div");
        card.className =
          "d-flex justify-content-between align-items-center mb-2";
        card.innerHTML = `
                  <div>
                    <h5 class="card-title">
                      <a href="/create/item/${instance.id}/">
                        ${
                          instance.approved
                            ? instance.item_name + " - APPROVED"
                            : instance.item_name
                        } 
                      </a>
                    </h5>
                    <p class="card-text">Created By: ${instance.created_by}</p>
                    <p class="card-text">Created On: ${instance.created_on}</p>
                    <p class="card-text">Active Status: ${
                      instance.active_status
                    }</p>
                    <p class="card-text">Approved: ${instance.approved}</p>
                  </div>
                  <div>
                    <span class="badge ${
                      instance.has_unread_comments
                        ? "text-warning"
                        : "text-secondary"
                    }">
                      <span class="material-icons">comment</span>
                      ${instance.comment_count}
                    </span>
                    <a href="/create/approve_item_instance/${
                      instance.id
                    }/" class="btn btn-success btn-sm ${
          instance.approved ? "disabled" : ""
        }" title="Approve Instance">
                      <span class="material-icons">check_circle</span>
                    </a>
                    <a href="/create/edit_item_instance/${
                      instance.id
                    }/" class="btn btn-warning btn-sm ${
          instance.approved ? "disabled" : ""
        }" title="Edit Instance">
                      <span class="material-icons">edit</span>
                    </a>
                    <a href="/create/delete_item_instance/${
                      instance.id
                    }/" class="btn btn-danger btn-sm ${
          instance.approved ? "disabled" : ""
        }" title="Delete Instance">
                      <span class="material-icons">delete</span>
                    </a>
                  </div>
                        
                `;
        itemInstancesDiv.appendChild(card);
      });
    });
}
