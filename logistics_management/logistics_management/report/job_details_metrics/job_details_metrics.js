frappe.query_reports["Job Details Metrics"] = {
    "filters": [
        {
            "fieldname": "job_details",
            "label": __("Job Details"),
            "fieldtype": "Link",
            "options": "Job Details",
            "reqd": 0,
            "default": "",
            "width": "80"
        }
    ],

    "onload": function(report) {
        report.page.add_inner_button(__('Refresh Data'), function() {
            report.refresh();
        });
    },

    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        if (column.fieldname == "profit_and_loss") {
            if (data.profit_and_loss < 0) {
                value = `<span style="color:red">${value}</span>`;
            } else {
                value = `<span style="color:green">${value}</span>`;
            }
        }
        // Highlight outstanding amount of sales invoices in green
        if (column.fieldname == "outstanding_amount" && data.invoice_type === "Sales Invoice") {
            if (flt(value) === 0) {
                value = `<span style="color:black">${value}</span>`;
            } else {
                value = `<span style="color:red">${value}</span>`;
            }
        }
        // Highlight outstanding amount of purchase invoices in orange
        if (column.fieldname == "outstanding_amount" && data.invoice_type === "Purchase Invoice") {
            if (flt(value) === 0) {
                value = `<span style="color:black">${value}</span>`;
            } else {
                value = `<span style="color:orange">${value}</span>`;
            }
        }
        return value;
    }
};
