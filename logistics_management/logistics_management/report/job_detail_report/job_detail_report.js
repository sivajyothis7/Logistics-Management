// Copyright (c) 2024, siva and contributors
// For license information, please see license.txt

frappe.query_reports["Job Detail Report"] = {
    "filters": [
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "job_status",
            "label": __("Job Status"),
            "fieldtype": "Select",
            "options": "\nPending\nIn Progress\nCompleted\nOn Hold\nCancelled"
        },
        {
            "fieldname": "created_user",
            "label": __("Created User"),
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Partner"
        },
        // {
        //     "fieldname": "company",
        //     "label": __("Company"),
        //     "fieldtype": "Link",
        //     "options": "Company",
        //     "default": frappe.defaults.get_user_default("company")
        // }
    ]
};
