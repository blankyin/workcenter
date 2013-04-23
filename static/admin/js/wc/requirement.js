/**
 * User: yinchangjiang.ht
 * Date: 13-4-21
 * Time: 上午9:54
 */

$(document).ready(function () {

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
                    url: "do.php?action=del",
                    data: "ids=" + sels,
                    beforeSend: function () {
                        $().message("正在请求...");
                    },
                    error: function () {
                        $().message("请求失败...");
                    },
                    success: function (msg) {
                        if (msg != 0) {
                            var arr = msg.split(',');
                            $.each(arr, function (i, n) {
                                if (arr[i] != "") {
                                    $("#list").jqGrid('delRowData', n);
                                }
                            });
                            $().message("已成功删除!");
                        } else {
                            $().message("操作失败！");
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


function requirement_detail(cellvalue){
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

