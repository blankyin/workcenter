/**
 * User: yinchangjiang.ht
 * Date: 13-4-21
 * Time: 上午9:54
 */

$(document).ready(function () {
    $("#requirementTable").jqGrid({
        mtype: "POST",
        url: "/admin/workcenter/requirement_list/",
        datatype: "json",
        height: 300,
        //        width: 'auto',
        autowidth: true,
        rownumbers: true,
//        cellEdit: true,
        colNames: ['操作', '需求状态', '需求单号', '需求名称', '需求类别', '需求部门', '需求描述'
            , '期望完成日期', '需求提出人', '需求提出时间', '修改人', '修改时间'],
        colModel: [
            {name: 'id', index: 'id', width: 100, sortable: false, frozen: true, resizable: true, search: false,
                formatter: function (cellvalue, options, rowObject) {
                    opration = '<a onclick="requirement_detail(' + cellvalue + ')">详情</a>'
                    return opration
                }
            },
            {name: 'status', index: 'status', width: 100 },
            {name: 'requirement_code', index: 'requirement_code', width: 100},
            {name: 'requirement_name', index: 'requirement_name', width: 100, editable: true, edittype: 'text', editrules: {required: true} },
            {name: 'requirement_type_name', index: 'requirement_type', width: 100,
                editable: true, edittype: 'select', editrules: {required: true},
                editoptions: {
                    dataUrl: "/admin/workcenter/requirement_type_list/"
                },
                search: true, stype: 'select',
                searchoptions: {
                    // value: buildRequirementTypeSelect(),
                    dataUrl: "/admin/workcenter/requirement_type_list/",
                    sopt: ['eq']
                }
            },
            {name: 'requirement_dept_name', index: 'requirement_dept', width: 100,
                editable: true, edittype: 'select', editrules: {required: true},
                editoptions: {
                    dataUrl: "/admin/workcenter/requirement_dept_list/"
                },
                search: true, stype: 'select',
                searchoptions: {
                    dataUrl: "/admin/workcenter/requirement_dept_list/",
                    sopt: ['eq']
                }},
            {name: 'requirement_desc', index: 'requirement_desc', width: 100, editable: true, edittype: 'textarea', editoptions: {rows: "2", cols: "10"} },
            {name: 'gmt_hope_finished', index: 'gmt_hope_finished', width: 150,
                formatter: "date", formatoptions: {srcformat: 'Y-m-d H:i:s', newformat: 'Y-m-d'},
                search: true,
                searchoptions: {
                    dataInit: function (elem) {
                        jQuery(elem).datepicker({dateFormat: 'yy-mm-dd'});
                    },
                    attr: {title: '期望完成日期'},
                    sopt: ['eq']
                }},
            {name: 'submitter_user_name', index: 'submitter_user_name', width: 100,
                search: true, stype: 'select',
                searchoptions: {
                    dataUrl: "/admin/workcenter/user_list/",
                    sopt: ['eq']
                }
            },
            {name: 'gmt_submit', index: 'gmt_submit', width: 150,
                search: true,
                searchoptions: {
                    dataInit: function (elem) {
//                        $(elem).click(function(){
//                            WdatePicker({readOnly:true})
//                        })
                        jQuery(elem).datepicker({dateFormat: 'yy-mm-dd'});
                    },
                    attr: {title: '需求提出时间'},
                    sopt: ['eq']
                }
            },
            {name: 'modifier_user_name', index: 'modifier_user_name', width: 100, search: false},
            {name: 'gmt_modified', index: 'gmt_modified', width: 150, search: false}

        ],
        sortname: 'gmt_submit',
        sortorder: 'desc',
        viewrecords: true,
        rowNum: 10,
        rowList: [10, 20, 30],
        pager: "#requirementPager",
        multiselect: true,
        caption: "第一个jqGrid例子",
        gridview: true,


        ondblClickRow: function (id) {
            if (id) {
                var rowData = $("#requirementTable").jqGrid("getRowData", id);
                // 'editGridRow'会弹出修改窗口，'editRow'直接在列表修改
                $('#requirementTable').jqGrid('editGridRow', id, {
                    keys: true,        //这里按[enter]保存
                    url: '/admin/workcenter/update_requirement/',
                    mtype: "POST",
                    restoreAfterError: true,
                    closeAfterEdit: true,
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    extraparam: {
                        "id": id
//                        ,
//                        "requirement_type": $("#" + id + "_requirement_type").val(),
                    },
                    successfunc: function (response) {
                        result = eval(response.responseText)
                        if (result[0].status == true) {
                            alert('修改成功！')
                        } else {
                            alert('修改失败！')
                        }
                        jQuery("#requirementTable").jqGrid().trigger("reloadGrid");
                        return true;
                    },
                    errorfunc: function (rowid, res) {
                        console.log(rowid);
                    },
                    afterSubmit: function (response) {  // 使用"editGridRow"时此方法会生效
                        result = eval(response.responseText)
                        if (result[0].status == true) {
                            alert('修改成功！')
                        } else {
                            alert('修改失败！')
                        }
                        jQuery("#requirementTable").jqGrid().trigger("reloadGrid");
                        return true;
                    }
                });
            }
        }
//        ,
//        loadComplete: function () {
//            alert("grid is loaded/reloaded");
//        }

    }).navGrid('#pager', {edit: false, add: false, del: false, searchtext: '查找', refreshtext: '刷新表格'});
    $('#requirementTable').jqGrid('filterToolbar', { searchOnEnter: true, enableClear: true });


    // 固定栏位
    jQuery("#requirementTable").jqGrid('setFrozenColumns');

    $("#add_btn").click(function () {
        $.fancybox({
            'type': 'ajax',
            'href': '/admin/workcenter/add_requirement/'
        });
    });

    // 删除
    $("#del_btn").click(function () {
        var sels = $("#requirementTable").jqGrid('getGridParam', 'selarrrow');
        if (sels == "") {
            $.pnotify({
                title: '提示',
                text: '请选择要删除的项！'
            });
        } else {
            if (confirm("您是否确认删除？")) {
                $.ajax({
                    type: "POST",
                    url: "/admin/workcenter/del_requirement/",
                    data: "ids=" + sels,
                    dataType: "json", /*这句可用可不用，没有影响*/
                    // contentType: "application/json; charset=utf-8",
                    success: function (data) {
                        if (data["status"] == true) {
                            jQuery("#requirementTable").jqGrid("setGridParam", {
                                url: "/admin/workcenter/requirement_list/"
                            }).trigger("reloadGrid");
                            alert('删除成功！')
                        } else {
                            alert('删除失败！')
                        }
                    }
                });
            }
        }
    });

    // 新增
    $('#close').on('click', function () {
        $.fancybox.close(true);
        $.fancybox.close();
        parent.$.fancybox.close(true);
        parent.$.fancybox.close();
        parent.$.fn.fancybox.close(true)
        parent.$.fn.fancybox.close()
        console.log('tried to close');
    });


    $('#add_form').ajaxForm({
        beforeSubmit: validate, //验证表单
        success: function (msg) {
            if (msg == 1) { //如果成功提交
                jQuery.fancybox.close();   //关闭fancybox弹出层
                alert("成功添加"); //提示信息
                $("#requirementTable").trigger("reloadGrid"); //重新载入jqGrid数据
            } else {
                alert(msg);
            }
        }
    });

});


// 详情链接
function requirement_detail(cellvalue) {
    $.fancybox({
        'type': 'ajax',
        'href': '/admin/workcenter/requirement_detail/' + cellvalue
    });
}


function validate(formData, jqForm, options) {
    for (var i = 0; i < formData.length; i++) {
        if (!formData[i].value) {
            alert("请输入完整相关信息");
            return false;
        }
    }

    // $().message("正在提交...");
}

/**
 * 查询功能
 */
var timeoutHnd;
var flAuto = false;

function doSearch(ev) {
    if (!flAuto)
        return;
    if (timeoutHnd)
        clearTimeout(timeoutHnd)
    timeoutHnd = setTimeout(gridReload, 500)
}

function gridReload() {
    var search_requirement_name = jQuery("#search_requirement_name").val();
    var search_requirement_type = jQuery("#search_requirement_type").val();
    jQuery("#requirementTable").jqGrid("setGridParam", {
        url: "/admin/workcenter/requirement_list/",
        page: 1,
        postData: {"requirement_name": search_requirement_name, "requirement_type": search_requirement_type}
    }).trigger("reloadGrid");
}

function enableAutosubmit(state) {
    flAuto = state;
    jQuery("#submitButton").attr("disabled", state);
}

//function buildRequirementTypeSelect() {
//    htmlobj = $.ajax({
//        dataType:"text",
//        url: "/admin/workcenter/requirement_type_list/",
//        async: true
//    });
//    values = htmlobj.responseText;
//
//    var values = ":All;1:A;2:B";
//    return values;
//}