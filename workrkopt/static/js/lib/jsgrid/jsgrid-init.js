        $(function() {

            $("#jsGrid").jsGrid({
                height: "100%",
                width: "100%",
                filtering: false,
                editing: true,
                inserting: true,
                sorting: true,
                paging: true,
                autoload: true,
                pageSize: 15,
                pageButtonCount: 5,
                deleteConfirm: "Do you really want to delete the client?",
                controller: db,
                fields: [
                    { name: "ID", type: "text", width: 150 },
                    { name: "Name", type: "text", width: 150 },
                    { name: "Age", type: "number", width: 50 },
                    { name: "Email", type: "text", width: 200 },
                    { name: "Phone", type: "text", width: 200 },
                    { name: "Position", type: "select", items: db.positions, valueField: "Id", textField: "Name" },
                    { name: "Schedule", type: "select", items: db.schedules, valueField: "Id", textField: "Name" },
                    { name: "Working", type: "checkbox", title: "Is Working", sorting: false },
                    { type: "control" }
                ]
            });

        });