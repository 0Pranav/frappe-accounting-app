frappe.treeview_settings["Account"]={
    breadcrumbs:"Account",
    title:__("Chart of Accounts"),
    root_label:"Accounts",
    onrender:async function(node){
        if(frappe.boot.user.can_read.indexOf("General Ledger") !== -1){ 
            var res = await frappe.db.get_value("Account",node.title,['account_balance','account_type'])
            debugger
           if(node.data && res !== undefined){
               $('<span class="balance-area pull-right text-muted small">'+res.message.account_balance+ (in_list(["Liability","Income"],res.message.account_type)?" Cr":" Dr")+'</span>').insertBefore(node.$ul)
           } 
        }
    }
}