frappe.ui.form.on("Job Details", {
    refresh: function(frm) {
        add_custom_button(frm);
        frm.events.set_dashboard_indicators(frm); 
    },

    set_dashboard_indicators: function(frm) {
        // Your existing code for dashboard indicators
    }
});

function add_custom_button(frm) {
    frm.add_custom_button(__('Job Ledger'), function() {
        frappe.set_route('query-report', 'Job Details Metrics', {
            
            job_details: frm.doc.name
        });
    }, __('View'));

    frm.add_custom_button(__('Generate Project'), function() {
        frappe.call({
            method: 'logistics_management.logistics_management.doctype.job_details.job_details.generate_project',
            args: {
                docname: frm.docname
            },
            callback: function(response) {
                if (response.message) {
                    frm.reload_doc();
                    // frappe.msgprint('Waybill generated successfully.');
                }
            }
        });
    });
}
