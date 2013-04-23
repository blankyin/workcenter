/**
 * Created with PyCharm.
 * User: yinchangjiang.ht
 * Date: 13-4-15
 * Time: 下午8:40
 * To change this template use File | Settings | File Templates.
 */


$(document).ready(function() {

    $("#gridTable").jqGrid({
        mtype: "GET",
        url: "/admin/workcenter/foo_list",
        datatype: "json",
        height: 250,
        width:800,
        colNames:['编号','名称'],
        colModel:[
            {name:'id',index:'id', width:260, sorttype:"int"},
            {name:'name',index:'name', width:290}
        ],
        sortname:'id',
        sortorder:'asc',
        viewrecords:true,
        rowNum:10,
        rowList:[10,20,30],
        pager:"#gridPager",
        caption: "第一个jqGrid例子",

    }).navGrid('#pager2',{edit:true,add:true,del:true});


    // 新增
    $('#close').on('click', function(){
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
        success: function(msg){
            if(msg==1){ //如果成功提交
                jQuery.fancybox.close();   //关闭fancybox弹出层
                alert("成功添加"); //提示信息
                $("#gridTable").trigger("reloadGrid"); //重新载入jqGrid数据
            }else{
                alert(msg);
            }
        }
    });


    // 删除
    $("#del_btn").click(function(){
        var sels = $("#gridTable").jqGrid('getGridParam','selarrrow');
        if(sels==""){
            $.pnotify({
                title: '提示',
                text: '请选择要删除的项！'
            });
        }else{
            if(confirm("您是否确认删除？")){
                $.ajax({
                    type: "POST",
                    url: "do.php?action=del",
                    data: "ids="+sels,
                    beforeSend: function() {
                        $().message("正在请求...");
                    },
                    error:function(){
                        $().message("请求失败...");
                    },
                    success: function(msg){
                        if(msg!=0){
                            var arr = msg.split(',');
                            $.each(arr,function(i,n){
                                if(arr[i]!=""){
                                    $("#list").jqGrid('delRowData',n);
                                }
                            });
                            $().message("已成功删除!");
                        }else{
                            $().message("操作失败！");
                        }
                    }
                });
            }
        }
    });

});


function validate(formData, jqForm, options) {
    for (var i=0; i < formData.length; i++) {
        if (!formData[i].value) {
//            $.pnotify({
//                title: '提示',
//                text: '请选择要删除的项！'
//            });
            alert("请输入完整相关信息");
            return false;
        }
    }

    $().message("正在提交...");
}