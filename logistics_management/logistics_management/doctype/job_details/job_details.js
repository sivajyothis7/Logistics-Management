// Copyright (c) 2024, siva and contributors
// For license information, please see license.txt

frappe.ui.form.on("Job Details", {
    refresh(frm) {
        // Add a custom button "Generate POD"
        frm.add_custom_button(__('Generate POD'), function() {
            var objWindowOpenResult = window.open(frappe.urllib.get_full_url("/printview?"
                + "doctype=" + encodeURIComponent("Job Details")
                + "&name=" + encodeURIComponent(frm.doc.name)
                + "&trigger_print=0"
                + "&format=POD"
                + "&no_letterhead=0"
                + "&_lang=en"
            ));

            if (!objWindowOpenResult) {
                frappe.msgprint(__("Please set permission for pop-up windows in your browser!"));
                return;
            }
        });
    },
});

