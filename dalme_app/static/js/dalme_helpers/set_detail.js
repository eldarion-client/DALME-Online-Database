function set_detail() {
}

function edit_set(id) {
      $.ajax({
        method: "GET",
        url: `${api_endpoint}/options/?target=active_staff,user_groups_1&format=json`,
        xhrFields: { withCredentials: true },
        crossDomain: true,
        headers: {
          "Content-Type": "application/json",
          'X-CSRFToken': get_cookie("csrftoken")
        }
      }).done(function(data, textStatus, jqXHR) {
          const staff = data.active_staff;
          const usergroups = data.user_groups;
          editSetForm = new $.fn.dataTable.Editor( {
                ajax: {
                  method: "PATCH",
                  url: `${api_endpoint}/sets/_id_/`,
                  headers: { 'X-CSRFToken': get_cookie("csrftoken") },
                  data: function (data) { return { "data": JSON.stringify( data ) }; }
                },
                fields: [
                    {
                      label: "Id",
                      name:  "id",
                      type: "hidden"
                    },
                    {
                      label: "Name:",
                      name:  "name"
                    },
                    {
                      label: "Type",
                      name: "set_type",
                      type: "selectize",
                      options: [
                        { label: "Corpus", value: "1" },
                        { label: "Collection", value: "2" },
                        { label: "Dataset", value: "3" },
                        { label: "Workset", value: "4" },
                      ],
                    },
                    {
                      label: "Description:",
                      name:  "description",
                      type: "textarea"
                    },
                    {
                      label: "Owner",
                      name:  "owner",
                      type: "selectize",
                      opts: {'placeholder': "Select owner"},
                      options: staff
                    },
                    {
                      label: "Permissions:",
                      name:  "permissions",
                      type: "selectize",
                      options: [
                        { label: "Private", value: "1" },
                        { label: "Others: view", value: "2" },
                        { label: "Others: view|add", value: "3" },
                        { label: "Others: view|add|delete", value: "4" },
                      ],
                    },
                    {
                      label: "Public",
                      name:  "is_public",
                      type: "checkbox",
                      options: [
                        {label: "Set featured in the public-facing website.", value: true}
                      ],
                    },
                    {
                      label: "Landing",
                      name:  "has_landing",
                      type: "checkbox",
                      options: [
                        {label: "Set has a landing page on the public-facing website.", value: true}
                      ],
                    },
                    {
                      label: "DS User Group",
                      name: "dataset_usergroup",
                      type: "selectize",
                      opts: {'placeholder': "Select user group"},
                      options: usergroups
                    },
                    {
                      label: "Stat Title:",
                      name:  "stat_title"
                    },
                    {
                      label: "Stat Text:",
                      name:  "stat_text",
                      type: "textarea"
                    }
                  ]
          });
          editSetForm.hide(['is_public', 'has_landing', 'dataset_usergroup', 'stat_title', 'stat_text']);
          editSetForm.field('set_type').input().on('change.dalme', change_on_set_type);
          editSetForm.on('submitSuccess', function(e, json, data, action) {
            toastr.success('The set was updated successfully.');
            location.reload();
          });
          editSetForm.buttons({
            text: "Update",
            className: "btn btn-primary",
            action: function () { this.submit(); }
          }).title('Edit Set').edit(id, false);
          for (const prop in set) {
              if (set.hasOwnProperty(prop)) {
                  editSetForm.set(prop, set[prop]);
              }
          };
          editSetForm.open();
      });
}

function change_on_set_type(callback='undefined') {
  var stype = editSetForm.get('set_type');
  editSetForm.hide(['is_public', 'has_landing', 'dataset_usergroup', 'stat_title', 'stat_text']);
  if (stype == "2") {
    editSetForm.show(['is_public', 'has_landing', 'stat_title', 'stat_text']);
  } else if (stype == "3") {
    editSetForm.show('dataset_usergroup');
  }
}

function delete_set_members(table, id) {
    const confirmation = confirm("Are you sure you want to remove these records from the set? This action cannot be undone.")
    if (confirmation) {
        var selected = table.rows( { selected: true } ).data();
        var sel_ids = []
        for (let i = 0, len = selected.length; i < len; ++i) {
          sel_ids.push(selected[i][0]);
        };
        $.ajax({
          method: "PATCH",
          url: `${api_endpoint}/sets/${id}/remove_members/`,
          xhrFields: { withCredentials: true },
          crossDomain: true,
          headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': get_cookie("csrftoken")
          },
          data: JSON.stringify({ members: sel_ids })
        }).done(function(data, textStatus, jqXHR) {
          table.rows( { selected: true } ).remove().draw();
          toastr.success('The set was updated successfully.')
        }).fail(function(jqXHR, textStatus, errorThrown) {
          toastr.error('There was an error communicating with the server: '+errorThrown);
        });
    }
}
