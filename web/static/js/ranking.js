$(function(){
    var url = '/ranking'
    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),

        editing: {
            allowUpdating: false,
            allowDeleting: false,
            allowAdding: false
        },

        paging: {
            pageSize: 12
        },

        pager: {
            showPageSizeSelector: false,
            allowedPageSizes: [8, 12, 20]
        },

        columns: [{
            dataField: "username",
            allowEditing: false
        }, {
            dataField: "score",
            dataType: "number",
            allowEditing: false
        }],
    }).dxDataGrid("instance");
});
